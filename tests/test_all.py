import importlib.util
import os
import numpy as np
import builtins
import cv2
import tkinter.filedialog

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# -----------------------------
# SAFETY PATCHES
# -----------------------------

# Disable file dialog popup
tkinter.filedialog.askopenfilename = lambda *args, **kwargs: "dummy.png"

# Fake image reader (always return dummy image)
cv2.imread = lambda *args, **kwargs: np.zeros((50, 50, 3), dtype=np.uint8)

# Fake cascade detector
class FakeCascade:
    def detectMultiScale(self, *args, **kwargs):
        return [(0, 0, 50, 50)]

cv2.CascadeClassifier = lambda *args, **kwargs: FakeCascade()

# Prevent infinite loops
_original_range = builtins.range
def safe_range(*args):
    if len(args) == 1 and args[0] > 1000:
        return _original_range(1)
    return _original_range(*args)

builtins.range = safe_range


# -----------------------------
# Safe module loader
# -----------------------------
def load_module(filename, name):
    path = os.path.join(ROOT, filename)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except BaseException:
        # Ignore runtime errors from GUI / camera code
        pass
    return module


# Load your scripts (NO sin nn.py)
take_picture = load_module("take picture.py", "take_picture_mod")
training = load_module("training.py", "training_mod")
test_app = load_module("test.py", "test_mod")


# =============================
# take picture.py tests
# =============================
def test_extract_face_output_shape():
    img = np.zeros((200, 200, 3), dtype=np.uint8)

    class DummyCascade:
        def detectMultiScale(self, gray, a, b):
            return [(50, 50, 100, 100)]

    face = take_picture.extract_face(img, DummyCascade())
    assert face.shape == (50, 50)


# =============================
# training.py tests
# =============================
def test_training_layer_forward_shape():
    layer = training.Layer(10, 5)
    X = np.random.rand(3, 10)
    layer.forward(X)
    assert layer.output.shape == (3, 5)


def test_training_build_dataset_shape():
    img1 = np.zeros((50, 50))
    img2 = np.ones((50, 50))
    X = training.build_dataset([(img1, img2)])
    assert X.shape == (1, 5000)


# =============================
# NOTE:
# test.py predict() is NOT tested because
# test.py executes GUI + camera code during import.
# This makes predict() unavailable safely in CI.
# =============================
