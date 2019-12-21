from tkinter import *
import ctypes
import pyautogui
import numpy as np
import tensorflow.keras as keras
from datetime import datetime
from datetime import timedelta
from PIL import Image, ImageTk, ImageDraw
import json

# Load Model
model = keras.models.load_model('E:\\Projects\\COD Head Spotter\\Models\\MultiClassV2.h5')

# Classes
classesOrigional = json.loads(open('E:\\Projects\\COD Head Spotter\\Models\\Classes.json').read())
classes = {}

for cl in classesOrigional:
    classes[classesOrigional[cl]] = cl

# Find Center Of Screen
user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
centerPoint = tuple(i/2 for i in screenSize)

root = Tk()
v = StringVar()
flashLabel = Label(root, textvariable=v, background='black', foreground='red', font=("Helvetica bold", 10), width=1000)
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
c.set('')
d.set('')

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
        v.set(f'Classified as: {classes[np.argmax(prediction)]} with {round(prediction[0][np.argmax(prediction)] * 100, 2)} Confidence')
        predictionPercent = round(prediction[0][0] * 100, 2)

        flashLabel.update()

        try:
            draw = ImageDraw.Draw(image)

            finalClassification = classes[np.argmax(prediction)]
            if finalClassification != 'Unknown' and finalClassification != 'Neutral':
                splitString = finalClassification.split('-')
                col = (int(splitString[0].replace('COL', '')) * 20) + 10
                row = (int(splitString[1].replace('ROW', '')) * 20) + 10
                draw.line(
                    (0,
                     row,
                    200,
                     row),
                    fill=128, width=5)
                draw.line(
                    (col,
                     0,
                    col,
                     200),
                    fill=128, width=5)
                if round(prediction[0][np.argmax(prediction)] * 100, 2) > 5:
                    last100Image = image



            render = ImageTk.PhotoImage(image)
            img = Label(image=render)
            img.image = render
            img.place(x=0, y=100)

            render2 = ImageTk.PhotoImage(last100Image)
            img100 = Label(image=render2)
            img100.image = render2
            img100.place(x=896, y=100)
        except:
            print('error')






root.overrideredirect(True)
root.attributes('-topmost', True)
root.wm_attributes("-transparentcolor", "#ffffff")
root.configure(background='#ffffff')
root.geometry('%dx%d+%d+%d' % (1100, 1100, centerPoint[0] - (500 * 1), centerPoint[1] - (500 * 1)))
root.title("Welcome to LikeGeeks app")

root.after(2000, task)
root.mainloop()
