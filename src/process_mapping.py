import pandas as pd
#Markov Chain
class ProcessMapper:
    @staticmethod
    def generate_transition_matrix(df, pk_col='CADIS_ID', table_col='TABLE_NAME', time_col='SYSTEM_TIMESTAMP'):
        print("\n[Phase 3] Generating Markov Sequence Maps & Latency...")
        df = df.sort_values(by=[pk_col, time_col])
        
        df['NEXT_TABLE'] = df.groupby(pk_col)[table_col].shift(-1)
        df['TIME_DELTA_SEC'] = df.groupby(pk_col)[time_col].diff().shift(-1).dt.total_seconds()
        transitions = df.dropna(subset=['NEXT_TABLE'])
        
        # Markov Probabilities
        trans_counts = transitions.groupby([table_col, 'NEXT_TABLE']).size().unstack(fill_value=0)
        trans_probs = trans_counts.div(trans_counts.sum(axis=1), axis=0).round(3)
        
        # Latency
        latency = transitions.groupby([table_col, 'NEXT_TABLE'])['TIME_DELTA_SEC'].agg(['median', 'max']).round(1)
        
        print("\nTransition Probabilities:")
        print(trans_probs.to_string())
        
        print("\nProcess Latency (Seconds):")
        print(latency.to_string())
        
        return trans_probs, latency