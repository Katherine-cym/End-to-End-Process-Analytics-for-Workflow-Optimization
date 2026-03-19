import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier

class ContextExtractor:
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.rf = RandomForestClassifier(n_estimators=100, random_state=42)

    def fit_predict(self, df, pk_col='CADIS_ID', table_col='TABLE_NAME', context_cols=['ASSET_CLASS', 'AMOUNT']):
        print("\n[Phase 2] Running Clustering & Context Extraction...")
        
        # 1. Build Traversal Matrix
        path_matrix = df.groupby([pk_col, table_col]).size().unstack(fill_value=0).clip(upper=1)
        
        # 2. Cluster Paths
        path_matrix['CLUSTER'] = self.kmeans.fit_predict(path_matrix)
        print(f" - Grouped {len(path_matrix)} entities into {self.n_clusters} behavioral clusters.")
        
        # 3. Supervised Context Extraction
        context_df = df.groupby(pk_col).agg({col: 'first' if df[col].dtype == 'O' else 'mean' for col in context_cols})
        merged = path_matrix.join(context_df)
        
        X = pd.get_dummies(merged[context_cols], drop_first=True)
        y = merged['CLUSTER']
        
        self.rf.fit(X, y)
        importances = pd.Series(self.rf.feature_importances_, index=X.columns).sort_values(ascending=False)
        
        print(" - Feature Importances (What drives the processing route?):")
        print(importances.to_string())
        
        return merged