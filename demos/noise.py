# Code adapted from
# https://matplotlib.org/stable/gallery/mplot3d/custom_shaded_3d_surface.html#sphx-glr-gallery-mplot3d-custom-shaded-3d-surface-py
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import numpy as np
import perlin_noise


# Load and format data
nrows, ncols = 100, 100
xmin=-1
xmax=1
ymin=-1
ymax=1
def get_landscape(size, seed=1):
    x = np.linspace(xmin, size[0], size[1])
    y = np.linspace(ymin, size[1], size[1])
    x, y = np.meshgrid(x, y)

    proportions = reversed([100, 0.5, 0.5, 1.])
    pnoise = [perlin_noise.PerlinNoise(i) for i in [1, 3, 5, 10 ]]
    def perlin(x, y, o):
        return pnoise[o]([x, y])
    vperlin = np.vectorize(perlin)

    region = np.s_[0:size[0], 0:size[1]]
    z=vperlin(x[region], y[region], 0)
    for i, prop in zip(range(len(pnoise)), proportions):
        z += prop*vperlin(x[region], y[region], i) 
    return x, y, z
# Set up plot

if __name__ == '__main__':
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

    x, y, z = get_landscape((nrows, ncols))
    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(z, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=rgb,
                        linewidth=0, antialiased=False, shade=False)
    ax.set_zlim3d(-1, 1)
    plt.show()