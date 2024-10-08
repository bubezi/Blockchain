// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedLearning {
    struct ModelUpdate {
        address submitter;
        string ipfsHash;
        uint256 timestamp;
        bool isValidated;
    }

    ModelUpdate[] public modelUpdates;
    mapping(address => uint256) public validatorTrustScores;

    event UpdateSubmitted(address submitter, string ipfsHash);
    event UpdateValidated(address validator, uint256 updateIndex);

    function submitUpdate(string memory _ipfsHash) public {
        modelUpdates.push(ModelUpdate({
            submitter: msg.sender,
            ipfsHash: _ipfsHash,
            timestamp: block.timestamp,
            isValidated: false
        }));
        emit UpdateSubmitted(msg.sender, _ipfsHash);
    }

    function validateUpdate(uint256 _updateIndex) public {
        require(_updateIndex < modelUpdates.length, "Invalid update index");
        require(!modelUpdates[_updateIndex].isValidated, "Update already validated");
        
        modelUpdates[_updateIndex].isValidated = true;
        validatorTrustScores[msg.sender]++;
        
        emit UpdateValidated(msg.sender, _updateIndex);
    }

    function getTrustScore(address _validator) public view returns (uint256) {
        return validatorTrustScores[_validator];
    }
}
