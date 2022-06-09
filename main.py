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
from idlelib.tooltip import Hovertip

__author__ = 'Zachary Kennedy'
__credits__ = ['WSU KTPO Research Group ']
__license__ = 'Open Source'
__version__ = '1.0'
__maintainer__ = 'Zachary Kennedy'
__email__ = 'zacharykennedy@mail.weber.edu'
__status__ = 'early development'

_AppName_ = 'KTPO Light Curve Graphing Tool'

# Setup for tkinter
root = tk.Tk()

# Set the window to not be resizeable, add a title to the window and the set the window dimensions
root.resizable(False, False)
root.title("KTPO Light Curve Graphing Tool")
root.geometry("520x560")
root.iconbitmap("images/LOGOICO.ico")

# Set our background image and place it
backgroundImage=tk.PhotoImage(file = 'images/spacebackground.png')
backgroundImageLabel=tk.Label(root, image=backgroundImage)
backgroundImageLabel.place(x=0,y=0)

# Make a white box to put over the background
canvas = tk.Canvas(root, width=400,height=440)
canvas.configure(bg='white')
canvas.place(x=60, y=60)


# This function plots our graph
def plotGraph():

    # Split the path up
    split_path = os.path.splitext(filepath)

    # Set the variable fileType equal to the .filetype part of our split path
    fileType = split_path[1]

    # Checks to see if our filetype is a .csv file
    if fileType != ".csv":
        messageLabel.config(text="ERROR: Could not graph. Unsupported file type")
    else:
        # Disable the "graph" button. This is so it can't be clicked again, opening multiple graphs
        graph_button.config(state='disable')

        # Disable the "gear" button
        graph_settings.config(state='disable')

        # Use pandas to make a dataframe with our filepath
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

            # Split the filename and the extension
            def uniquify(path):
                filename, extension = os.path.splitext(path)
                counter = 2

                # Increment the number at the end of filename when a file with the same name already exists
                while os.path.exists(path):
                    path = filename + str(counter) + extension
                    counter += 1

                return path

            # Plot c2 to c4
            plt.scatter(jd_list, c2_app_mag, label="c2 apparent mag.")
            plt.scatter(jd_list, c3_app_mag, label="c3 apparent mag.")
            plt.scatter(jd_list, c4_app_mag, label="c4 apparent mag.")

            # Plot c5 and c6 if applicaable
            if source_c5_list[0] != 0:
                plt.scatter(jd_list, c5_app_mag, label="c5 apparent mag.")
            if source_c6_list[0] != 0:
                plt.scatter(jd_list, c6_app_mag, label="c6 apparent mag.")

            # Plot our target star
            plt.scatter(jd_list, t1_app_mag, label="t1 apparent mag.")

            # Plot the legend
            plt.legend(title='Object Magnititudes', bbox_to_anchor=(1.05, 1.0), loc='upper left')
            plt.tight_layout()

            # Checks to see if the user is in quicksave mode or not
            try:
                if var.get() == 0:
                    plt.show()
                elif var.get() == 1:
                    desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                    imagePath = desktopPath + '/graph.png'

                    imagePath = uniquify(imagePath)

                    plt.savefig(imagePath)
                    plt.clf()
                    #print(desktopPath)
            except NameError:
                plt.show()

        # Sets the users chosen choice star and it's magnitude
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

        # If the plot is still open, don't let the user graph again until it is closed
        if plt.fignum_exists(100):
            pass
        else:
            graph_button.config(state='normal')
            graph_settings.config(state='normal')

# Create a label for our feedback messages
messageLabel = tk.Label(root)

# browseFile is a function linked to the "browse" button in the program. It gets the filepath
def browseFile():
    global filepath

    # Set our filepath variable equal to the file the user chooses
    filepath = tk.filedialog.askopenfilename()

    split_path = os.path.splitext(filepath)
    fileType = split_path[1]

    # If the filepath isn't a .csv file then show an error
    if fileType != ".csv":
        messageLabel.config(text="ERROR: filetype " + fileType + " is not supported", foreground='red')
        messageLabel.place(x=160, y=400)
        graph_button.config(state='disable')
        graph_settings.config(state='disable')
    elif fileType == ".csv":
        messageLabel.config(text="File: " + os.path.basename(filepath), foreground='black')
        messageLabel.place(x=180, y=400)
        graph_settings.config(state='normal')
        graph_button.config(state='normal')


        # Create a temporary dataframe for our file
        tempDF = pd.read_csv(filepath)

        # Check and see how many check stars there are, and unlock accordingly
        if 'Source-Sky_C6' in tempDF:
            r2.config(state='normal')
            r3.config(state='normal')
            r4.config(state='normal')
            r5.config(state='normal')
            r6.config(state='normal')
        elif 'Source-Sky_C5' in tempDF:
            r2.config(state='normal')
            r3.config(state='normal')
            r4.config(state='normal')
            r5.config(state='normal')
        elif 'Source-Sky_C4' in tempDF:
            r2.config(state='normal')
            r3.config(state='normal')
            r4.config(state='normal')
        else:
            r2.config(state='normal')
            r3.config(state='normal')


    return filepath


# Function attached to the "gear" button on the program
def graphSettings():
    global var


    # Code attached to the "Apply" button
    def applySettings():
        plt.xlabel(str(xTitleBox.get()))
        plt.ylabel(str(yTitleBox.get()))
        plt.title(str(graphTitleBox.get()))

        graph_settings.config(state='normal')

        # Change the text of the graph button depending on if quick save mode is enabled
        if var.get() == 1:
            graph_button.config(text="Save")
        if var.get() == 0:
            graph_button.config(text="Graph Curve")

        graph_button.config(state='normal')

        newWindow.destroy()


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
    newWindow.geometry("300x400")

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

    # Create label for Y-axis Title
    yTitleLabel = tk.Label(newWindow, text="Y-axis Title")
    yTitleLabel.place(x=35, y=210)

    # Create textbox input for Y-axis input box
    yTitleBox = tk.Entry(newWindow, width=30, borderwidth=5)
    yTitleBox.place(x=60, y=235)

    var = tk.IntVar()
    quickSave = tk.Checkbutton(newWindow, text="Quick Save", variable=var)
    quickSave.place(x=90, y=280)
    quickSave_tip = Hovertip(quickSave, 'Disables dynamic graphing and automatically saves graph image to your system')

    # Apply Button
    applyButton = tk.Button(newWindow, text="Apply", command=applySettings)
    applyButton.place(x=105, y=350)

    # Cancel Button
    cancelButton = tk.Button(newWindow, text="Cancel", command=quit_win)
    cancelButton.place(x=155, y=350)

    # Calls the quit_win function when the window is closed.
    newWindow.protocol("WM_DELETE_WINDOW", quit_win)

img = ImageTk.PhotoImage(Image.open("images/LOGO6.png"))
panel = tk.Label(root, image = img, borderwidth=0, background='white')
panel.place(x=60, y=70)
#panel.pack(pady=45)

# Create a title label for the main window, then place it
#label = tk.Label(root, text="KTPO Light Curve Graphing Tool", font=("Courier", 14), bg="grey")
#label.place(x=55, y=15)
root.columnconfigure(0, weight=1)

# Add the instructions and place them
#instructions = tk.Label(root, text="Welcome! This program takes an .csv file of light flux data, \n "
                              #     "graphing a light curve of time vs magnitude.")
#instructions.place(x=95, y=145)
#instructions.pack()

# Add a button to browse for files, and place it
button = tk.Button(root, text="Browse File", command=browseFile)
button.pack(pady=190)
#button.place(x=220, y=205)
button_tip = Hovertip(button,'Browse for a file. Only .csv files are supported')


# Add label for primary check star info
label_primary_check = tk.Label(root, text="Please select your primary check star:")
label_primary_check.place(x=155, y=238)
#label_primary_check.pack()

# Radio buttons selecton for check stars
checkStarChoice = tk.StringVar(value=1)
r2 = tk.Radiobutton(root, text='C2', value=1, variable=checkStarChoice, state='disable')
r3 = tk.Radiobutton(root, text='C3', value=2, variable=checkStarChoice, state='disable')
r4 = tk.Radiobutton(root, text='C4', value=3, variable=checkStarChoice, state='disable')
r5 = tk.Radiobutton(root, text='C5', value=4, variable=checkStarChoice, state='disable')
r6 = tk.Radiobutton(root, text='C6', value=5, variable=checkStarChoice, state='disable')

# Variables to set the position of the r2 radio button
r2_x = 145
r2_y = 270

# Place all of the radio buttons relative to r2
r2.place(x=r2_x, y=r2_y)
r3.place(x=r2_x + 50, y=r2_y)
r4.place(x=r2_x + 100, y=r2_y)
r5.place(x=r2_x + 150, y=r2_y)
r6.place(x=r2_x + 200, y=r2_y)



# "graph" button
graph_button = tk.Button(root, text="Graph Curve", command=plotGraph)
graph_button.place(x=190, y=445)
#graph_button.pack()

# Gear Icon info
gearIcon = tk.PhotoImage(file='images/gear_icon.png')
gearIcon.zoom(8, 8)


# Gear Button
graph_settings = tk.Button(root, image=gearIcon, command=graphSettings, state='disable')
graph_settings.place(x=280, y=445)
#graph_settings.pack()
graph_settings_tip = Hovertip(graph_settings,'Opens a menu to customize your graph')

# Check star mag label
check_star_mag_label_x = 145
check_star_mag_label = tk.Label(root, text="Check Star Magnitude:")
check_star_mag_label.place(x=check_star_mag_label_x, y=340)
#check_star_mag_label.pack()

# Check star mag box and placed
check_star_mag_box = tk.Entry(root, width=10, borderwidth=5)
check_star_mag_box.place(x=check_star_mag_label_x + 130, y=340)
#check_star_mag_box.pack()
check_star_mag_box_tip = Hovertip(check_star_mag_box,'Enter the magnitude of your primary check star')

def quit_me():
    root.quit()
    root.destroy()

# Disable the "graph" button. This is so it can't be clicked again, opening multiple graphs
graph_button.config(state='disable')

# Disable the "gear" button
graph_settings.config(state='disable')

# Run program
root.mainloop()


