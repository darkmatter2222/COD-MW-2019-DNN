import pyautogui
import numpy as np
import ctypes

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)
print('Screen Size X:%d y:%d' % screenSize)
print('Targeting Center X:%d y:%d' % centerPoint)

print('Started')
while 1 == 1:
    # Grab Screen
    image = pyautogui.screenshot(region=(centerPoint[0] - 100, centerPoint[1] - 100, 200, 200))
    # Format and Normalize Data
    normalizedImage = np.asarray([np.asarray(image)]) / 255
    # Save
