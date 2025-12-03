# Copyright (C) 2025 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pygplates
import os
import scipy.spatial
try:
    import pykdtree
except ImportError:
    pass
import cartopy.crs as ccrs
from config import rotation_model
from ipywidgets import IntSlider, VBox, Output
from IPython.display import display
from tectonics import get_plate_boundaries, reconstruct_features, reconstruct_coastlines
import importlib
import fossils
importlib.reload(fossils)
from utils import log

# Access functions via the module namespace to ensure you use the latest
fetch_and_cache_fossils = fossils.fetch_and_cache_fossils
reconstruct_fossil_locations = fossils.reconstruct_fossil_locations

# Load the T. rex image once
BASE_DIR   = os.path.dirname(os.path.dirname(__file__)) # Go up one level in the directory
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
T_REX_ICON = mpimg.imread(os.path.join(ASSETS_DIR, "t_rex.png"))


from cartopy import feature as cfeature
from shapely.geometry import Polygon
import numpy as np
import matplotlib.patches as Patch

def render_oceanmask(ax, color=(0.0, 0.2, 0.55)):
    """
    Paint global ocean using a PlateCarree polygon.
    Works for all projections including Robinson.
    """

    pc = ccrs.PlateCarree()

    # A global rectangle in lat/lon
    world_rect = Polygon([(-180, -90), (-180, 90), (180, 90), (180, -90)])

    ax.add_geometries(
        [world_rect],
        crs=pc,
        facecolor=color,
        edgecolor='none',
        zorder=-50
    )

def extract_polygon_loops(reconstructed_features):
    """
    Extract polygon or polyline loops from reconstructed coastlines.
    Compatible with all pygplates versions.
    Returns a list of loops, each loop = list of (lon, lat).
    """
    polygons = []

    for feature in reconstructed_features:
        geom = feature.get_reconstructed_geometry()
        if geom is None:
            continue

        # Try direct lat/lon extraction (works for most geom types)
        if hasattr(geom, 'to_lat_lon_list'):
            coords = geom.to_lat_lon_list()
            if len(coords) >= 3:
                polygons.append(coords)
            continue

        # Try accessing points directly (older PolygonOnSphere)
        if hasattr(geom, 'get_points'):
            pts = geom.get_points()
            coords = [(p.get_longitude(), p.get_latitude()) for p in pts]
            if len(coords) >= 3:
                polygons.append(coords)
            continue

        # Try general point sequence attribute (fallback)
        if hasattr(geom, 'points'):
            pts = geom.points
            coords = [(p.get_longitude(), p.get_latitude()) for p in pts]
            if len(coords) >= 3:
                polygons.append(coords)
            continue

        # If truly nothing works, skip
        # (very rare — only for non-spatial metadata)
        # print("⚠️ Skipped unknown geometry:", geom.__class__.__name__)
        pass

    return polygons

def render_landmask(ax, land_polygons, color='green', alpha=0.6, zorder=1):
    """
    Render filled landmasses using precomputed coastline polygons.
    
    land_polygons: list of polygons, where each polygon is a list of (lon, lat) pairs.
                   Example: [ [ (lon1,lat1), (lon2,lat2), ... ], [ ... ], ... ]

    ax: the Cartopy axes (already initialized with projection=ccrs.Robinson() or similar)
    """

    proj = ax.projection          # Same trick used in the T. rex icon code
    pc = ccrs.PlateCarree()       # Source coordinate system

    for poly in land_polygons:
        if len(poly) < 3:
            continue  # not enough points to fill

        # Extract lon/lat arrays
        lons = np.array([p[0] for p in poly])
        lats = np.array([p[1] for p in poly])

        # Project the vertices from PlateCarree → ax projection (Robinson)
        projected = proj.transform_points(pc, lons, lats)

        # projected is Nx3 array: columns = [x, y, z]
        xs = projected[:, 0]
        ys = projected[:, 1]

        # Fill polygon in projected coordinate space
        ax.fill(
            xs, ys,
            color=color,
            alpha=alpha,
            transform=proj,
            zorder=zorder
        )

def plot_reconstructed_features(ax, reconstructed_geometries, color_map):
    for feature in reconstructed_geometries:
        geom = feature.get_reconstructed_geometry()
        if hasattr(geom, 'to_lat_lon_list'):
            lat_lon_list = geom.to_lat_lon_list()
            if lat_lon_list:
                lats, lons = zip(*lat_lon_list)
                ax.plot(
                    lons, lats, '-', 
                    color=color_map.get(
                        'polygon' if 'Polygon' in geom.__class__.__name__ else 'polyline',
                        'black'
                    ),
                    transform=ccrs.Geodetic(), linewidth=0.5
                )
                
def plot_fossils(ax, fossil_data, size_deg=1.0, original=False):
    """
    If original=True  → draw grey dots
    If original=False → draw T. rex image icons
    """
    pc = ccrs.PlateCarree()
    proj = ax.projection # Robinson projection used in the figure

    for fossil in fossil_data:
        lat = fossil['original_lat'] if original else fossil['recon_lat']
        lon = fossil['original_lon'] if original else fossil['recon_lon']

        if original:
            # --- Present-day fossils: grey dots ---
            ax.plot(
                lon, lat, 'o',
                transform=ccrs.Geodetic(),
                color='gray',
                markersize=3,
                alpha=0.6,
                zorder=5
            )
        else:
            # --- Reconstructed fossils: image icons ---
            # Transform (lon, lat) into Robinson projected coordinates
            x, y = proj.transform_point(lon, lat, pc)

            # Size in projected units (rough guess: degrees → projection scale)
            d = size_deg * 10000

            ax.imshow(
                T_REX_ICON,
                extent=[x - d, x + d, y - d, y + d],
                transform=proj,   # NOT PlateCarree anymore
                origin="upper",
                alpha=1.0,
                zorder=10
            )

def plot_fossil_vectors(ax, fossil_data, color='red'):
    for fossil in fossil_data:
        orig_lat = fossil['original_lat']
        orig_lon = fossil['original_lon']
        recon_lat = fossil['recon_lat']
        recon_lon = fossil['recon_lon']

        ax.plot(
            [orig_lon, recon_lon], [orig_lat, recon_lat],
            transform=ccrs.Geodetic(), color=color,
            linewidth=0.7, alpha=0.7
        )

def draw_dynamic_legend(ax, active_layers):
    from matplotlib.lines import Line2D
    
    legend_elements = []
    if active_layers.get('reconstructed_fossils'):
        legend_elements.append(Line2D([0], [0], marker='o', color='darkgreen', label='Reconstructed Fossils', linestyle='None'))
    if active_layers.get('present_day_fossils'):
        legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Present-Day Fossils', linestyle='None'))
    if active_layers.get('vectors'):
        legend_elements.append(Line2D([0], [0], color='red', lw=1, label='Net Displacement Vectors'))
    if active_layers.get('coastlines'):
        legend_elements.append(Line2D([0], [0], color='saddlebrown', lw=1, label='Coastlines'))
    if active_layers.get('plate_boundaries'):
        legend_elements.append(Line2D([0], [0], color='blue', lw=1, label='Plate Boundaries'))

    ax.legend(handles=legend_elements, loc='lower right')

def plot_all(ax, time, export=False, outdir="exports"):
    print(f"⏳ Reconstructing for time: {time} Ma")
    ### SANITY CHECK FOR WHY IMAGES WERE NOT SHOWING
#    import numpy as np

#    print("Shape:", T_REX_ICON.shape)
#    print("Min/Max:", np.min(T_REX_ICON), np.max(T_REX_ICON))
#    print("Unique sample:", np.unique(T_REX_ICON.reshape(-1, T_REX_ICON.shape[-1])[:20], axis=0))

#    for lon, lat in [(0,0), (30,30), (-60,15)]:
#        x, y = ax.projection.transform_point(lon, lat, ccrs.PlateCarree())
#        d = 5 * 100000
#        ax.imshow(
#            T_REX_ICON,
#            extent=[x-d, x+d, y-d, y+d],
#            transform=ax.projection,
#            zorder=50
#        )
    
    features = get_plate_boundaries(time)
    reconstructed_boundaries = reconstruct_features(features, time)
    reconstructed_coastlines = reconstruct_coastlines(time)

    land_polygons = extract_polygon_loops(reconstructed_coastlines) # Extract polygon loops from coastlines

    render_oceanmask(ax) # Paint oceans first
    render_landmask(ax, land_polygons, color='green') # Paint landmasses

    plot_reconstructed_features(ax, reconstructed_boundaries, {'polygon': 'red', 'polyline': 'blue'})
    plot_reconstructed_features(ax, reconstructed_coastlines, {'polygon': 'saddlebrown', 'polyline': 'saddlebrown'})

    FORCE_REFRESH = False  # or make it a UI toggle
    fossil_df = fetch_and_cache_fossils(force_refresh=FORCE_REFRESH)
    log(f"🦴 Fossil data rows: {len(fossil_df)}")

    fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time)
    log(f"✅ Fossils reconstructed: {len(fossil_data)}")

    plot_fossils(ax, fossil_data, size_deg=150, original=False)  # Reconstructed
    plot_fossils(ax, fossil_data, size_deg=100, original=True)   # Present-day
    plot_fossil_vectors(ax, fossil_data, color='red')            # Arrows between them

    active_layers = {
    'reconstructed_fossils': True,
    'present_day_fossils': True,
    'vectors': True,
    'coastlines': True,
    'plate_boundaries': True,
    }
    draw_dynamic_legend(ax, active_layers)

def create_ui():
    from ipywidgets import Button
    from animation import run_animation

    out = Output()
    slider = IntSlider(
        value=70, min=0, max=1000, step=5,
        description='Time (Ma)', continuous_update=False
    )

    # --- Plot updater for slider ---
    def update_plot(change):
        with out:
            out.clear_output(wait=True)
            time = change['new']

            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
            ax.set_global()
            ax.set_title(f"Reconstructed Plates and Fossils at {time} Ma")

            plot_all(ax, time)
            plt.show()

    slider.observe(update_plot, names='value')

    # --- Animation button ---
    button = Button(description="Run Animation", button_style="info")

    def on_button_click(b):
        with out:
            out.clear_output(wait=True)
            print("🎬 Running animation...")
            run_animation(start=0, end=70, step=5, export=False, outdir="exports", make_video=False)
            print("✅ Animation complete. Frames saved in 'exports/'")

    button.on_click(on_button_click)

    # Display both slider + button + output
    display(VBox([slider, button, out]))

    # Initialize with current slider value
    update_plot({'new': slider.value})
