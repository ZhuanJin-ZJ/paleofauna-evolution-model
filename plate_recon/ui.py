import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from config import rotation_model
from ipywidgets import IntSlider, VBox, Output
from IPython.display import display
from tectonics import get_plate_boundaries, reconstruct_features, reconstruct_coastlines
import importlib
import fossils
importlib.reload(fossils)

# Access functions via the module namespace to ensure you use the latest
fetch_and_cache_fossils = fossils.fetch_and_cache_fossils
reconstruct_fossil_locations = fossils.reconstruct_fossil_locations


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


def plot_fossils(ax, fossil_data, color='darkgreen', original=False):
    for fossil in fossil_data:
        lat = fossil['original_lat'] if original else fossil['recon_lat']
        lon = fossil['original_lon'] if original else fossil['recon_lon']
        ax.plot(
            lon, lat, 'o',
            transform=ccrs.Geodetic(), 
            color='gray' if original else color, 
            markersize=3, alpha=0.6 if original else 1.0
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


def plot_all(ax, time, window=5):
    print(f"⏳ Reconstructing for time: {time} Ma")

    features = get_plate_boundaries(time)
    reconstructed_boundaries = reconstruct_features(features, time)
    reconstructed_coastlines = reconstruct_coastlines(time)

    plot_reconstructed_features(ax, reconstructed_boundaries, {'polygon': 'red', 'polyline': 'blue'})
    plot_reconstructed_features(ax, reconstructed_coastlines, {'polygon': 'saddlebrown', 'polyline': 'saddlebrown'})

    FORCE_REFRESH = True  # or make it a UI toggle
    fossil_df = fetch_and_cache_fossils(force_refresh=FORCE_REFRESH)
    print(f"🦴 Fossil data rows: {len(fossil_df)}")

    fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time, window=window)
    print(f"✅ Fossils reconstructed: {len(fossil_data)}")

    plot_fossils(ax, fossil_data, color='darkgreen')             # Reconstructed
    plot_fossils(ax, fossil_data, color='gray', original=True)   # Present-day
    plot_fossil_vectors(ax, fossil_data, color='red')            # Arrows between them


def create_ui():
    out = Output()
    slider = IntSlider(value=110, min=0, max=1000, step=10, description='Time (Ma)', continuous_update=False)

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
    display(VBox([slider, out]))
    update_plot({'new': slider.value})