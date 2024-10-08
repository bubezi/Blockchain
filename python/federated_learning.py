import config
from client_node import ClientNode
from validator_node import ValidatorNode
from ipfs_manager import IPFSManager
from snowball_consensus import SnowballConsensus
from web3 import Web3
import json

def main():
    # Connect to Ethereum
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
    
    # Load contract ABI and address
    with open('build/contracts/FederatedLearning.json') as f:
        contract_json = json.load(f)
    contract = w3.eth.contract(address=config.CONTRACT_ADDRESS, abi=contract_json['abi'])
    
    # Initialize IPFS
    ipfs_manager = IPFSManager()
    
    # Initialize clients and validators
    clients = [ClientNode(i) for i in range(config.NUM_CLIENTS)]
    validators = [ValidatorNode(i) for i in range(config.NUM_VALIDATORS)]
    
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
        global_model = aggregate_updates(valid_updates)
        
        # Evaluate and print results
        accuracy = evaluate_model(global_model)
        print(f"Global model accuracy: {accuracy}")
    
    print("Federated Learning process completed.")

if __name__ == "__main__":
    main()