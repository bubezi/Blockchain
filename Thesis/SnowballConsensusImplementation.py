import random

class SnowballConsensus:
    def __init__(self, k, alpha, beta):
        self.k = k  # Number of validators to query each round
        self.alpha = alpha  # Threshold for changing preference
        self.beta = beta  # Threshold for termination
        self.preference = None
        self.last_preference = None
        self.confidence = 0

    def query_validators(self, validators):
        sample = random.sample(validators, min(self.k, len(validators)))
        return [validator.get_preference() for validator in sample]

    def decide(self, validators):
        while self.confidence < self.beta:
            votes = self.query_validators(validators)
            count = sum(votes)
            
            if count >= self.alpha:
                if self.preference != 1:
                    self.confidence = 0
                self.preference = 1
            elif len(votes) - count >= self.alpha:
                if self.preference != 0:
                    self.confidence = 0
                self.preference = 0
            else:
                self.preference = self.last_preference
            
            if self.preference == self.last_preference:
                self.confidence += 1
            else:
                self.confidence = 0
            
            self.last_preference = self.preference
        
        return self.preference

# Usage
# snowball = SnowballConsensus(k=10, alpha=6, beta=20)
# decision = snowball.decide(validators)  # validators is a list of Validator objects
