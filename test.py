import matplotlib.pyplot as plt
import numpy as np
import random, os, cv2, time, pygame, tkinter.filedialog

np.random.seed(0)
random.seed(0)

# -----------------------------
# Settings
# -----------------------------
model_folder = 'model'
model_name_load = '50x50-4l'
folder = 'subjects_photos'
camera_input = False

names = {0:'MML' , 1:'mml' , 2:'mml' , 3:'sol' , 4:'sol', 5:'sol'}

# -----------------------------
# Load subject photos
# -----------------------------
if not os.path.exists(folder):
    print("❌ Folder not found:", folder)
    exit()

list_dir = os.listdir(folder)
print("Photos:", list_dir)
print("Total photos:", len(list_dir))

# -----------------------------
# Select input image
# -----------------------------
if not camera_input:
    filename = tkinter.filedialog.askopenfilename(title="Select a face image")
    print("Selected:", filename)
    frame = cv2.imread(filename)
else:
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()

if frame is None:
    print("❌ Failed to load input image.")
    exit()

# -----------------------------
# Load Haar cascade
# -----------------------------
cascade_path = "haarcascade_frontalface_default.xml"
if not os.path.exists(cascade_path):
    print("❌ Missing haarcascade file:", cascade_path)
    exit()

face_cascade = cv2.CascadeClassifier(cascade_path)

# -----------------------------
# Data containers
# -----------------------------
data = []
y = []

# -----------------------------
# Load photos function
# -----------------------------
def load_photos():
    global data, y, frame

    data = []
    labels = []

    # Reload frame
    if camera_input:
        check, frame = webcam.read()
    else:
        frame = cv2.imread(filename)

    if frame is None:
        print("❌ Failed to reload image.")
        return False

    # Assume the selected image is the face (already cropped)
    if len(frame.shape) == 3:
        face_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        face_roi = frame
    face_roi = cv2.resize(face_roi, (50, 50))

    # -----------------------------
    # Build dataset
    # -----------------------------
    for fname in list_dir:
        img_path = os.path.join(folder, fname)
        image1 = cv2.imread(img_path)

        if image1 is None:
            print("⚠️ Could not read:", fname)
            continue

        image1 = cv2.resize(image1, (50, 50))
        photodata = []

        # Subject image pixels
        for j in range(50):
            for k in range(50):
                photodata.append(image1[j][k][0] / 255.0)

        # Detected face pixels
        for j in range(50):
            for k in range(50):
                photodata.append(face_roi[j][k] / 255.0)

        data.append(photodata)
        labels.append(0)

    y = np.array(labels)
    return True

# Initial load
if not load_photos():
    print("❌ Cannot continue without face detection.")
    exit()

print("Dataset size:", len(data))

# -----------------------------
# Neural Network
# -----------------------------
class Layer:
    def __init__(self, n_inputs, n_neurons):
        self.weights = 0.1 * np.random.rand(n_inputs, n_neurons) - 0.05
        self.biases = np.zeros((1, n_neurons))

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class ActivationReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)


class ActivationSoftmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        self.output = exp_values / np.sum(exp_values, axis=1, keepdims=True)


# -----------------------------
# Build network
# -----------------------------
layer1 = Layer(5000, 500)
layer2 = Layer(500, 50)
layer3 = Layer(50, 10)
layer4 = Layer(10, 2)

activation1 = ActivationReLU()
activation2 = ActivationReLU()
activation3 = ActivationReLU()
activation4 = ActivationSoftmax()

# -----------------------------
# Load saved weights (optional)
# -----------------------------
try:
    layer1.weights = np.load(model_folder + '/best_layer1_weights'+model_name_load+'.npy')
    layer1.biases  = np.load(model_folder + '/best_layer1_biases'+model_name_load+'.npy')
    layer2.weights = np.load(model_folder + '/best_layer2_weights'+model_name_load+'.npy')
    layer2.biases  = np.load(model_folder + '/best_layer2_biases'+model_name_load+'.npy')
    layer3.weights = np.load(model_folder + '/best_layer3_weights'+model_name_load+'.npy')
    layer3.biases  = np.load(model_folder + '/best_layer3_biases'+model_name_load+'.npy')
    layer4.weights = np.load(model_folder + '/best_layer4_weights'+model_name_load+'.npy')
    layer4.biases  = np.load(model_folder + '/best_layer4_biases'+model_name_load+'.npy')
    print("✅ Model weights loaded.")
except:
    print("⚠️ Model weights not found. Using random weights.")

# -----------------------------
# Single prediction
# -----------------------------
layer1.forward(data)
activation1.forward(layer1.output)

layer2.forward(activation1.output)
activation2.forward(layer2.output)

layer3.forward(activation2.output)
activation3.forward(layer3.output)

layer4.forward(activation3.output)
activation4.forward(layer4.output)

predictions = np.argmax(activation4.output, axis=1)
print("Predictions for each subject:", predictions)
print("Program completed.")
