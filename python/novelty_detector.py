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
        
        scores = self.lof.score_samples(X)
        return scores < self.lof.offset_