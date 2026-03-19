# main.py
from src.db_connector import EDMDataFetcher
from src.heuristics import TemporalHeuristics
from src.models import ContextExtractor
from src.process_mapping import ProcessMapper

def main():
    # 1. Load Data
    fetcher = EDMDataFetcher(use_mock=True)
    df = fetcher.fetch_data(num_records=1000)
    
    # Optional: Save raw data to mimic actual repository flow
    df.to_csv('data/raw/edm_extract.csv', index=False)
    
    # 2. Heuristics
    anchors = TemporalHeuristics.identify_temporal_anchors(df)
    time_col = anchors[0] if anchors else 'SYSTEM_TIMESTAMP'
    
    # 3. Clustering & Context
    extractor = ContextExtractor()
    clustered_data = extractor.fit_predict(df)
    clustered_data.to_csv('data/event_tables/clustered_paths.csv')
    
    # 4. Process Mapping
    mapper = ProcessMapper()
    trans_probs, latency = mapper.generate_transition_matrix(df, time_col=time_col)
    
    # 5. Save Outputs
    trans_probs.to_csv('output/transition_matrix.csv')
    latency.to_csv('output/latency_metrics.csv')

if __name__ == "__main__":
    main()