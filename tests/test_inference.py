import numpy as np
from test import predict
from model import Layer, ActivationReLU, ActivationLinear


def test_predict_output_shape():
    X = np.random.rand(3, 5000)

    layers = [
        Layer(5000, 10), ActivationReLU(),
        Layer(10, 5), ActivationReLU(),
        Layer(5, 3), ActivationReLU(),
        Layer(3, 2), ActivationLinear()
    ]

    output = predict(layers, X)

    assert output.shape == (3, 2)
