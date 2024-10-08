from sklearn.neighbors import LocalOutlierFactor
import numpy as np

class NoveltyDetector:
    def __init__(self, n_neighbors=20, contamination=0.1):
        self.lof = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=contamination, novelty=True)
        self.is_fit = False

    def fit(self, X):
        self.lof.fit(X)
        self.is_fit = True

    def detect_outliers(self, X):
        if not self.is_fit:
            raise ValueError("Model must be fit before detecting outliers")
        
        # Negative scores indicate outliers
        scores = self.lof.score_samples(X)
        return scores < self.lof.offset_

# Usage
detector = NoveltyDetector()
normal_updates = np.random.randn(100, 10)  # 100 normal updates with 10 features each
detector.fit(normal_updates)

new_updates = np.random.randn(10, 10)  # 10 new updates to check
outliers = detector.detect_outliers(new_updates)
print(f"Detected {sum(outliers)} potential anomalies")
