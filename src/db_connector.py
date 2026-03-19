import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class EDMDataFetcher:
    def __init__(self, use_mock=True):
        self.use_mock = use_mock

    def fetch_data(self, num_records=1000):
        if self.use_mock:
            return self._generate_mock_data(num_records)
        else:
            # Placeholder for actual Snowflake sqlalchemy/connector logic
            raise NotImplementedError("Live Snowflake connection requires valid RSA keys.")

    def _generate_mock_data(self, num_records):
        print("Fetching data from EDM... (Mock Mode)")
        np.random.seed(42)
        data = []
        
        for i in range(num_records):
            cadis_id = f"PK_{i:04d}"
            asset_class = np.random.choice(['Equity', 'Option'], p=[0.7, 0.3])
            amount = np.random.uniform(1000, 50000)
            
            base_time = datetime.now() - timedelta(days=np.random.randint(1, 30))
            data.append([cadis_id, 'Table_A_Ingest', base_time, asset_class, amount])
            
            if asset_class == 'Equity': # STP Route
                t2 = base_time + timedelta(seconds=np.random.randint(1, 5))
                data.append([cadis_id, 'Table_B_Transform', t2, asset_class, amount])
                t3 = t2 + timedelta(seconds=np.random.randint(1, 5))
                data.append([cadis_id, 'Table_D_Warehouse', t3, asset_class, amount])
            else: # Exception Route
                t2 = base_time + timedelta(seconds=np.random.randint(300, 3600))
                data.append([cadis_id, 'Table_C_Exception', t2, asset_class, amount])
                t3 = t2 + timedelta(seconds=np.random.randint(10, 60))
                data.append([cadis_id, 'Table_D_Warehouse', t3, asset_class, amount])
                
        return pd.DataFrame(data, columns=['CADIS_ID', 'TABLE_NAME', 'SYSTEM_TIMESTAMP', 'ASSET_CLASS', 'AMOUNT'])