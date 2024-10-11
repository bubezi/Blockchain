import random
import numpy as np

class SnowballConsensus:
    def __init__(self, k, alpha, beta):
        self.k = k
        self.alpha = alpha
        self.beta = beta
        self.preference = None
        self.last_preference = None
        self.confidence = 0

    def query_validators(self, validators):
            sample = np.random.choice(validators, self.k, replace=False)
            votes_and_updates = []
            for validator in sample:
                preference = validator.get_preference()
                update = validator.get_update()
                if update is not None:  # Ensure update is valid
                    votes_and_updates.append((preference, update))
            return votes_and_updates

    def decide(self, validators):
        valid_updates = []
        while self.confidence < self.beta:
            votes_and_updates = self.query_validators(validators)
            votes = [vote for vote, _ in votes_and_updates]
            count = sum(votes)
            
            if count >= self.alpha:
                if self.preference != 1:
                    self.confidence = 0
                self.preference = 1
                valid_updates.extend([update for vote, update in votes_and_updates if vote == 1])
            elif len(votes) - count >= self.alpha:
                if self.preference != 0:
                    self.confidence = 0
                self.preference = 0
                valid_updates.extend([update for vote, update in votes_and_updates if vote == 0])
            else:
                self.preference = self.last_preference
            
            if self.preference == self.last_preference:
                self.confidence += 1
            else:
                self.confidence = 0
            
            self.last_preference = self.preference
        
        # Here you could also include weights if needed. For now, just return updates.
        # Assuming a weight of 1 for simplicity; adjust as needed based on your logic.
        return [(update, 1) for update in valid_updates]
    