import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from config import rotation_model
from ipywidgets import IntSlider, VBox, Output
from IPython.display import display
from tectonics import get_plate_boundaries, reconstruct_features, reconstruct_coastlines
import importlib
import fossils
importlib.reload(fossils)
from fossils import fetch_and_cache_fossils, reconstruct_fossil_locations


def plot_reconstructed_features(ax, reconstructed_geometries, color_map):
    for feature in reconstructed_geometries:
        geom = feature.get_reconstructed_geometry()
        if hasattr(geom, 'to_lat_lon_list'):
            lat_lon_list = geom.to_lat_lon_list()
            if lat_lon_list:
                lats, lons = zip(*lat_lon_list)
                ax.plot(lons, lats, '-', color=color_map.get(
                    'polygon' if 'Polygon' in geom.__class__.__name__ else 'polyline', 'black'),
                        transform=ccrs.Geodetic(), linewidth=0.5)

def plot_fossils(ax, fossil_data, color='darkgreen'):
    for fossil in fossil_data:
        ax.plot(
            fossil['recon_lon'], fossil['recon_lat'], 'o',
            transform=ccrs.Geodetic(), color=color, markersize=6
        )

def create_ui():
    out = Output()
    slider = IntSlider(value=110, min=0, max=1000, step=10, description='Time (Ma)', continuous_update=False)

    def update_plot(change):
        with out:
            out.clear_output(wait=True)

            time = change['new']
            print(f"⏳ Reconstructing for time: {time} Ma")

            features = get_plate_boundaries(time)
            reconstructed_boundaries = reconstruct_features(features, time)
            reconstructed_coastlines = reconstruct_coastlines(time)

            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
            ax.set_title(f"Reconstructed Plates and Coastlines at {time} Ma")

            plot_reconstructed_features(ax, reconstructed_boundaries, {'polygon': 'red', 'polyline': 'blue'})
            plot_reconstructed_features(ax, reconstructed_coastlines, {'polygon': 'saddlebrown', 'polyline': 'saddlebrown'})

            # === FOSSIL INTEGRATION ===
            fossil_df = fetch_and_cache_fossils()
            print(f"🦴 Fossil data rows: {len(fossil_df)}")

            fossil_data = reconstruct_fossil_locations(fossil_df, rotation_model, time, window=5)
            print(f"✅ Fossils reconstructed: {len(fossil_data)}")
#            print(fossil_data[:3])  # Preview first few reconstructions

            plot_fossils(ax, fossil_data)
            plt.show()

    slider.observe(update_plot, names='value')
    display(VBox([slider, out]))
    update_plot({'new': slider.value})

