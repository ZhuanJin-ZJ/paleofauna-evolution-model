# Copyright (C) 2026 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from ui import update_scene
import utils
import os
from export_movie import make_mp4
from concurrent.futures import ProcessPoolExecutor

def render_frame(args):
    t, frame_index, export, outdir = args
    
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())
    ax.set_global()
    ax.set_title(f"Reconstructed Plates and Fossils at {t} Ma")

    plot_all(ax, t, export=export, outdir=outdir)
    if export:
        save_path = os.path.join(outdir, f"frame_{frame_index:04d}.png")
        fig.savefig(save_path, dpi=150)
        

def run_animation(start=0, end=70, step=5, export=False, outdir="exports", make_video=False, workers=2):
    utils.VERBOSE = False    # Silence logs globally
    ### Animate tectonic & fossil reconstructions.
    #   Args:
        # start (int): starting Ma (default 0, present-day).
        # end (int): max Ma to step back to.
        # step (int): step size in Ma (default 10).
        # export (bool): whether to export images instead of interactive display.
        # outdir (str): directory to save images.

    times = list(range(start, end + 1, step))
    frame_index = 0

    if export:
        os.makedirs(outdir, exist_ok=True)

        tasks = [
            (t, i, export, outdir)
            for i, t in enumerate(times)
        ]

        with ProcessPoolExecutor(max_workers=workers) as executor:
            executor.map(render_frame, tasks)

        if make_video:
            make_mp4(input_dir=outdir, output_file=f"{outdir}/animation.mp4", fps=1)

    else:
        # fallback to sequential for interactive mode
        for i, t in enumerate(times):
            render_frame((t, i, export, outdir))