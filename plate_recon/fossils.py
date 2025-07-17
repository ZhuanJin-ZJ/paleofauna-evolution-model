import pandas as pd
import pygplates
import requests
import os
from io import StringIO
from config import BASE_PATH, rotation_model

# === Static polygons for fossil partitioning ===
TOPOLOGY_PATH = os.path.join(BASE_PATH, 'shapes_static_polygons_Merdith_et_al.gpml')
topology_features = pygplates.FeatureCollection(TOPOLOGY_PATH)

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
from tectonics import get_plate_boundaries  # so you can access topologies

def reconstruct_fossil_locations(fossil_df, rotation_model, reconstruction_time, window=5):
    # Step 1: Filter fossils
    filtered_df = fossil_df[
        (fossil_df['early_age'] >= reconstruction_time - window) &
        (fossil_df['late_age'] <= reconstruction_time + window)
    ]

    print(f"🦴 Filtered fossil count at {reconstruction_time} ± {window} Ma: {len(filtered_df)}")

    # Step 2: Convert to Point features
    fossil_features = []
    for _, row in filtered_df.iterrows():
        point = pygplates.PointOnSphere(float(row['lat']), float(row['lng']))
        feature = pygplates.Feature()
        feature.set_geometry(point)
        fossil_features.append(feature)

    # Step 3: Get plate topologies for partitioning
    topology_features = get_plate_boundaries(reconstruction_time)

    # Step 4: Partition fossils into plates
    partitioned_fossils = pygplates.partition_into_plates(
        topology_features,  # partitioning_features
        rotation_model,     # rotation_model
        fossil_features,    # features_to_partition
        reconstruction_time=reconstruction_time
        )

    # Step 5: Reconstruct the partitioned fossils
    rotated_features = []
    pygplates.reconstruct(partitioned_fossils, rotation_model, rotated_features, reconstruction_time)

    # Step 6: Extract rotated coordinates
    reconstructed = []
    for original, rotated in zip(partitioned_fossils, rotated_features):
        try:
            reconstructed_geometry = rotated.get_reconstructed_geometry()
            original_geometry = original.get_geometry()
    
#            # 🧪 INSERT THESE PRINTS FOR DEBUGGING
#            print("📍 Original (present-day) fossil:", original_geometry.to_lat_lon())
#            print("🧭 Reconstructed fossil:", reconstructed_geometry.to_lat_lon())
    
            lat, lon = reconstructed_geometry.to_lat_lon()
            reconstructed.append({
                'recon_lat': lat,
                'recon_lon': lon,
                'original_lat': original_geometry.to_lat_lon()[0],
                'original_lon': original_geometry.to_lat_lon()[1],
                'plate_id': original.get_reconstruction_plate_id(),
                'age': reconstruction_time
            })
        except Exception as e:
            print(f"❌ Could not extract geometry: {e}")

    return reconstructed
