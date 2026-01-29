import importlib.util
import os
import numpy as np
import cv2

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# -----------------------------
# Helper to load python files
# -----------------------------
def load_module(filename, name):
    path = os.path.join(ROOT, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Load your files
take_picture = load_module("take picture.py", "take_picture_mod")
training = load_module("training.py", "training_mod")
test_app = load_module("test.py", "test_mod")
sin_nn = load_module("sin nn.py", "sin_nn_mod")


# =============================
# take picture.py tests
# =============================
def test_extract_face_output_shape():
    img = np.zeros((200, 200, 3), dtype=np.uint8)

    class FakeCascade:
        def detectMultiScale(self, gray, a, b):
            return [(50, 50, 100, 100)]

    face = take_picture.extract_face(img, FakeCascade())
    assert face.shape == (50, 50)


def test_extract_face_no_face():
    img = np.zeros((200, 200, 3), dtype=np.uint8)

    class FakeCascade:
        def detectMultiScale(self, gray, a, b):
            return []

    face = take_picture.extract_face(img, FakeCascade())
    assert face is None


# =============================
# training.py tests
# =============================
def test_layer_forward_shape():
    layer = training.Layer(10, 5)
    X = np.random.rand(3, 10)
    layer.forward(X)
    assert layer.output.shape == (3, 5)


def test_loss_c2_positive_value():
    loss = training.Loss_C2()
    y_pred = np.array([[2.0], [1.0]])
    y_true = np.array([[0.0], [0.0]])
    value = loss.calculate(y_pred, y_true)
    assert value > 0


def test_build_dataset_shape():
    img1 = np.zeros((50, 50))
    img2 = np.ones((50, 50))
    X = training.build_dataset([(img1, img2)])
    assert X.shape == (1, 5000)


# =============================
# test.py tests
# =============================
def test_predict_output_shape():
    X = np.random.rand(2, 5000)

    layers = [
        test_app.Layer(5000, 10), test_app.ActivationReLU(),
        test_app.Layer(10, 5), test_app.ActivationReLU(),
        test_app.Layer(5, 3), test_app.ActivationReLU(),
        test_app.Layer(3, 2), test_app.ActivationSoftmax()
    ]

    output = test_app.predict(layers, X)
    assert output.shape == (2, 2)


# =============================
# sin nn.py tests
# =============================
def test_sin_layer_forward_shape():
    layer = sin_nn.Layer(1, 5)
    X = np.random.rand(4, 1)
    layer.forward(X)
    assert layer.output.shape == (4, 5)


def test_sin_loss_positive():
    loss = sin_nn.Loss_C2()
    y_pred = np.array([[1.0], [2.0]])
    y_true = np.array([[0.0], [0.0]])
    value = loss.calculate(y_pred, y_true)
    assert value > 0
