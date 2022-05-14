import pandas as pd
import math as m
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
from matplotlib.figure import Figure


class LCG:

    def __init__(self):

        self.filepath = ' '

        self.fig = Figure(figsize=(6, 5), dpi=100)

        # Initilize Julian Date list
        self.jd_list = []

        # Initilize Source count lists
        self.source_t1_list = []
        self.source_c2_list = []
        self.source_c3_list = []
        self.source_c4_list = [0]
        self.source_c5_list = [0]
        self.source_c6_list = [0]
        
        # Initilize Magnitiude_Difference & Apparent_Magnitude Columns
        self.t1_mag_dif = []
        self.t1_app_mag = []

        self.c2_mag_dif = []
        self.c2_app_mag = []

        self.c3_mag_dif = []
        self.c3_app_mag = []

        self.c4_mag_dif = []
        self.c4_app_mag = []

        self.c5_mag_dif = []
        self.c5_app_mag = []

        self.c6_mag_dif = []
        self.c6_app_mag = []

        self.checkChoice = 0
        self.choiceMag = 0

    def ConfigureFile(self):

        df = pd.read_csv(self.filepath)

        self.jd_list = df["J.D.-2400000"].tolist()
        self.source_t1_list = df["Source-Sky_T1"].tolist()
        self.source_c2_list = df["Source-Sky_C2"].tolist()
        self.source_c3_list = df["Source-Sky_C3"].tolist()

        if 'Source-Sky_C4' in df:
            self.source_c4_list = df["Source-Sky_C4"].tolist()
        else:
            self.source_c4_list = [0]

        if 'Source-Sky_C5' in df:
            self.source_c5_list = df["Source-Sky_C5"].tolist()
        else:
            self.source_c5_list = [0]

        if 'Source-Sky_C6' in df:
            self.source_c6_list = df["Source-Sky_C6"].tolist()
        else:
            self.source_c6_list = [0]

        self.total_source_list = [self.source_t1_list, self.source_c2_list, self.source_c3_list, self.source_c4_list, self.source_c5_list]
        self.total_mag_dif = [self.t1_mag_dif, self.c2_mag_dif, self.c3_mag_dif, self.c4_mag_dif, self.c5_mag_dif, self.c6_mag_dif]
        self.total_app_mag = [self.t1_app_mag, self.c2_app_mag, self.c3_app_mag, self.c4_app_mag, self.c5_app_mag, self.c6_app_mag]

        if self.source_c5_list[0] == 0:
            self.total_source_list = [self.source_t1_list, self.source_c2_list, self.source_c3_list, self.source_c4_list]
            self.total_mag_dif = [self.t1_mag_dif, self.c2_mag_dif, self.c3_mag_dif, self.c4_mag_dif]
            self.total_app_mag = [self.t1_app_mag, self.c2_app_mag, self.c3_app_mag, self.c4_app_mag]
        elif self.source_c6_list[0] == 0:
            self.total_source_list = [self.source_t1_list, self.source_c2_list, self.source_c3_list, self.source_c4_list, self.source_c5_list]
            self.total_mag_dif = [self.t1_mag_dif, self.c2_mag_dif, self.c3_mag_dif, self.c4_mag_dif, self.c5_mag_dif]
            self.total_app_mag = [self.t1_app_mag, self.c2_app_mag, self.c3_app_mag, self.c4_app_mag, self.c5_app_mag]
        else:
            self.total_source_list = [self.source_t1_list, self.source_c2_list, self.source_c3_list, self.source_c4_list, self.source_c5_list, self.source_c6_list]
            self.total_mag_dif = [self.t1_mag_dif, self.c2_mag_dif, self.c3_mag_dif, self.c4_mag_dif, self.c5_mag_dif, self.c6_mag_dif]
            self.total_app_mag = [self.t1_app_mag, self.c2_app_mag, self.c3_app_mag, self.c4_app_mag, self.c5_app_mag, self.c6_app_mag]

    def process_data(self):

        # Get columns for chosen check star
        source_choice = self.total_source_list[self.checkChoice]
        mag_dif_choice = self.total_mag_dif[self.checkChoice]
        app_mag_choice = self.total_app_mag[self.checkChoice]

        del (self.total_source_list[self.checkChoice])
        del (self.total_mag_dif[self.checkChoice])
        del (self.total_app_mag[self.checkChoice])

        for i in range(len(self.jd_list)):
            app_mag_choice.append(self.choiceMag)

        for i in range(len(app_mag_choice)):
            mag_dif_choice.append(-2.5 * m.log10(source_choice[i] / source_choice[0]))

        for i in range(len(self.total_source_list)):

            source = self.total_source_list[i]
            mag_dif = self.total_mag_dif[i]
            app_mag = self.total_app_mag[i]

            for j in range(len(app_mag_choice)):
                mag_dif.append(-2.5*m.log10(source[j]/source_choice[j]))
                app_mag.append(mag_dif[j]+ float(app_mag_choice[j]))


    def graph_results(self):

        object_name = input("Please enter the name of your object")
        date = input("PLease enter the date the object was observered")

        plt.scatter(self.jd_list, self.c2_app_mag, label="c2 apparent mag.")
        plt.scatter(self.jd_list, self.c3_app_mag, label="c3 apparent mag.")
        plt.scatter(self.jd_list, self.c4_app_mag, label="c4 apparent mag.")

        if self.source_c5_list[0] != 0:
            plt.scatter(self.jd_list, self.c5_app_mag, label="c5 apparent mag.")
        if self.source_c6_list[0] != 0:
            plt.scatter(self.jd_list, self.c6_app_mag, label="c6 apparent mag.")

        plt.scatter(self.jd_list, self.t1_app_mag, label="t1 apparent mag.")

        plt.title(object_name + " Light Curve - " + date)
        plt.xlabel("Time (J.D.)")
        plt.ylabel("Magnitude")

        plt.legend(title='Object Magnititudes', bbox_to_anchor=(1.05, 1.0), loc='upper left')
        plt.tight_layout()

        plt.show()

    def LCG_Plot(self):

        subplot = self.fig.add_subplot(111)

        subplot.scatter(self.jd_list, self.c2_app_mag, label="c2 apparent mag.")
        subplot.scatter(self.jd_list, self.c3_app_mag, label="c3 apparent mag.")
        subplot.scatter(self.jd_list, self.c4_app_mag, label="c4 apparent mag.")

        if self.source_c5_list[0] != 0:
            subplot.scatter(self.jd_list, self.c5_app_mag, label="c5 apparent mag.")
        if self.source_c6_list[0] != 0:
            subplot.scatter(self.jd_list, self.c6_app_mag, label="c6 apparent mag.")

        subplot.scatter(self.jd_list, self.t1_app_mag, label="t1 apparent mag.")

        subplot.legend(title='Object Magnititudes', bbox_to_anchor=(1.05, 1.0), loc='upper left')
        # subplot.tight_layout()

        plt.scatter(self.jd_list, self.c2_app_mag, label="c2 apparent mag.")
        plt.scatter(self.jd_list, self.c3_app_mag, label="c3 apparent mag.")
        plt.scatter(self.jd_list, self.c4_app_mag, label="c4 apparent mag.")

        #plt.show()


    def setCheckChoice(self, choice):
        self.checkChoice = choice

    def setChoiceMag(self, mag):
        self.choiceMag = mag

    def setFilePath(self, fpath):
        self.filepath = fpath

    def getCheckChoice(self):
        return self.checkChoice

    def getChoiceMag(self):
        return self.choiceMag

    def getFilePath(self):
        return self.filepath

    def getFig(self):
        return self.fig

"""

MyLCG = LCG()

MyLCG.setFilePath('measurements6.csv')
MyLCG.ConfigureFile()

CheckChoice = 1
Mag = 8.91

MyLCG.setCheckChoice(CheckChoice)
MyLCG.setChoiceMag(Mag)

MyLCG.process_data()
MyLCG.graph_results()


del(self.total_source_list[choice])
del(self.total_mag_dif[choice])
del(self.total_app_mag[choice])

check_pick(source_choice,mag_dif_choice,app_mag_choice,mag)
process_data(source_choice,mag_dif_choice,app_mag_choice)
graph_results()

"""