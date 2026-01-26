import pandas as pd
from sqlalchemy import create_engine

# Create database connection
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

print("Loading green taxi data...")
df = pd.read_parquet('data/green_tripdata_2025-11.parquet')
df.to_sql('green_taxi_trips', engine, if_exists='replace', index=False)
print(f"Loaded {len(df)} green taxi trips")

print("Loading taxi zones...")
zones = pd.read_csv('data/taxi_zone_lookup.csv')
zones.to_sql('taxi_zones', engine, if_exists='replace', index=False)
print(f"Loaded {len(zones)} taxi zones")

print("Done!")
