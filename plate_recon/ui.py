# Copyright (C) 2026 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import cartopy.crs as ccrs

from config import rotation_model
from ipywidgets import IntSlider, VBox, Output
from IPython.display import display

from tectonics import (
    get_plate_boundaries, 
    reconstruct_features, 
    reconstruct_coastlines, 
    reconstruct_polygons, 
    rasterise_landmask
)

import fossils
from utils import log

class Scene:
    def __init__(self):
        self.fig = None
        self.ax = None

        self.landmask_img = None
        self.boundary_lines = None
        self.coastline_lines = None

        self.fossil_artists = []

OCEAN_BLUE = "#305CDE"
LAND_GREEN = "#a9fb4c"
RES_DEG    = 1.0

# Access functions via the module namespace to ensure you use the latest
fetch_and_cache_fossils = fossils.fetch_and_cache_fossils
reconstruct_fossil_locations = fossils.reconstruct_fossil_locations

# Load the T. rex image once
BASE_DIR   = os.path.dirname(os.path.dirname(__file__)) # Go up one level in the directory
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
T_REX_ICON = mpimg.imread(os.path.join(ASSETS_DIR, "t_rex.png"))

from shapely.geometry import Polygon

def render_oceanmask(ax, color=OCEAN_BLUE):
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

def render_landmask(ax, time, resolution_deg=1.0, img=None):
    """
    Raster landmask renderer.
    This REPLACES all polygon filling logic.
    """
    polygons = reconstruct_polygons(time)

    landmask, lats, lons = rasterise_landmask(
        polygons,
        time,
        resolution_deg
    )

    from matplotlib.colors import ListedColormap

    cmap = ListedColormap([
        (0, 0, 0, 0),   # Transparent ocean
        "#89C544"
    ])

    if img is None:
        
        img = ax.imshow(
            landmask.astype(float),
            extent=[-180, 180, -90, 90],
            origin="lower",
            transform=ccrs.PlateCarree(),
            cmap=cmap,
            vmin=0,
            vmax=1,
            zorder=1
        )

        return img
    else:
        img.set_data(landmask.astype(float))
        return img

from matplotlib.collections import LineCollection
    
def build_lines(reconstructed_geometries,):
    
    lines = []
    
    for feature in reconstructed_geometries:
        geom = feature.get_reconstructed_geometry()
        if hasattr(geom, 'to_lat_lon_list'):
            lat_lon_list = geom.to_lat_lon_list()
            if lat_lon_list:
                lats, lons = zip(*lat_lon_list)
                lines.append(list(zip(lons, lats)))

    return lines
                
def plot_fossils(ax, fossil_data, size_deg=1.0, original=False):
    """
    If original=True  → draw grey dots
    If original=False → draw T. rex image icons
    """
    artists = []
    
    pc = ccrs.PlateCarree()
    proj = ax.projection # Robinson projection used in the figure

    for fossil in fossil_data:
        lat = fossil['original_lat'] if original else fossil['recon_lat']
        lon = fossil['original_lon'] if original else fossil['recon_lon']

        if original:
            # --- Present-day fossils: grey dots ---
            artist = ax.plot(
                lon, lat, 'o',
                transform=ccrs.Geodetic(),
                color='gray',
                markersize=3,
                alpha=0.6,
                zorder=5
            )[0]

            artists.append(artist)
            
        else:
            # --- Reconstructed fossils: image icons ---
            # Transform (lon, lat) into Robinson projected coordinates
            x, y = proj.transform_point(lon, lat, pc)

            # Size in projected units (rough guess: degrees → projection scale)
            d = size_deg * 10000

            artist = ax.imshow(
                T_REX_ICON,
                extent=[x - d, x + d, y - d, y + d],
                transform=proj,   # NOT PlateCarree anymore
                origin="upper",
                alpha=1.0,
                zorder=10
            )

            artists.append(artist)
    return artists

def plot_fossil_vectors(ax, fossil_data, color='red'):

    artists = []
    
    for fossil in fossil_data:
        orig_lat = fossil['original_lat']
        orig_lon = fossil['original_lon']
        recon_lat = fossil['recon_lat']
        recon_lon = fossil['recon_lon']

        artist = ax.plot(
            [orig_lon, recon_lon], [orig_lat, recon_lat],
            transform=ccrs.Geodetic(), color=color,
            linewidth=0.7, alpha=0.7
        )[0]
        
        artists.append(artist)
        
    return artists

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

def update_scene(scene, time):
    
    print(f"⏳ Reconstructing for time: {time} Ma")
    
    import time as pytime
    t0 = pytime.perf_counter()

    ax = scene.ax
    ax.set_title(f"Reconstructed Plates and Fossils at {time} Ma")

    # --- Plate features ---
    t1 = pytime.perf_counter()

    features = get_plate_boundaries(time)

    boundaries = reconstruct_features(features, time)
    coastlines = reconstruct_coastlines(time)

    lines_boundaries = build_lines(boundaries)
    lines_coast = build_lines(coastlines)

    scene.boundary_lines.set_segments(lines_boundaries)
    scene.coastline_lines.set_segments(lines_coast)

    print("Tectonics:", pytime.perf_counter() - t1)

    # --- Landmask ---
    t2 = pytime.perf_counter()
    
    scene.landmask_img.remove()
    scene.landmask_img = render_landmask(
        ax,
        time,
        resolution_deg=RES_DEG
    )

    print("Land mask:", pytime.perf_counter() - t2)

    # --- Fossils ---
    t3 = pytime.perf_counter()
    
    for artist in scene.fossil_artists:
        artist.remove()

    scene.fossil_artists.clear()

    FORCE_REFRESH = False  # or make it a UI toggle

    fossil_df = fetch_and_cache_fossils(force_refresh=FORCE_REFRESH)
    log(f"🦴 Fossil data rows: {len(fossil_df)}")

    fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time, species_name="Tyrannosaurus_rex", limit=4, model_name="Muller2022")
    log(f"✅ Fossils reconstructed: {len(fossil_data)}")

    print("Fossils:", pytime.perf_counter() - t3)

    t4 = pytime.perf_counter()
    
    artists = []

    artists += plot_fossils(ax, fossil_data, size_deg=150, original=False)  # Reconstructed
    artists += plot_fossils(ax, fossil_data, size_deg=100, original=True)   # Present-day
    artists += plot_fossil_vectors(ax, fossil_data, color='red')            # Arrows between them

    scene.fossil_artists = artists

    print("Fossil plotting:", pytime.perf_counter() - t4)

    # --- Legend ---
    t5 = pytime.perf_counter()

    active_layers = {
    'reconstructed_fossils': True,
    'present_day_fossils': True,
    'vectors': True,
    'coastlines': True,
    'plate_boundaries': True,
    }
    draw_dynamic_legend(ax, active_layers)
    print("Legend:", pytime.perf_counter() - t5)

    # --- Render ---
    t6 = pytime.perf_counter()
    scene.fig.canvas.draw_idle()
    print("Render:", pytime.perf_counter() - t6)

    print("Total time:", pytime.perf_counter() - t0)    


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
    import time as pytime
    t0 = pytime.perf_counter()

    t1 = pytime.perf_counter()
    features = get_plate_boundaries(time)
    reconstructed_boundaries = reconstruct_features(features, time)
    reconstructed_coastlines = reconstruct_coastlines(time)
    print("Tectonics:", pytime.perf_counter() - t1)

    t2 = pytime.perf_counter()
    render_oceanmask(ax)                                         # Paint oceans first
    print("Ocean mask:", pytime.perf_counter() - t2)

    t3 = pytime.perf_counter()
    render_landmask(ax, time, resolution_deg=RES_DEG)            # Paint landmasses
    print("Land mask:", pytime.perf_counter() - t3)

    t4 = pytime.perf_counter()
    plot_reconstructed_features(ax, reconstructed_boundaries, 'blue')
    plot_reconstructed_features(ax, reconstructed_coastlines, 'saddlebrown')
    print("Plate features:", pytime.perf_counter() - t4)

    t5 = pytime.perf_counter()
    FORCE_REFRESH = False  # or make it a UI toggle
    fossil_df = fetch_and_cache_fossils(force_refresh=FORCE_REFRESH)
    log(f"🦴 Fossil data rows: {len(fossil_df)}")

    fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time, species_name="Tyrannosaurus_rex", limit=4, model_name="Muller2022")
    log(f"✅ Fossils reconstructed: {len(fossil_data)}")
    print("Fossils:", pytime.perf_counter() - t5)

    t6 = pytime.perf_counter()
    plot_fossils(ax, fossil_data, size_deg=150, original=False)  # Reconstructed
    plot_fossils(ax, fossil_data, size_deg=100, original=True)   # Present-day
    plot_fossil_vectors(ax, fossil_data, color='red')            # Arrows between them
    print("Fossil plotting:", pytime.perf_counter() - t6)

    t7 = pytime.perf_counter()
    active_layers = {
    'reconstructed_fossils': True,
    'present_day_fossils': True,
    'vectors': True,
    'coastlines': True,
    'plate_boundaries': True,
    }
    draw_dynamic_legend(ax, active_layers)
    print("Legend:", pytime.perf_counter() - t7)

    print("Total time:", pytime.perf_counter() - t0)


def create_scene(initial_time=70):

    scene = Scene()

    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(1,1,1, projection=ccrs.Robinson())
    ax.set_global()

    scene.fig = fig
    scene.ax = ax

    render_oceanmask(ax)

    # --- Initial tectonics ---
    features = get_plate_boundaries(initial_time)
    boundaries = reconstruct_features(features, initial_time)
    coastlines = reconstruct_coastlines(initial_time)

    lines1 = build_lines(boundaries)
    lines2 = build_lines(coastlines)

    scene.boundary_lines = LineCollection(
        lines1,
        colors='blue',
        linewidths=0.5,
        transform=ccrs.Geodetic()
    )

    scene.coastline_lines = LineCollection(
        lines2,
        colors='saddlebrown',
        linewidths=0.5,
        transform=ccrs.Geodetic()
    )

    ax.add_collection(scene.boundary_lines)
    ax.add_collection(scene.coastline_lines)

    # --- Landmask ---
    scene.landmask_img = render_landmask(ax, initial_time)

    plt.close(fig)

    return scene
    
def create_ui():
    from ipywidgets import Button
    from animation import run_animation

    scene = create_scene(initial_time=70)

    out = Output()
    slider = IntSlider(
        value=70, min=0, max=1000, step=5,
        description='Time (Ma)', continuous_update=False
    )

    # --- Plot updater for slider ---
    def update_plot(change):
        with out:
            out.clear_output(wait=True)
            update_scene(scene, change['new'])
            display(scene.fig)

    slider.observe(update_plot, names='value')

    # --- Animation button ---
    button = Button(description="Run Animation", button_style="info")

    def on_button_click(b):
        with out:
            out.clear_output(wait=True)
            print("🎬 Running animation...")
            run_animation(start=0, end=70, step=5, export=True, outdir="exports", make_video=True, workers=2)
            print("✅ Animation complete. Frames saved in 'exports/'")

    button.on_click(on_button_click)

    # Display both slider + button + output
    display(VBox([slider, button, out]))

    # Initialize with current slider value
    update_plot({'new': slider.value})
