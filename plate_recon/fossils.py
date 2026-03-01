# Copyright (C) 2026 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import pandas as pd
import pygplates
import requests
import os
from io import StringIO
from config import BASE_PATH, rotation_model
from utils import log 

# === Static polygons for fossil partitioning ===
TOPOLOGY_PATH = os.path.join(BASE_PATH, 'shapes_static_polygons_Merdith_et_al.gpml')
topology_features = pygplates.FeatureCollection(TOPOLOGY_PATH)

# === FETCH ===
def fetch_fossils(query_name='Tyrannosaurus rex', limit=4):
    url = "https://paleobiodb.org/data1.2/occs/list.csv"
    params = {
        'base_name': query_name,
        'show': 'coords,time,phylo',
        'limit': limit
    }
    response = requests.get(url, params=params)
    df = pd.read_csv(StringIO(response.text))
    log(f"✅ Raw fossils downloaded: {len(df)}")

    df = df.dropna(subset=['lng', 'lat', 'max_ma', 'min_ma'])
    df = df.rename(columns={'max_ma': 'early_age', 'min_ma': 'late_age'})
    
    # Strict filtering (optional)
    df = df[df['accepted_name'] == 'Tyrannosaurus rex']
    return df

_cached_df = None  # Cache placeholder

def fetch_and_cache_fossils(csv_path='data/theropods.csv', query_name='Tyrannosaurus rex', force_refresh=False):
    global _cached_df

    if not force_refresh and _cached_df is not None:
        log("✅ Loaded fossils from in-memory cache.")
        return _cached_df

    if not force_refresh:
        try:
            df = pd.read_csv(csv_path)
            log("✅ Loaded fossils from disk cache.")
        except FileNotFoundError:
            df = fetch_fossils(query_name)
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            df.to_csv(csv_path, index=False)
            log("⬇️ Fetched fossils from PBDB and cached locally.")
    else:
        if os.path.exists(csv_path):
            os.remove(csv_path)
            log("🗑️ Deleted existing fossil cache file.")
        
        df = fetch_fossils(query_name)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        log("🔁 Force-refreshed fossil data and updated cache.")

    _cached_df = df
    return df

def clear_fossil_cache(csv_path='data/theropods.csv'):
    global _cached_df
    _cached_df = None
    if os.path.exists(csv_path):
        os.remove(csv_path)
        log("🧨 Fully cleared fossil cache from disk and memory.")

# === RECONSTRUCT ===
from tectonics import get_plate_boundaries  # to access topologies

def reconstruct_fossil_locations(fossil_df, rotation_model, reconstruction_time):
    ### Reconstruct fossils that are 'alive' at the given reconstruction_time.
    
    # A fossil is considered "alive" if:
    #    late_age <= reconstruction_time <= early_age
    #    where:
    #    - early_age = oldest known occurrence of the species (max_ma)
    #    - late_age  = youngest known occurrence (min_ma)

    # Step 1: Filter fossils
    filtered_df = fossil_df[
        (fossil_df['early_age'] >= reconstruction_time) #&
#        (fossil_df['late_age'] <= reconstruction_time)
    ]

    log(f"🦴 Filtered fossil count at {reconstruction_time} Ma: {len(filtered_df)}")

    # Step 2: Convert to Point features
    fossil_features = []
    fossil_metadata = []
    for _, row in filtered_df.iterrows():
        point = pygplates.PointOnSphere(float(row['lat']), float(row['lng']))
        feature = pygplates.Feature()
        feature.set_geometry(point)
        if "genus" in row:
            feature.set_name(str(row["genus"]))
        fossil_features.append(feature)
        fossil_metadata.append(row.to_dict()) # Save full row metadata

    # Step 3: Get plate topologies for partitioning
    topology_features = get_plate_boundaries(reconstruction_time)

    # Step 4: Partition fossils into plates
    partitioned_fossils = pygplates.partition_into_plates(
        topology_features,  # partitioning_features
        rotation_model,     # rotation_model
        fossil_features,    # features_to_partition
        reconstruction_time=0
        )

    # Step 5: Reconstruct the partitioned fossils
    rotated_features = []
    pygplates.reconstruct(partitioned_fossils, rotation_model, rotated_features, reconstruction_time)

    # Step 6: Extract rotated coordinates
    reconstructed = []
    for meta, original, rotated in zip(fossil_metadata, partitioned_fossils, rotated_features):
        try:
            reconstructed_geometry = rotated.get_reconstructed_geometry()
            original_geometry = original.get_geometry()
    
#            # 🧪 INSERT THESE PRINTS FOR DEBUGGING
#            print("📍 Original (present-day) fossil:", original_geometry.to_lat_lon())
#            print("🧭 Reconstructed fossil:", reconstructed_geometry.to_lat_lon())
    
            lat, lon = reconstructed_geometry.to_lat_lon()

            # Build dict with coordinates + metadata
            fossil_data = {
                'recon_lat': lat,
                'recon_lon': lon,
                'original_lat': original_geometry.to_lat_lon()[0],
                'original_lon': original_geometry.to_lat_lon()[1],
                'plate_id': original.get_reconstruction_plate_id(),
                'age': reconstruction_time
            }
            # Merge metadata dictionary back in
            fossil_data.update(meta)
            reconstructed.append(fossil_data)
            
        except Exception as e:
            log(f"❌ Could not extract geometry: {e}")

    return reconstructed
