from tkinter import *
import ctypes
import pyautogui
import numpy as np
import tensorflow.keras as keras
from datetime import datetime
from datetime import timedelta

# Load Model
model = keras.models.load_model('..\\Models\\CODV5.h5')

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)



root = Tk()
v = StringVar()
flashLabel = Label(root, textvariable=v, background='black', foreground='red', font=("Helvetica bold", 50), width=1000)
flashLabel.pack()

v.set("Woot")

def task():
    lastSecondTimestamp = datetime.utcnow() + timedelta(seconds=1)
    tickCounter = 0
    while 1 == 1:
        tickCounter += 1

        if datetime.utcnow() > lastSecondTimestamp:
            lastSecondTimestamp = datetime.utcnow() + timedelta(seconds=1)
            print('Ticks Per Second %d' % tickCounter)
            tickCounter = 0


        # Grab Screen
        image = pyautogui.screenshot(region=(centerPoint[0] - 100, centerPoint[1] - 100, 200, 200))
        # Predict
        prediction = model.predict(np.asarray([np.asarray(image)]) / 255)
        # Print Result
        if prediction[0][0] > 0.95:
            v.set("Enemy " + str(round(prediction[0][0] * 100, 2)).zfill(6) + '% Confident')
            flashLabel.configure(foreground="red")
            flashLabel.update()
        else:
            v.set("Enemy " + str(round(prediction[0][0] * 100, 2)).zfill(6) + '% Confident')
            flashLabel.configure(foreground="green")
            flashLabel.update()


root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "#ffffff")
root.configure(background='#ffffff')
root.geometry('%dx%d+%d+%d' % (1000, 1000, centerPoint[0] - (500 * 1), centerPoint[1] - (500 * 1)))
root.title("Welcome to LikeGeeks app")

root.after(2000, task)
root.mainloop()
