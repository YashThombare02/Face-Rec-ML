import numpy as np
from training import build_dataset


def test_build_dataset_shape():
    img1 = np.zeros((50, 50))
    img2 = np.ones((50, 50))

    X = build_dataset([(img1, img2)])

    assert X.shape == (1, 5000)


def test_build_dataset_value_range():
    img1 = np.zeros((50, 50)) * 255
    img2 = np.ones((50, 50)) * 255

    X = build_dataset([(img1, img2)])

    assert X.min() >= 0.0
    assert X.max() <= 1.0
