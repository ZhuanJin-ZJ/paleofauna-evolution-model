# Copyright (C) 2025 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
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

    ### Plot fossils as T. rex PNG silhouettes instead of dots.
    #   size_deg controls the size of each icon in degrees.
    for fossil in fossil_data:
        lat = fossil['original_lat'] if original else fossil['recon_lat']
        lon = fossil['original_lon'] if original else fossil['recon_lon']

        # Half-size for convenience
        d = size_deg / 2.0

        ax.imshow(
            T_REX_ICON,
            extent=[lon - d, lon + d, lat - d, lat + d],
#            transform=ccrs.Geodetic(),
            alpha=0.8 if original else 1.0,
            zorder=10  # ensures fossils display above coastlines
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
    import numpy as np

    print("Shape:", T_REX_ICON.shape)
    print("Min/Max:", np.min(T_REX_ICON), np.max(T_REX_ICON))
    print("Unique sample:", np.unique(T_REX_ICON.reshape(-1, T_REX_ICON.shape[-1])[:20], axis=0))
    
    features = get_plate_boundaries(time)
    reconstructed_boundaries = reconstruct_features(features, time)
    reconstructed_coastlines = reconstruct_coastlines(time)

    plot_reconstructed_features(ax, reconstructed_boundaries, {'polygon': 'red', 'polyline': 'blue'})
    plot_reconstructed_features(ax, reconstructed_coastlines, {'polygon': 'saddlebrown', 'polyline': 'saddlebrown'})

    FORCE_REFRESH = False  # or make it a UI toggle
    fossil_df = fetch_and_cache_fossils(force_refresh=FORCE_REFRESH)
    log(f"🦴 Fossil data rows: {len(fossil_df)}")

    fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time)
    log(f"✅ Fossils reconstructed: {len(fossil_data)}")

    plot_fossils(ax, fossil_data, size_deg=15, original=False)  # Reconstructed
    plot_fossils(ax, fossil_data, size_deg=10, original=True)   # Present-day
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
        value=40, min=0, max=1000, step=5,
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
