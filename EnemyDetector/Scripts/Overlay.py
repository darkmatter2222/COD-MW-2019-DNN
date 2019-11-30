from tkinter import *
import ctypes
import pyautogui
import numpy as np
import tensorflow.keras as keras

# Load Model
model = keras.models.load_model('..\\Models\\CODV4.h5')

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)

root = Tk()
v = StringVar()
flashLabel = Label(root, textvariable=v, background='#ffffff', foreground='red', font=("Helvetica bold", 23), width=400)
flashLabel.pack()

v.set("Woot")

def task():
    while 1 == 1:
        # Grab Screen
        image = pyautogui.screenshot(region=(centerPoint[0] - 100, centerPoint[1] - 100, 200, 200))
        # Predict
        prediction = model.predict(np.asarray([np.asarray(image)]) / 255)
        # Print Result
        if prediction[0][0] > 0.95:
            v.set("Enemy %d" % round(prediction[0][0] * 100, 5))
            flashLabel.update()
        else:
            v.set("")
            flashLabel.update()


root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "#ffffff")
root.configure(background='#ffffff')
root.geometry('%dx%d+%d+%d' % (400, 400, centerPoint[0] - (100 * 1), centerPoint[1] - (300 * 1)))
root.title("Welcome to LikeGeeks app")

root.after(2000, task)
root.mainloop()
