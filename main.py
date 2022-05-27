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


# Setup for tkinter
root = tk.Tk()


# Set the window to not be resizeable, add a title to the window and the set the window dimensions
root.resizable(False, False)
root.title("KTPO Light Curve Graphing Tool")
root.geometry("450x450")
root.configure(bg='white')

# This function plots our graph
def plotGraph():

    # Disable the "graph" button. This is so it can't be clicked again, opening multiple graphs
    graph_button.config(state='disable')

    # Disable the "gear" button
    graph_settings.config(state='disable')

    #Use pandas to make a dataframe with our filepath
    df = pd.read_csv(filepath)

    # Create some lists using column titles from our dataframe
    jd_list = df["J.D.-2400000"].tolist()
    source_t1_list = df["Source-Sky_T1"].tolist()
    source_c2_list = df["Source-Sky_C2"].tolist()
    source_c3_list = df["Source-Sky_C3"].tolist()

    # Check to see how many check stars we have up to 6, and adjust accordingly
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

    # Making our magnitude difference and apparent magnititude lists
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

    # A list of our lists
    total_source_list = [source_t1_list, source_c2_list, source_c3_list, source_c4_list, source_c5_list]
    total_mag_dif = [t1_mag_dif, c2_mag_dif, c3_mag_dif, c4_mag_dif, c5_mag_dif, c6_mag_dif]
    total_app_mag = [t1_app_mag, c2_app_mag, c3_app_mag, c4_app_mag, c5_app_mag, c6_app_mag]

    # Adjusting total list based on how many check stars there are
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

    def process_data(source_choice, mag_dif_choice, app_mag_choice):

        for i in range(len(total_source_list)):

            source = total_source_list[i]
            mag_dif = total_mag_dif[i]
            app_mag = total_app_mag[i]

            for j in range(len(app_mag_choice)):
                mag_dif.append(-2.5 * m.log10(source[j] / source_choice[j]))
                # print(app_mag_choice[j])
                app_mag.append(mag_dif[j] + app_mag_choice[j])
                # print(mag_dif[j]+app_mag_choice[j])

    def graph_results():

        plt.scatter(jd_list, c2_app_mag, label="c2 apparent mag.")
        plt.scatter(jd_list, c3_app_mag, label="c3 apparent mag.")
        plt.scatter(jd_list, c4_app_mag, label="c4 apparent mag.")

        if source_c5_list[0] != 0:
            plt.scatter(jd_list, c5_app_mag, label="c5 apparent mag.")
        if source_c6_list[0] != 0:
            plt.scatter(jd_list, c6_app_mag, label="c6 apparent mag.")

        plt.scatter(jd_list, t1_app_mag, label="t1 apparent mag.")

        plt.legend(title='Object Magnititudes', bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()

        plt.show()

    choice = int(checkStarChoice.get())
    mag = float(check_star_mag_box.get())

    source_choice = total_source_list[choice]
    mag_dif_choice = total_mag_dif[choice]
    app_mag_choice = total_app_mag[choice]

    del (total_source_list[choice])
    del (total_mag_dif[choice])
    del (total_app_mag[choice])

    check_pick(source_choice, mag_dif_choice, app_mag_choice, mag)
    process_data(source_choice, mag_dif_choice, app_mag_choice)
    graph_results()

    if plt.fignum_exists(100):
        pass
    else:
        graph_button.config(state='normal')
        graph_settings.config(state='normal')


# browseFile is a function linked to the "browse" button in the program. It gets the filepath
def browseFile():

    global filepath

    filepath = tk.filedialog.askopenfilename()


    return filepath

# Function attached to the "gear" button on the program
def graphSettings():

    # Code attached to the "Apply" button
    def applySettings():

        plt.xlabel(str(xTitleBox.get()))
        plt.ylabel(str(yTitleBox.get()))
        plt.title(str(graphTitleBox.get()))
        newWindow.destroy()
        graph_settings.config(state='normal')
        graph_button.config(state='normal')

    # When the window is closed, return the "gear" button to it's normal state
    def quit_win():
        newWindow.destroy()
        graph_settings.config(state='normal')
        graph_button.config(state='normal')

    # Code to make a seperate window
    newWindow = tk.Toplevel(root)

    # Make it so our new window isn't resizeable
    newWindow.resizable(False, False)

    # Disable the "gear" button. This is so it can't be clicked again, opening multiple settings windows
    graph_settings.config(state='disable')

    # Disable the "graph" button. This is so it can't be clicked again, opening multiple graphs
    graph_button.config(state='disable')

    # sets the title of the window
    newWindow.title("Graph Settings")

    # sets the size of the window
    newWindow.geometry("300x320")

    # Creates and places the label header for the window
    graphSettingsLabel = tk.Label(newWindow, text="Graph Settings", font=("Courier 14 bold"))
    graphSettingsLabel.place(x=70, y=25)

    # Create label for Graph Title
    graphTitleLabel = tk.Label(newWindow, text="Graph Title")
    graphTitleLabel.place(x=35, y=80)

    # Create textbox input for Graph Title
    graphTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    graphTitleBox.place(x=60, y=105)

    # Create label for X-axis Title
    xTitleLabel = tk.Label(newWindow, text="X-axis Title")
    xTitleLabel.place(x=35, y=140)

    # Create textbox input for x-axis input
    xTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    xTitleBox.place(x=60, y=165)

    #Create label for Y-axis Title
    yTitleLabel = tk.Label(newWindow, text="Y-axis Title")
    yTitleLabel.place(x=35, y=210)

    # Create textbox input for Y-axis input box
    yTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    yTitleBox.place(x=60, y=235)

    #Apply Button
    applyButton = tk.Button(newWindow, text="Apply", command=applySettings)
    applyButton.place(x=105, y=280)

    #Cancel Button
    cancelButton = tk.Button(newWindow, text="Cancel", command=quit_win)
    cancelButton.place(x=155, y=280)



    # Calls the quit_win function when the window is closed.
    newWindow.protocol("WM_DELETE_WINDOW", quit_win)

# Create a title label for the main window, then place it
label = tk.Label(root, text="KTPO Light Curve Graphing Tool", font=("Courier", 14), bg="grey")
label.place(x=55, y=15)
root.columnconfigure(0, weight=1)

# Add the instructions and place them
instructions = tk.Label(root, text="Welcome! This program takes an excel file of light flux data. \n "
                                  "It graphs a light curve of time vs magnitude.")
instructions.place(x=65, y=55)

# Add a button to browse for files, and place it
button = tk.Button(root, text="Browse File", command=browseFile)
button.place(x=190, y=115)

# Add label for primary check star info
label_primary_check = tk.Label(root, text="Please select your primary check star:")
label_primary_check.place(x=125, y=168)

# Radio buttons selecton for check stars
checkStarChoice = tk.StringVar(value=1)
r2 = tk.Radiobutton(root, text='C2', value=1, variable=checkStarChoice)
r3 = tk.Radiobutton(root, text='C3', value=2, variable=checkStarChoice)
r4 = tk.Radiobutton(root, text='C4', value=3, variable=checkStarChoice)
r5 = tk.Radiobutton(root, text='C5', value=4, variable=checkStarChoice)
r6 = tk.Radiobutton(root, text='C6', value=5, variable=checkStarChoice)

# Variables to set the position of the r2 radio button
r2_x = 105
r2_y = 200

# Place all of the radio buttons relative to r2
r2.place(x=r2_x, y=r2_y)
r3.place(x=r2_x+50, y=r2_y)
r4.place(x=r2_x+100, y=r2_y)
r5.place(x=r2_x+150, y=r2_y)
r6.place(x=r2_x+200, y=r2_y)

# "graph" button
graph_button = tk.Button(root, text="Graph Curve", command=plotGraph)
graph_button.place(x=150, y=310)

# Gear Icon info
gearIcon = tk.PhotoImage(file = 'images/gear_icon.png')
gearIcon.zoom(8,8)

# Gear Button
graph_settings = tk.Button(root, image=gearIcon, command=graphSettings)
graph_settings.place(x=240, y=310)

# Check star mag label
check_star_mag_label_x = 115
check_star_mag_label = tk.Label(root, text="Check Star Magnitude:")
check_star_mag_label.place(x=check_star_mag_label_x, y=250)

# Check star mag box and placed
check_star_mag_box = tk.Entry(root, width=10, borderwidth=5)
check_star_mag_box.place(x=check_star_mag_label_x+130, y=250)

# Run program
root.mainloop()
