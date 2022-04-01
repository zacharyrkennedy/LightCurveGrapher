import tkinter as tk
import tkinter.filedialog
import math as m
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import random as r
import numpy as np

# Setup for tkinter
root = tk.Tk()

# Set the window to not be resizeable, add a title to the window and the set the window dimensions
root.resizable(False, False)
root.title("Zack's Light Curve Graphing Tool")
root.geometry("1000x500")
root.configure(bg='white')


def plot():
    fig = Figure(figsize=(5, 4), dpi=100)

    colors = ['red','green','blue','purple']

    t = np.arange(0, 3, .01)
    subplot = fig.add_subplot(111)
    subplot.plot(t, 2 * np.sin(2 * np.pi * t), color=colors[r.randrange(0,3, 1)])
    subplot.set_xlabel("time [s]")
    subplot.set_ylabel("f(t)")
    subplot.set_title("Super cool Plot")

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().place(x=405, y=20)

    #toolbar = NavigationToolbar2Tk(canvas, root)
    #toolbar.update()
    #canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def CalculateData(filepath):

    global jd_list

    df = pd.read_csv(filepath)

    jd_list = df["J.D.-2400000"].tolist()
    source_t1_list = df["Source-Sky_T1"].tolist()
    source_c2_list = df["Source-Sky_C2"].tolist()
    source_c3_list = df["Source-Sky_C3"].tolist()

    if 'Source-Sky_C4' in df:
        source_c4_list = df["Source-Sky_C4"].tolist()
    else:
        source_c4_list = [0]

    if 'Source-Sky_C5' in df:
        source_c5_list = df["Source-Sky_C5"].tolist()
    else:
        source_c5_list = [0]

    if 'Source-Sky_C6' in df:
        source_c6_list = df["Source-Sky_C6"].tolist()
    else:
        source_c6_list = [0]

    t1_mag_dif = []
    t1_app_mag = []

    c2_mag_dif = []
    c2_app_mag = []

    c3_mag_dif = []
    c3_app_mag = []

    c4_mag_dif = []
    c4_app_mag = []

    c5_mag_dif = []
    c5_app_mag = []

    c6_mag_dif = []
    c6_app_mag = []

    total_source_list = [source_t1_list, source_c2_list, source_c3_list, source_c4_list, source_c5_list]
    total_mag_dif = [t1_mag_dif, c2_mag_dif, c3_mag_dif, c4_mag_dif, c5_mag_dif, c6_mag_dif]
    total_app_mag = [t1_app_mag, c2_app_mag, c3_app_mag, c4_app_mag, c5_app_mag, c6_app_mag]

    if source_c5_list[0] == 0:
        total_source_list = [source_t1_list, source_c2_list, source_c3_list, source_c4_list]
        total_mag_dif = [t1_mag_dif, c2_mag_dif, c3_mag_dif, c4_mag_dif]
        total_app_mag = [t1_app_mag, c2_app_mag, c3_app_mag, c4_app_mag]
    elif source_c6_list[0] == 0:
        total_source_list = [source_t1_list, source_c2_list, source_c3_list, source_c4_list, source_c5_list]
        total_mag_dif = [t1_mag_dif, c2_mag_dif, c3_mag_dif, c4_mag_dif, c5_mag_dif]
        total_app_mag = [t1_app_mag, c2_app_mag, c3_app_mag, c4_app_mag, c5_app_mag]
    else:
        total_source_list = [source_t1_list, source_c2_list, source_c3_list, source_c4_list, source_c5_list,
                             source_c6_list]
        total_mag_dif = [t1_mag_dif, c2_mag_dif, c3_mag_dif, c4_mag_dif, c5_mag_dif, c6_mag_dif]
        total_app_mag = [t1_app_mag, c2_app_mag, c3_app_mag, c4_app_mag, c5_app_mag, c6_app_mag]


def check_pick(source_choice, mag_dif_choice, app_mag_choice, mag):

    for i in range(len(jd_list)):
        app_mag_choice.append(mag)

    for i in range(len(app_mag_choice)):
        mag_dif_choice.append(-2.5 * m.log10(source_choice[i] / source_choice[0]))


def browseFile():
    filepath = tk.filedialog.askopenfilename()
    print(filepath)
    filename = print(os.path.basename(filepath))

    return filepath





label = tk.Label(root, text="Zack's Light Curve Graphing Tool", font=("Courier", 14), bg="grey")
label.place(x=15, y=15)
root.columnconfigure(0, weight=1)

instructions = tk.Label(root, text="Welcome! This program takes an excel file of light flux data. \n "
                                  "It graphs a light curve of time vs magnitude.")
instructions.place(x=25, y=55)

button = tk.Button(root, text="Browse File", command=browseFile)
button.place(x=150, y=105)

label_primary_check = tk.Label(root, text="Please select your primary check star:")
label_primary_check.place(x=85, y=143)

selected = tk.StringVar(value=' ')
r2 = tk.Radiobutton(root, text='C2', value='C2', variable=selected)
r3 = tk.Radiobutton(root, text='C3', value='C3', variable=selected)
r4 = tk.Radiobutton(root, text='C4', value='C4', variable=selected)
r5 = tk.Radiobutton(root, text='C5', value='C5', variable=selected)
r6 = tk.Radiobutton(root, text='C6', value='C6', variable=selected)

r2_x = 65

r2.place(x=r2_x, y=175)
r3.place(x=r2_x+50, y=175)
r4.place(x=r2_x+100, y=175)
r5.place(x=r2_x+150, y=175)
r6.place(x=r2_x+200, y=175)


graph_button = tk.Button(root, text="Graph Curve", command=plot)
graph_button.place(x=145, y=285)

# Create label for Planet Name

check_star_mag_label_x = 75
check_star_mag_label = tk.Label(root, text="Check Star Magnitude:")
check_star_mag_label.place(x=check_star_mag_label_x, y=225)

# Create textbox input for Planet Name
check_star_mag_box = tk.Entry(root, width=10, borderwidth=5)
check_star_mag_box.place(x=check_star_mag_label_x+130, y=225)





root.mainloop()
