# Copyright (C) 2025 Zhuan Jin Yee
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import subprocess

def make_mp4(input_dir="exports", output_file="animation.mp4", fps=6):
    ### Stitch PNG frames into an MP4 using ffmpeg.
    # Requires ffmpeg installed on your system.
    # Check ffmpeg exists
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        raise RuntimeError("ffmpeg not found. Install from https://ffmpeg.org/download.html")

    input_pattern = os.path.join(input_dir, "frame_%04dMa.png")

    cmd = [
        "ffmpeg",
        "-y",                     # overwrite output file
        "-framerate", str(fps),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_file
    ]

    print("🎥 Creating MP4...")
    subprocess.run(cmd, check=True)
    print(f"✅ Movie saved as {output_file}")