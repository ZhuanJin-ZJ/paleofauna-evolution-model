import pandas as pd
import requests
from io import StringIO

#To align argument names with .csv column names from PBDB, across all functions. The mismatch is likely filtering out the fossils.

def fetch_fossil_data(query_name='Theropoda', limit=None):
    base_url = "https://paleobiodb.org/data1.2/occs/list.csv"
    params = {
        'base_name': query_name,
        'show': 'coords,time,phylo',
        'limit': limit or 100000
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        raise Exception(f"PBDB request failed: {response.status_code}")

    df = pd.read_csv(StringIO(response.text))
    print(f"📥 Fetched {len(df)} fossil rows from PBDB before filtering.")

    # Drop fossils without coordinates or age data
    df = df.dropna(subset=['lng', 'lat', 'max_ma', 'min_ma'])
    df = df.rename(columns={'max_ma': 'early_age', 'min_ma': 'late_age'})
    df['midpoint_ma'] = (df['early_age'] + df['late_age']) / 2
    print(f"🧹 Remaining after dropna and renaming: {len(df)}")

    # Sanity check for empty result
    if df.empty:
        print(f"⚠️ Warning: No fossils found for query '{query_name}'.")

    return df


def fetch_and_cache_fossils(csv_path='data/theropods.csv', query_name='Theropoda'):
    try:
        df = pd.read_csv(csv_path)
        print("✅ Loaded fossils from cache.")
    except FileNotFoundError:
        df = fetch_fossil_data(query_name)
        df.to_csv(csv_path, index=False)
        print("⬇️ Fetched fossils from PBDB and cached locally.")
    return df

def reconstruct_fossil_locations(fossil_df, rotation_model, reconstruction_time, window=5):
    filtered_df = fossil_df[
        (fossil_df['early_age'] >= reconstruction_time - window) &
        (fossil_df['late_age'] <= reconstruction_time + window)
    ]

    print(f"🦴 Filtered fossil count at {reconstruction_time} ±{window} Ma: {len(filtered_df)}")

    reconstructed = []

    for _, row in filtered_df.iterrows():
        point = pygplates.PointOnSphere(float(row['lat']), float(row['lng']))
        time = float(row['midpoint_ma'])
        try:
            recon_point = rotation_model.get_reconstructed_position(point, time)
            if recon_point:
                lat, lon = recon_point.to_lat_lon()
                reconstructed.append({
                    'recon_lat': lat,
                    'recon_lon': lon,
                    'taxon': row.get('accepted_name') or row.get('genus') or 'Unknown',
                    'taxonomy': {
                        'phylum': row.get('phylum'),
                        'class': row.get('class'),
                        'order': row.get('order'),
                        'family': row.get('family'),
                        'genus': row.get('genus'),
                        'accepted_name': row.get('accepted_name'),
                    },
                    'original_lat': row['lat'],
                    'original_lon': row['lng'],
                    'age': time
                })
        except Exception as e:
            print(f"❌ Failed to reconstruct point at {time} Ma: {e}")

    return reconstructed


