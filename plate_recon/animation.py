# Copyright (C) 2025 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ui import plot_all
import utils
import os
from export_movie import make_mp4

def run_animation(start=0, end=70, step=5, export=False, outdir="exports", make_video=False):
    utils.VERBOSE = False    # Silence logs globally
    ### Animate tectonic & fossil reconstructions.
    #   Args:
        # start (int): starting Ma (default 0, present-day).
        # end (int): max Ma to step back to.
        # step (int): step size in Ma (default 10).
        # export (bool): whether to export images instead of interactive display.
        # outdir (str): directory to save images.

    times = range(start, end + 1, step)
    frame_index = 0

    for t in times:
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
        ax.set_global()
        ax.set_title(f"Reconstructed Plates and Fossils at {t} Ma")

        plot_all(ax, t, export=export, outdir=outdir)
        if export:
            save_path = os.path.join(outdir, f"frame_{frame_index:04d}.png")
            fig.savefig(save_path, dpi=150)
            frame_index += 1
        else:
            plt.show()

        plt.close(fig)  # Close to free memory

    # Create MP4 if requested
    if export and make_video:
        make_mp4(input_dir=outdir, output_file=f"{outdir}/animation.mp4", fps=6)