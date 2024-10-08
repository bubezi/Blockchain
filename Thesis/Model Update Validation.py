import numpy as np
from scipy.spatial.distance import cosine

class Validator:
    def __init__(self, global_model):
        self.global_model = global_model
        self.trust_scores = {}

    def validate_update(self, client_address, model_update):
        # Check for NaN or Inf values
        if np.any(np.isnan(model_update)) or np.any(np.isinf(model_update)):
            return False

        # Check cosine similarity with global model
        similarity = 1 - cosine(self.global_model.flatten(), model_update.flatten())
        if similarity < 0.8:  # Threshold can be adjusted
            return False

        # Update trust score
        self.trust_scores[client_address] = self.trust_scores.get(client_address, 0) + 1
        return True

# Usage
validator = Validator(global_model_weights)
is_valid = validator.validate_update(client_address, model_update)
