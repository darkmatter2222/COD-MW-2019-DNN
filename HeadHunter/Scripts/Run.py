import pyautogui
import numpy as np
import tensorflow.keras as keras
import ctypes
import json

# Load Model
model = keras.models.load_model('..\\Models\\MultiClassV2.h5')

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)
print('Screen Size X:%d y:%d' % screenSize)
print('Targeting Center X:%d y:%d' % centerPoint)

# Classes
classesOrigional = json.loads(open('..\\Models\\Classes.json').read())
classes = {}

for cl in classesOrigional:
    classes[classesOrigional[cl]] = cl

# Starting Main Loop (will run faster if using Tensorflow + GPU)
print('Started')
while 1 == 1:
    # Grab Screen
    image = pyautogui.screenshot(region=(centerPoint[0] - 100, centerPoint[1] - 100, 200, 200))
    # Format and Normalize Data
    normalizedImage = np.asarray([np.asarray(image)]) / 255
    # Predict
    prediction = model.predict(normalizedImage)

    results = []

    results.append(round((prediction[0][0] * 100), 2))
    results.append(round((prediction[0][1] * 100), 2))
    results.append(round((prediction[0][2] * 100), 2))

    # Print Result
    #print(f'{classes[0]}:{results[0]}, '
     #     f'{classes[1]}:{results[1]}, '
      #    f'{classes[2]}:{results[2]}, '
       #   f'Identified as: {classes[np.argmax(prediction)]}')

    print(f'Classified as: {classes[np.argmax(prediction)]} with {   round(prediction[0][np.argmax(prediction)] * 100, 2)   } Confidence')

