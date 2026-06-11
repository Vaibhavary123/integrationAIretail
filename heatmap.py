import numpy as np

heatmap = np.zeros(
    (1080,1920),
    dtype=np.float32
)


def update_heatmap(x, y):

    heatmap[y, x] += 1