from tkinter import *

class messaje:
    def __init__(self, marco, text, color):
        messaje = Label(marco, text=text, fg=color)
        messaje.grid(column=2, row=1)