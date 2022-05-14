import tkinter as tk
import tkinter.filedialog
import math as m
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from PIL import Image, ImageTk
import random as r
import numpy as np
import LCGLib
from PIL import Image, ImageTk

# Setup for tkinter
root = tk.Tk()

#Setup for LCGLib
myLCG = LCGLib.LCG()

# Set the window to not be resizeable, add a title to the window and the set the window dimensions
root.resizable(False, False)
root.title("KTPO Light Curve Graphing Tool")
root.geometry("450x450")
root.configure(bg='white')

def plotLightCurve():

    myLCG.setCheckChoice(int(checkStarChoice.get()))
    myLCG.setChoiceMag(check_star_mag_box.get())

    myLCG.ConfigureFile()
    myLCG.process_data()

    myLCG.LCG_Plot()


    canvas = FigureCanvasTkAgg(myLCG.getFig(), master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().place(x=405, y=20)



def browseFile():

    global filepath

    filepath = tk.filedialog.askopenfilename()

    myLCG.setFilePath(filepath)
    print(myLCG.getFilePath())

    return filepath

def graphSettings():

    def applySettings():
        print("Settings applied!")

    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(root)

    newWindow.resizable(False, False)
    graph_settings.config(state='disable')

    # sets the title of the
    newWindow.title("Graph Settings")

    # sets the geometry of toplevel
    newWindow.geometry("300x320")

    graphSettingsLabel = tk.Label(newWindow, text="Graph Settings", font=("Courier 14 bold"))
    graphSettingsLabel.place(x=70, y=25)

    # Create label for Graph Title
    graphTitleLabel = tk.Label(newWindow, text="Graph Title")
    graphTitleLabel.place(x=35, y=80)

    # Create textbox input for Graph Title
    graphTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    graphTitleBox.place(x=60, y=105)

    # Create label for Graph Title
    xTitleLabel = tk.Label(newWindow, text="X-axis Title")
    xTitleLabel.place(x=35, y=140)

    # Create textbox input for Graph Title
    xTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    xTitleBox.place(x=60, y=165)

    # Create label for Graph Title
    yTitleLabel = tk.Label(newWindow, text="Y-axis Title")
    yTitleLabel.place(x=35, y=210)

    # Create textbox input for Graph Title
    yTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    yTitleBox.place(x=60, y=235)

    #Apply Button
    applyButton = tk.Button(newWindow, text="Apply", command=applySettings)
    applyButton.place(x=105, y=280)

    #Cancel Button
    cancelButton = tk.Button(newWindow, text="Cancel")
    cancelButton.place(x=155, y=280)

    def quit_win():
        newWindow.destroy()
        graph_settings.config(state='normal')





    newWindow.protocol("WM_DELETE_WINDOW", quit_win)


label = tk.Label(root, text="KTPO Light Curve Graphing Tool", font=("Courier", 14), bg="grey")
label.place(x=55, y=15)
root.columnconfigure(0, weight=1)

instructions = tk.Label(root, text="Welcome! This program takes an excel file of light flux data. \n "
                                  "It graphs a light curve of time vs magnitude.")
instructions.place(x=65, y=55)

button = tk.Button(root, text="Browse File", command=browseFile)
button.place(x=190, y=115)

label_primary_check = tk.Label(root, text="Please select your primary check star:")
label_primary_check.place(x=125, y=168)

checkStarChoice = tk.StringVar(value=1)
r2 = tk.Radiobutton(root, text='C2', value=1, variable=checkStarChoice)
r3 = tk.Radiobutton(root, text='C3', value=2, variable=checkStarChoice)
r4 = tk.Radiobutton(root, text='C4', value=3, variable=checkStarChoice)
r5 = tk.Radiobutton(root, text='C5', value=4, variable=checkStarChoice)
r6 = tk.Radiobutton(root, text='C6', value=5, variable=checkStarChoice)

r2_x = 105
r2_y = 200

r2.place(x=r2_x, y=r2_y)
r3.place(x=r2_x+50, y=r2_y)
r4.place(x=r2_x+100, y=r2_y)
r5.place(x=r2_x+150, y=r2_y)
r6.place(x=r2_x+200, y=r2_y)


graph_button = tk.Button(root, text="Graph Curve", command=plotLightCurve)
graph_button.place(x=185, y=310)

# Graph Settings Button
gearIcon = tk.PhotoImage(file = 'images/gear_icon.png')
gearIcon.zoom(8,8)


graph_settings = tk.Button(root, image=gearIcon, command=graphSettings)
graph_settings.place(x=275, y=310)

# Create label for Planet Name

check_star_mag_label_x = 115
check_star_mag_label = tk.Label(root, text="Check Star Magnitude:")
check_star_mag_label.place(x=check_star_mag_label_x, y=250)

# Create textbox input for Planet Name
check_star_mag_box = tk.Entry(root, width=10, borderwidth=5)
check_star_mag_box.place(x=check_star_mag_label_x+130, y=250)

root.mainloop()
