import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np


def get_elevation(size, octaves=3):
    xpix, ypix = size
    noise = PerlinNoise(octaves=octaves, seed=2)
    # elevation = np.random.random(size)
    elevation = np.array(
        [[noise([i / xpix, j / ypix]) for j in range(ypix)] for i in range(xpix)]
    )
    return elevation


def elevation_to_rgba(elevation, cmap="gist_earth"):
    xpix, ypix = np.array(elevation).shape
    colormap = plt.cm.get_cmap(cmap)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    landscape = (
        np.array(
            [colormap(elevation[i, j])[0:3] for i in range(xpix) for j in range(ypix)]
        ).reshape(xpix, ypix, 3)
        * 255
    )
    landscape = landscape.astype("uint8")
    return landscape


get_landscape = lambda pixel_map: elevation_to_rgba(get_elevation(pixel_map))
get_combat_bg = lambda pixel_map: elevation_to_rgba(
    get_elevation(pixel_map, 10), "RdPu"
)


if __name__ == "__main__":
    size = 640, 480
    pic = elevation_to_rgba(get_elevation(size))
    plt.imshow(pic, cmap="gist_earth")
    plt.show()
