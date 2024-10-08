from scipy.spatial.distance import cosine

class ValidatorNode:
    def __init__(self, id, w3):
        self.id = id
        self.w3 = w3
        self.address = w3.eth.accounts[id + config.NUM_CLIENTS]
        self.trust_scores = {}

    def validate_update(self, client_address, model_update):
        # Simple validation check (replace with more sophisticated checks)
        if any(tf.math.is_nan(w).numpy().any() for w in model_update):
            return False
        return True

    def get_preference(self):
        # Simplified preference (replace with actual logic)
        return True