# Copyright (C) 2026 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import pygplates
import os
import numpy as np
from config import BASE_PATH, rotation_model  # ⬅️ import shared config

COB_PATH = os.path.join(BASE_PATH, 'COB_polygons_and_coastlines_combined_1000_0_Merdith_etal.gpml') # Continent-Ocean Boundary
cob_features = pygplates.FeatureCollection(COB_PATH)

LANDMASK_CACHE = "cache/landmask"
os.makedirs(LANDMASK_CACHE, exist_ok=True)

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

def load_raw_land_polygons():
    polys = []
    for feat in cob_features:
        geom = feat.get_geometry()
        if geom is None:
            continue

        gname = geom.__class__.__name__

        # Match PolygonOnSphere, MultiPolygonOnSphere, etc.
        if "Polygon" in gname:
            polys.append(feat)

    return polys

def reconstruct_features(features, time):
    reconstructed = []
    pygplates.reconstruct(features, rotation_model, reconstructed, time)
    return reconstructed

def reconstruct_coastlines(time):
    return reconstruct_features(cob_features, time)

def reconstruct_polygons(time):
    """
    Reconstruct only polygon features (landmasses) to a given time.
    Returns a list of reconstructed feature geometries.
    """
    raw_polygons = load_raw_land_polygons()
    reconstructed = []
    pygplates.reconstruct(raw_polygons, rotation_model, reconstructed, time)

    polygons = []
    for feat in reconstructed:
        geom = feat.get_reconstructed_geometry()
        if isinstance(geom, pygplates.PolygonOnSphere):
            polygons.append(geom)
            
    return polygons

# --------------------------------------------------
# RASTERISATION FUNCTION
# --------------------------------------------------

def rasterise_landmask(
    reconstructed_polygons,
    time_ma,
    resolution_deg=1.0
):
    """
    Spherical landmask rasterisation using point-in-polygon tests.
    Returns:
        landmask : 2D boolean array (lat, lon)
        lats     : 1D latitude array
        lons     : 1D longitude array
    """

    cache_file = (
        f"{LANDMASK_CACHE}/"
        f"landmask_{int(time_ma)}Ma_{resolution_deg:.2f}deg.npz"
    )

    # --------------------
    # Load from cache
    # --------------------
    if os.path.exists(cache_file):
        data = np.load(cache_file)
        return data["mask"], data["lats"], data["lons"]

    # --------------------
    # Raster grid
    # --------------------
    lats = np.arange(-90, 90 + resolution_deg, resolution_deg)
    lons = np.arange(-180, 180 + resolution_deg, resolution_deg)

    lon_grid, lat_grid = np.meshgrid(lons, lats)

    # Flatten grid
    flat_lats = lat_grid.ravel()
    flat_lons = lon_grid.ravel()

    landmask_flat = np.zeros(flat_lats.shape, dtype=bool)

    # --------------------
    # Get land polygons
    # --------------------
    polygons = reconstructed_polygons

    # --------------------
    # Bounding-box accelerated rasterisation
    # --------------------

    for poly in polygons:

        coords = poly.to_lat_lon_list()
        if not coords:
            continue

        poly_lats, poly_lons = zip(*coords)

        min_lat = min(poly_lats)
        max_lat = max(poly_lats)
        min_lon = min(poly_lons)
        max_lon = max(poly_lons)

        # Handle dateline crossing
        crosses_dateline = (max_lon - min_lon) > 180

        # Vectorised candidate mask
        lat_mask = (flat_lats >= min_lat) & (flat_lats <= max_lat)

        if crosses_dateline:
            lon_mask = (flat_lons >= min_lon) | (flat_lons <= max_lon)
        else:
            lon_mask = (flat_lons >= min_lon) & (flat_lons <= max_lon)

        candidate_indices = np.where(lat_mask & lon_mask)[0]

        # Now only test candidates
        for idx in candidate_indices:

            if landmask_flat[idx]:
                continue

            point = pygplates.PointOnSphere(
                flat_lats[idx],
                flat_lons[idx]
            )

            if poly.is_point_in_polygon(point):
                landmask_flat[idx] = True

    # Reshape back
    landmask = landmask_flat.reshape(lat_grid.shape)

    # --------------------
    # Cache
    # --------------------
    np.savez_compressed(
        cache_file,
        mask=landmask,
        lats=lats,
        lons=lons
    )

    return landmask, lats, lons