import numpy as np
import cv2
from take_picture import extract_face


def test_extract_face_returns_50x50():
    img = np.zeros((200, 200, 3), dtype=np.uint8)

    class FakeCascade:
        def detectMultiScale(self, gray, a, b):
            return [(50, 50, 100, 100)]

    face = extract_face(img, FakeCascade())

    assert face.shape == (50, 50)


def test_extract_face_returns_none_when_no_face():
    img = np.zeros((200, 200, 3), dtype=np.uint8)

    class FakeCascade:
        def detectMultiScale(self, gray, a, b):
            return []

    face = extract_face(img, FakeCascade())

    assert face is None
