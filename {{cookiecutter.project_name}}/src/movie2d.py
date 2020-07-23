#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create: 06-2019 - Carmelo Mordini <carmelo> <carmelo.mordini@unitn.it>

"""Module docstring

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
# from .holepatch import make_holepatch

try:
    from moviepy.video.io.bindings import mplfig_to_npimage
    import moviepy.editor as mpy
    IMPORT_MOVIEPY = True
except ModuleNotFoundError as e:
    print(f"{e}\nFallback to matplotlib")
    IMPORT_MOVIEPY = False


import h5py


def make_movie(h5filename, fps=20, output=None):
    with h5py.File(h5filename, 'r') as f:
        t = f['1/t'][:]
        x = f['1/x'][:]
        y = f['1/x'][:]
        psiI = f['1/psiI'][:]
        psiR = f['1/psiR'][:]

    R_tf = 4.2

    density = psiR**2 + psiI**2
    phase = np.arctan2(psiR, psiI)

    Nframes = len(t)
    duration = Nframes / fps

    extent = (x.min(), x.max(), y.min(), y.max())

    h, w = plt.rcParams['figure.figsize']
    fig, (ax, ax_p) = plt.subplots(1, 2, figsize=(2 * w, h), sharey=True)
    fig.suptitle(h5filename)

    kk = {'ticks': None, 'orientation': 'horizontal',
          'ticklocation': 'top'}  # read this from make_axes

    c1 = ax.imshow(density[0], extent=extent, vmin=0, vmax=density.max())
    cax = ax.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c1, cax, **kk)

    c2 = ax_p.imshow(phase[0], cmap='RdBu', extent=extent)
    cax = ax_p.inset_axes([0, 1.06, 1, 0.04])
    plt.colorbar(c2, cax, **kk)

    for _ax, col in zip((ax, ax_p), ('w', 'k')):
        e = Ellipse((0, 0), 2 * R_tf, 2 * R_tf,
                    ls='--', lw=0.3, ec=col, fc='none')
        _ax.add_patch(e)
    # hp = make_holepatch(extent, radius=R_tf, color='w', alpha=0.6)
    # ax_p.add_patch(hp)

    text = ax.text(0, 1.23, f"t = {t[0]:.3f}",
                   transform=ax.transAxes, fontsize=14)

    R = abs(x.min())
    ax.set(xlim=(-R, R), ylim=(-R, R))
    ax_p.set(xlim=(-R, R), ylim=(-R, R))

    # plt.show()

    def update_frame(ix):
        c1.set_data(density[ix])
        c2.set_data(phase[ix])
        text.set_text(f"t = {t[ix]:.3f}")

    if not IMPORT_MOVIEPY or output is None:

        for ix in range(len(t)):
            update_frame(ix)
            # plt.draw()
            plt.pause(0.05)

    else:
        print(f"saving to {output}")
        plt.show()

        def make_frame_mpl(_t):
            ix = int(_t / duration * Nframes)
            # print(ix)
            update_frame(ix)
            return mplfig_to_npimage(fig)  # RGB image of the figure

        animation = mpy.VideoClip(make_frame_mpl, duration=duration)
        animation.write_videofile(output, fps=fps)
        # animation.write_gif("movie.gif", fps=20)


if __name__ == '__main__':
    import sys
    make_movie(sys.argv[1], 20, None)
