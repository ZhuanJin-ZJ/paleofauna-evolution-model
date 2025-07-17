import pygplates
import os
from config import BASE_PATH, rotation_model  # ⬅️ import shared config

COASTLINES_PATH = os.path.join(BASE_PATH, 'COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml')
coastline_features = pygplates.FeatureCollection(COASTLINES_PATH)

def get_plate_boundaries(reconstruction_time):
    if reconstruction_time > 410:
        paths = [
            os.path.join(BASE_PATH, '1000-410-Convergence.gpml'),
            os.path.join(BASE_PATH, '1000-410-Divergence.gpml'),
            os.path.join(BASE_PATH, '1000-410-Transforms.gpml'),
            os.path.join(BASE_PATH, '1000-410-Topologies.gpml')
        ]
    elif 250 < reconstruction_time <= 410:
        paths = [os.path.join(BASE_PATH, '410-250_plate_boundaries.gpml')]
    else:
        paths = [os.path.join(BASE_PATH, '250-0_plate_boundaries.gpml')]

    features = []
    for path in paths:
        features += pygplates.FeatureCollection(path)
        
#    # 🔎 Insert test here
#    print(f"🧱 Loaded {len(features)} topology features")

#    has_polygons = 0
#    has_plate_ids = 0

#    for f in features:
#        geom = f.get_geometry()
#        if geom and hasattr(geom, 'to_lat_lon_list'):
#            has_polygons += 1
#        if f.get_reconstruction_plate_id() is not None:
#            has_plate_ids += 1

#    print(f"🧩 Features with polygons: {has_polygons}")
#    print(f"🧭 Features with plate IDs: {has_plate_ids}")
    
    return features

def reconstruct_features(features, time):
    reconstructed = []
    pygplates.reconstruct(features, rotation_model, reconstructed, time)
    return reconstructed

def reconstruct_coastlines(time):
    reconstructed = []
    pygplates.reconstruct(coastline_features, rotation_model, reconstructed, time)
    return reconstructed