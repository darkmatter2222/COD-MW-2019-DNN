import pyautogui
import numpy as np
import tensorflow.keras as keras

# Load Model
model = keras.models.load_model('..\\Models\\CODV4.h5')

print('Started')
while 1 == 1:
    # Grab Screen
    im = pyautogui.screenshot(region=(860, 440, 200, 200))

    # Format and Normalize Data
    ReducedGrayScaleNPNeutralImages = np.asarray([np.asarray(im)]) / 255

    # Predict
    prediction = model.predict(ReducedGrayScaleNPNeutralImages)

    if prediction[0][0] > 0.99:
        print('Enemy!')
    else:
        print('')



