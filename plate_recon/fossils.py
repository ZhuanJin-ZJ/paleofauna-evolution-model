import pandas as pd
import pygplates
import requests
import os
from io import StringIO

# === FETCH ===
def fetch_fossils(query_name='Theropoda', limit=10000):
    url = "https://paleobiodb.org/data1.2/occs/list.csv"
    params = {
        'base_name': query_name,
        'show': 'coords,time,phylo',
        'limit': limit
    }
    response = requests.get(url, params=params)
    df = pd.read_csv(StringIO(response.text))
    print(f"✅ Raw fossils downloaded: {len(df)}")

    df = df.dropna(subset=['lng', 'lat', 'max_ma', 'min_ma'])
    df = df.rename(columns={'max_ma': 'early_age', 'min_ma': 'late_age'})
    df['midpoint_ma'] = (df['early_age'] + df['late_age']) / 2

    return df


_cached_df = None  # Cache placeholder

def fetch_and_cache_fossils(csv_path='data/theropods.csv', query_name='Theropoda', force_refresh=False):
    global _cached_df

    if not force_refresh and _cached_df is not None:
        print("✅ Loaded fossils from in-memory cache.")
        return _cached_df

    if not force_refresh:
        try:
            df = pd.read_csv(csv_path)
            print("✅ Loaded fossils from disk cache.")
        except FileNotFoundError:
            df = fetch_fossils(query_name)
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            print("⬇️ Fetched fossils from PBDB and cached locally.")
    else:
        if os.path.exists(csv_path):
            os.remove(csv_path)
            print("🗑️ Deleted existing fossil cache file.")
        
        df = fetch_fossils(query_name)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        print("🔁 Force-refreshed fossil data and updated cache.")

    _cached_df = df
    return df

def clear_fossil_cache(csv_path='data/theropods.csv'):
    global _cached_df
    _cached_df = None
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print("🧨 Fully cleared fossil cache from disk and memory.")
        

# === RECONSTRUCT ===
def reconstruct_fossil_locations(fossil_df, rotation_model, reconstruction_time, window=5):
    filtered_df = fossil_df[
        (fossil_df['early_age'] >= reconstruction_time - window) &
        (fossil_df['late_age'] <= reconstruction_time + window)
    ]

    print(f"🦴 Filtered fossil count at {reconstruction_time} ± {window} Ma: {len(filtered_df)}")

    reconstructed = []

    for _, row in filtered_df.iterrows():
        point = pygplates.PointOnSphere(float(row['lat']), float(row['lng']))
        try:
            feature = pygplates.Feature()
            feature.set_geometry(point)

            reconstructed_features = []
            pygplates.reconstruct([feature], rotation_model, reconstructed_features, float(row['midpoint_ma']))

            if reconstructed_features:
                lat, lon = reconstructed_features[0].get_reconstructed_geometry().to_lat_lon()
                reconstructed.append({
                    'recon_lat': lat,
                    'recon_lon': lon,
                    'original_lat': row['lat'],
                    'original_lon': row['lng'],
                    'age': row['midpoint_ma']
                })
        except Exception as e:
            print(f"❌ Failed to reconstruct point at {row['midpoint_ma']} Ma: {e}")

    return reconstructed
