import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ui import plot_all

def run_animation(start=0, end=250, step=10, export=False, outdir="exports"):
    ### Animate tectonic & fossil reconstructions.
    #   Args:
        # start (int): starting Ma (default 0, present-day).
        # end (int): max Ma to step back to.
        # step (int): step size in Ma (default 10).
        # export (bool): whether to export images instead of interactive display.
        # outdir (str): directory to save images.

    times = range(start, end + 1, step)

    for t in times:
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        ax.set_global()
        ax.set_title(f"Reconstructed Plates and Fossils at {t} Ma")

        plot_all(ax, t, window=5, export=export, outdir=outdir)

        if not export:
            plt.show()

        plt.close(fig)  # Close to free memory
