from tkinter import *
import ctypes
import pyautogui
import numpy as np
import tensorflow.keras as keras
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageTk

# Load Model
model = keras.models.load_model('..\\Models\\CODV6.h5')

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)

root = Tk()
v = StringVar()
flashLabel = Label(root, textvariable=v, background='black', foreground='red', font=("Helvetica bold", 50), width=1000)
flashLabel.pack()

c = StringVar()
infoLabel = Label(root, textvariable=c, background='black', foreground='red', font=("Helvetica bold", 25))
infoLabel.place(x=225, y=200)
infoLabel.pack()

d = StringVar()
infoLabel = Label(root, textvariable=d, background='black', foreground='red', font=("Helvetica bold", 25))
infoLabel.place(x=225, y=200)
infoLabel.pack()

v.set("Initializing...")
c.set('<= What is seen by the neural network')
d.set('Last highest seen by neural network =>')

def task():
    last100Image = None
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

        if last100Image is None:
            last100Image = image

        # Predict
        prediction = model.predict(np.asarray([np.asarray(image)]) / 255)
        # Print Result
        v.set("Enemy Confidence " + str(round(prediction[0][0] * 100)).zfill(3) + '%')
        predictionPercent = round(prediction[0][0] * 100, 2)

        r = 0
        g = 255
        b = 0
        if predictionPercent > 1:
            r = int((255*predictionPercent)/100)
            g = int(255-((255*predictionPercent)/100))
            b = 0

        flashLabel.configure(foreground="#%02x%02x%02x" % (r, g, b))
        flashLabel.update()

        if predictionPercent == 100:
            last100Image = image

        render = ImageTk.PhotoImage(image)
        img = Label(image=render)
        img.image = render
        img.place(x=0, y=100)

        render2 = ImageTk.PhotoImage(last100Image)
        img100 = Label(image=render2)
        img100.image = render2
        img100.place(x=896, y=100)






root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "#ffffff")
root.configure(background='#ffffff')
root.geometry('%dx%d+%d+%d' % (1100, 1100, centerPoint[0] - (500 * 1), centerPoint[1] - (500 * 1)))
root.title("Welcome to LikeGeeks app")

root.after(2000, task)
root.mainloop()
