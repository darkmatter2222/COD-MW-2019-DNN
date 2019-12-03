import pyautogui
import numpy as np
from datetime import datetime
from datetime import timedelta
import tensorflow.keras as keras
import ctypes
import uuid

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)
print('Screen Size X:%d y:%d' % screenSize)
print('Targeting Center X:%d y:%d' % centerPoint)

# 4K Check
fourKMultiplier = 1
if screenSize[0] == 3840:
    fourKMultiplier = 2
elif screenSize[0] == 1920:
    fourKMultiplier = 1
else:
    raise Exception('Invalid Screen Resolution', 'Set up your screen resolution')


lastSecondTimestamp = datetime.utcnow() + timedelta(seconds=1)
tickCounter = 0

# Load Model
model = keras.models.load_model('..\\Models\\CODV5.h5')

# Starting Main Loop (will run faster if using Tensorflow + GPU)
print('Started Inner Loop')
while True:
    tickCounter += 1

    if datetime.utcnow() > lastSecondTimestamp:
        lastSecondTimestamp = datetime.utcnow() + timedelta(seconds=1)
        print('Ticks Per Second %d' % tickCounter)
        tickCounter = 0

    # Grab Screen
    image = pyautogui.screenshot(region=(centerPoint[0] - (100 * fourKMultiplier),
                                         centerPoint[1] - (100 * fourKMultiplier),
                                         (200 * fourKMultiplier), (200 * fourKMultiplier)))
    if image.size != (200, 200):
        image = image.resize((200, 200), 0)

    # Format and Normalize Data
    normalizedImage = np.asarray([np.asarray(image)]) / 255
    # Predict
    prediction = model.predict(normalizedImage)

    targetFolder = None

    if prediction[0][0] == 1 and (1 == 1):
        targetFolder = '\\100\\'
    elif prediction[0][0] > .90 and prediction[0][0] < 100 and (1 == 1):
        targetFolder = '\\90-99\\'
    elif prediction[0][0] > .80 and prediction[0][0] < .90 and (1 == 1):
        targetFolder = '\\80-89\\'
    elif prediction[0][0] > .70 and prediction[0][0] < .80 and (1 == 1):
        targetFolder = '\\70-79\\'
    elif prediction[0][0] > .60 and prediction[0][0] < .70 and (1 == 1):
        targetFolder = '\\60-69\\'
    elif prediction[0][0] > .50 and prediction[0][0] < .60 and (1 == 1):
        targetFolder = '\\50-59\\'
    elif prediction[0][0] > .40 and prediction[0][0] < .50 and (1 == 1):
        targetFolder = '\\40-49\\'
    elif prediction[0][0] > .30 and prediction[0][0] < .40 and (1 == 1):
        targetFolder = '\\30-39\\'
    elif prediction[0][0] > .20 and prediction[0][0] < .30 and (1 == 1):
        targetFolder = '\\20-29\\'
    elif prediction[0][0] > .10 and prediction[0][0] < .20 and (1 == 1):
        targetFolder = '\\10-19\\'

    if targetFolder is not None:
        baseDirectory = 'G:\\Projects\\COD Target Trainer\\Data Collection'
        generatedGUID = str(uuid.uuid1())
        image.save(baseDirectory + targetFolder + generatedGUID + '.png', 'png')
        print('Writing %' + str((prediction[0][0] * 100)))


