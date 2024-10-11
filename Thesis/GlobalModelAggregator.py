import numpy as np

class GlobalModelAggregator:
    def __init__(self, initial_model):
        self.global_model = initial_model

    def aggregate_updates(self, validated_updates):
        aggregated_update = [np.zeros_like(layer) for layer in self.global_model]
        total_weight = 0

        for update, weight in validated_updates:
            total_weight += weight
            for i, layer in enumerate(update):
                aggregated_update[i] += layer * weight

        for i in range(len(aggregated_update)):
            aggregated_update[i] /= total_weight
            self.global_model[i] += aggregated_update[i]

    def get_global_model(self):
        return self.global_model

# Usage
# aggregator = GlobalModelAggregator(initial_model_weights)
# validated_updates = [(update1, weight1), (update2, weight2), ...]  # List of (update, weight) tuples
# aggregator.aggregate_updates(validated_updates)
# updated_global_model = aggregator.get_global_model()
