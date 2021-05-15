'''
@author: Beril Gökçe Çiçek
@task: Write a code for calculating the size of any color image that is defined by the user and
finding transmit time according to the modem that is given by the user.
'''#

import os
import cv2
import tkinter as tk
from tkinter import *
from tkinter import Button
from tkinter import filedialog



class ImageTransmitCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Image Transmission Time Calculator")
        self.window.geometry("400x280")
        canvas = tk.Canvas(self.window, width=400, height=300)
        canvas.pack()
        self.img_arr = []
        self.userInput = tk.Entry(self.window, width=30)
        canvas.create_window(250, 110, window=self.userInput)
        label = tk.Label(self.window, text="Modem speed:")
        label.place(x=50, y=100)
        subInfo = tk.Label(self.window, text="(Mbps)")
        subInfo.place(x=70, y=120)
        self.errorLabel = tk.Label(self.window, text="")
        self.errorLabel.place(x=150, y=80)
        self.buttonLabel = tk.Label(self.window, text="Select to image for calculation")
        self.buttonLabel.place(x=50, y=30)
        selectImgButton = Button(self.window, text="Select an image", command=self.selectImageEvent,
                                 activebackground="#82ccdd", width=12)
        selectImgButton.pack(side=RIGHT, padx="10", pady="10")
        selectImgButton.place(x=250, y=30)
        calculateButton = Button(self.window, text="Calculate speed", command=self.calculatorEvent,
                                 activebackground="#82ccdd", width=12)
        calculateButton.pack(side=RIGHT, padx="10", pady="10")
        calculateButton.place(x=250, y=140)
        self.window.mainloop()

    def selectImageEvent(self):
        path = filedialog.askopenfilename() # get image from device
        fileName = os.path.basename(path)
        if len(path) > 0:
            self.selected_image = cv2.imread(path) # read image
            self.dimensions = self.selected_image.shape # dimensions of the image
            self.height = self.selected_image.shape[0]
            self.width = self.selected_image.shape[1]
            self.channels = len(self.dimensions) # RGB
            self.img_arr.append(self.selected_image)
            if(len(self.img_arr) > 0):
                self.buttonLabel.config(text="'" + fileName + "'" + " selected", width=30, fg='#0000FF')
                self.buttonLabel.update_idletasks()
    def calculatorEvent(self):
        if(self.img_arr == []):
            self.buttonLabel.config(text="Please select a image file", width=30, fg='#ff0000')
            self.buttonLabel.update_idletasks()
        else:
            textInput = self.userInput.get()  # modem speed taken from user
            if(textInput == ""):
                self.errorLabel.config(text="Modem speed is a required field", width=30, fg='#ff0000')
                self.errorLabel.update_idletasks()
            else:
                try:
                    textInput = int(textInput)
                    size = self.width * self.height  # bytes
                    byteToBits = size * (1 + 8 + 1) * 3  # bits
                    mbps = int(textInput) * 1000000  # 1 Mbps = 1.000.000 bits/sec -- convert mbps to baud
                    result = byteToBits / mbps  # bits/(bits/sec) = sec
                    convertMin = result / 60  # convert sec to min
                    convertMin = round(convertMin, 5)
                    self.errorLabel.config(text="", width=30)
                    self.errorLabel.update_idletasks()
                    resultLabel = tk.Label(self.window, text="Time required: ")
                    resultLabel.place(x=50, y=200)
                    outputLabel = tk.Label(self.window, text=str(convertMin) + " min")
                    outputLabel.place(x=130, y=200)
                    dimensionLabel = tk.Label(self.window,
                                              text="Dimension of the image: " + "[" + str(self.height) + "x" +
                                                   str(self.width) + "]")
                    dimensionLabel.place(x=50, y=230)
                    self.userInput.delete(0, 'end')
                except ValueError:
                    self.errorLabel.config(text="Input is invalid", width=30, fg='#ff0000')
                    self.errorLabel.update_idletasks()


gui = ImageTransmitCalculator()
