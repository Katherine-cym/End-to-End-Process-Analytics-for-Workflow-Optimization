import pandas as pd
import numpy as np
from scipy.stats import entropy

class TemporalHeuristics:
    @staticmethod
    def calculate_shannon_entropy(series):
        """Calculates Shannon Entropy to determine if a date column is actively flowing."""
        value_counts = series.value_counts(normalize=True)
        return entropy(value_counts, base=2)

    @classmethod
    def identify_temporal_anchors(cls, df, threshold=2.0):
        print("\n[Phase 1] Identifying Temporal Anchors...")
        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns
        
        valid_anchors = []
        for col in datetime_cols:
            ent = cls.calculate_shannon_entropy(df[col].dt.date)
            print(f" - Column '{col}' Entropy: {ent:.2f}")
            if ent > threshold:
                valid_anchors.append(col)
                
        return valid_anchors