import importlib.util
import os
import sys
import numpy as np

# -------------------------------
# Load test.py explicitly by path
# -------------------------------

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEST_FILE = os.path.join(PROJECT_ROOT, "test.py")

spec = importlib.util.spec_from_file_location("local_test", TEST_FILE)
test_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(test_module)

predict = test_module.predict

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
