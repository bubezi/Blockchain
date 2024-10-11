from scipy.spatial.distance import cosine
import config
import tensorflow as tf


class ValidatorNode:
    def __init__(self, id, w3):
        self.id = id
        self.w3 = w3
        self.address = w3.eth.accounts[id + config.NUM_CLIENTS]
        self.trust_scores = {}
        self.latest_model_update = None  # To store the latest validated model update

    def validate_update(self, client_address, model_update):
        # Simple validation check (replace with more sophisticated checks)
        if any(tf.math.is_nan(w).numpy().any() for w in model_update):
            return False
        # If the update is valid, store it
        self.latest_model_update = model_update
        return True

    def get_preference(self):
        # Simplified preference (replace with actual logic)
        return True
    
    def get_update(self):
        # Return the latest validated model update
        return self.latest_model_update
