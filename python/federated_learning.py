import config
from client_node import ClientNode
from validator_node import ValidatorNode
from ipfs_manager import IPFSManager
from snowball_consensus import SnowballConsensus
from web3 import Web3
import json
import os
import numpy as np

class GlobalModelAggregator:
    def __init__(self, initial_model):
        self.global_model = initial_model

    def aggregate_updates(self, validated_updates):
        if not validated_updates:
            print("No updates to aggregate.")
            return

        aggregated_update = [np.zeros_like(layer) for layer in self.global_model]
        total_weight = 0

        for update, weight in validated_updates:
            if len(update) != len(self.global_model):
                raise ValueError("Update shape does not match global model shape.")

            total_weight += weight
            for i, layer in enumerate(update):
                aggregated_update[i] += layer * weight

        if total_weight > 0:
            for i in range(len(aggregated_update)):
                aggregated_update[i] /= total_weight
                self.global_model[i] += aggregated_update[i]
        else:
            print("Total weight is zero, aggregation skipped.")

    def get_global_model(self):
        return self.global_model

def main():
    # Connect to Ethereum
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

    # Check available accounts
    print("Available accounts:", w3.eth.accounts)

    # Load contract ABI and address
    print("Current working directory:", os.getcwd())
    with open('./blockchain-project/build/contracts/FederatedLearning.json') as f:
        contract_json = json.load(f)
    contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=contract_json['abi'])

    # Initialize IPFS
    ipfs_manager = IPFSManager()

    # Initialize clients and validators
    num_clients = min(config.NUM_CLIENTS, len(w3.eth.accounts))
    clients = [ClientNode(i, w3) for i in range(num_clients)]
    available_accounts = len(w3.eth.accounts) - config.NUM_CLIENTS
    validators = [ValidatorNode(i, w3) for i in range(min(config.NUM_VALIDATORS, available_accounts))]

    # Initialize consensus mechanism
    consensus = SnowballConsensus(config.SNOWBALL_K, config.SNOWBALL_ALPHA, config.SNOWBALL_BETA)

    # Initialize the global model
    initial_model_weights = [np.array([0.0]), np.array([0.0])]  # Replace with your actual model structure
    aggregator = GlobalModelAggregator(initial_model_weights)   

    for round in range(config.NUM_ROUNDS):
        print(f"Round {round + 1}:")
        
        # Local training and collecting updates
        updates = []
        for client in clients:
            update = client.train_local_model()
            
            # Ensure the update is a list of NumPy arrays
            if isinstance(update, list):
                # Convert to numpy arrays, ensuring all have the same shape
                update = [np.array(u) for u in update]
                
                # Check if all updates are the same shape
                if len(set(map(np.shape, update))) != 1:
                    raise ValueError(f"Client {client.id} has inconsistent update shapes: {[np.shape(u) for u in update]}")
            else:
                update = np.array(update)

            print(f"Client {client.id} update shape: {np.shape(update)}")
            updates.append(update)

        # Check shapes of updates
        print(f"Collected updates shapes: {[np.shape(update) for update in updates]}")

        # Submit updates to IPFS and blockchain
        validated_updates = []
        for i, update in enumerate(updates):
            ipfs_hash = ipfs_manager.encrypt_and_upload(update)
            contract.functions.submitUpdate(ipfs_hash).transact({'from': clients[i].address})
            weight = clients[i].get_weight()  # Assuming a method to get weight for each client update
            validated_updates.append((update, weight))
        
        # Validation and consensus
        valid_updates = consensus.decide(validators)
        
        # Aggregate updates using the aggregator
        if valid_updates:
            aggregator.aggregate_updates(validated_updates)

        # Global model update
        global_model = aggregator.get_global_model()
        
        # Evaluate and print results
        accuracy = evaluate_model(global_model)
        print(f"Global model accuracy: {accuracy}")

    print("Federated Learning process completed.")

if __name__ == "__main__":
    main()
