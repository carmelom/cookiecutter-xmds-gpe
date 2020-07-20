#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 06-2019 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""

import numpy as np
import matplotlib.pyplot as plt

try:
    from moviepy.video.io.bindings import mplfig_to_npimage
    import moviepy.editor as mpy
    IMPORT_MOVIEPY = True
except ModuleNotFoundError:  # as e:
    # print(f"{e}\nFallback to matplotlib")
    IMPORT_MOVIEPY = False


import h5py


def make_movie(h5filename, fps=20, output=None):
    with h5py.File(h5filename, 'r') as f:
        g = f['realtime/1']
        t = g['t'][:]
        x = g['x'][:]
        psiI = g['psiI'][:]
        psiR = g['psiR'][:]

    n = np.hypot(psiR, psiI)
    margin = 0.05
    ylim = n.min() - margin * n.ptp(), n.max() + margin * n.ptp()
    Nframes = len(t)
    duration = Nframes / fps

    fig, ax = plt.subplots()
    line, = ax.plot(x, n[0])
    ax.plot(x, n[0], ls='--', alpha=0.6)
    ax.set_ylim(ylim)

    if not IMPORT_MOVIEPY or output is None:
        print("Using matplotlib")

        def show_frame(ix):
            line.set_ydata(n[ix])

        for ix in range(len(t)):
            show_frame(ix)
            plt.pause(0.05)

    else:
        plt.show()

        def make_frame_mpl(_t):
            ix = int(_t / duration * Nframes)
            # print(ix)
            line.set_ydata(n[ix])  # <= Update the curve
            return mplfig_to_npimage(fig)  # RGB image of the figure

        animation = mpy.VideoClip(make_frame_mpl, duration=duration)
        animation.write_videofile(output, fps=fps)
        # animation.write_gif("movie.gif", fps=20)
