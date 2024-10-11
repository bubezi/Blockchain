import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
import config
from client_node import ClientNode
from validator_node import ValidatorNode
from ipfs_manager import IPFSManager
from snowball_consensus import SnowballConsensus
from web3 import Web3
import json
from Thesis.GlobalModelAggregator import GlobalModelAggregator  # Adjusted import


def initialize_model():
    # Example: a simple model with 2 layers
    layer1_weights = np.random.rand(10, 5)  # 10 neurons in layer 1, 5 inputs
    layer2_weights = np.random.rand(5, 1)    # 5 neurons in layer 2, 1 output
    return [layer1_weights, layer2_weights]

initial_model = initialize_model()
aggregator = GlobalModelAggregator(initial_model)

def evaluate_model(global_model):
    # Example evaluation logic
    test_data = np.random.rand(10, 5)  # Example test data
    test_labels = np.random.randint(0, 2, size=(10, 1))  # Example binary labels
    
    # Assuming the model is a simple linear combination of inputs and weights
    predictions = np.dot(test_data, global_model[0])  # Modify as needed based on your model structure
    predicted_classes = np.argmax(predictions, axis=1)  # Get predicted class indices
    accuracy = np.mean(predicted_classes == test_labels.flatten())  # Calculate accuracy
    return accuracy

def main():
    # Connect to Ethereum
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    
    # Load contract ABI and address
    with open('blockchain-project/build/contracts/FederatedLearning.json') as f:
        contract_json = json.load(f)
    contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=contract_json['abi'])
    
    # Initialize IPFS
    ipfs_manager = IPFSManager()
    
    # Initialize clients and validators
    clients = [ClientNode(i, w3) for i in range(config.NUM_CLIENTS)]
    validators = [ValidatorNode(i, w3) for i in range(config.NUM_VALIDATORS)]
    
    # Initialize consensus mechanism
    consensus = SnowballConsensus(config.SNOWBALL_K, config.SNOWBALL_ALPHA, config.SNOWBALL_BETA)
    
    for round in range(config.NUM_ROUNDS):
        print(f"Round {round + 1}:")
        
        # Local training
        updates = [client.train_local_model() for client in clients]
        
        # Submit updates to IPFS and blockchain
        for i, update in enumerate(updates):
            ipfs_hash = ipfs_manager.encrypt_and_upload(update)
            contract.functions.submitUpdate(ipfs_hash).transact({'from': clients[i].address})
        
        # Validation and consensus
        valid_updates = consensus.decide(validators)
        
        # Global model update
        if valid_updates:
            global_model = aggregator.aggregate_updates(valid_updates)  # Use GlobalModelAggregator
        else:
            print("No valid updates received, skipping global model update.")
            continue  # Skip to the next round if no valid updates

        # Evaluate and print results
        accuracy = evaluate_model(global_model)
        print(f"Global model accuracy: {accuracy}")

    print("Federated Learning process completed.")

if __name__ == "__main__":
    main()
