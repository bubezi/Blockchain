// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FederatedLearning {
    struct ModelUpdate {
        address submitter;
        string ipfsHash;
        uint256 timestamp;
        bool isValidated;
        uint256 round;
    }

    ModelUpdate[] public modelUpdates;
    mapping(address => uint256) public validatorTrustScores;
    uint256 public currentRound;
    uint256 public constant MINIMUM_TRUST_SCORE = 5;

    event UpdateSubmitted(address submitter, string ipfsHash, uint256 round);
    event UpdateValidated(address validator, uint256 updateIndex);
    event RoundCompleted(uint256 round);

    function submitUpdate(string memory _ipfsHash) public {
        modelUpdates.push(ModelUpdate({
            submitter: msg.sender,
            ipfsHash: _ipfsHash,
            timestamp: block.timestamp,
            isValidated: false,
            round: currentRound
        }));
        emit UpdateSubmitted(msg.sender, _ipfsHash, currentRound);
    }

    function validateUpdate(uint256 _updateIndex) public {
        require(_updateIndex < modelUpdates.length, "Invalid update index");
        require(!modelUpdates[_updateIndex].isValidated, "Update already validated");
        require(validatorTrustScores[msg.sender] >= MINIMUM_TRUST_SCORE, "Insufficient trust score");
        
        modelUpdates[_updateIndex].isValidated = true;
        validatorTrustScores[msg.sender]++;
        
        emit UpdateValidated(msg.sender, _updateIndex);
    }

    function completeRound() public {
        // In a real implementation, this would be called by a designated aggregator
        // after performing the federated averaging of validated updates
        currentRound++;
        emit RoundCompleted(currentRound);
    }

    function getTrustScore(address _validator) public view returns (uint256) {
        return validatorTrustScores[_validator];
    }
}
