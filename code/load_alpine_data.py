# -*- coding: utf-8 -*-
"""
Created on Sat Aug 13 12:40:25 2022

- RCS data processing from freq domain to time

@author: Administrator
"""

# %% Import Statements
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import os, time, math
from datetime import datetime
from copy import deepcopy

# Pull custom functions
from Build_Directories import build_directories
from User_Message import user_message
from Select_Data import select_data, simple_load, calc_stats
from Plot_Data import plot_polar, plot_rect, plot_contour
from norm_rcs import norm_data
from Extract_Data import extract_data
from Data_Generator import data_generator
from Save_Object import save_object

# Enable ANSI colors
os.system('color')


# %% Main loop body
if __name__ == '__main__':

    now = datetime.now()
    now = now.strftime("%d%b%y")
    plt.close('all')

    ROOT, dir_DATA, dir_FIG = build_directories()

    """ Set Plot Params"""
    polarizations = ['tt', 'pp']
    nP = len(polarizations)
    frequencies = [4.5, 5.5]

    """Select or load data"""
    choose_data = 'n'  #input("Select Data? [y/N]")
    if choose_data == 'y':

        checking_object_type = True
        while checking_object_type:
            object_type = 's'  #input("Are these objects sim [s] or measurement [m]?\n")
            if object_type == 'm' or 's':
                break
            else:
                print("Please choose either 'm' or 's' for data type.\n")
        # End:  Request data type

        entering_object_names = True
        object_names = []
        print("Enter object name, and press enter. Press 'x' to exit \n")
        while entering_object_names:
            obj = input("\t Object Name:  ")
            if obj == 'x':
                break
            object_names.append(obj)
        # End: Request filenames

        RCS_Data = {}
        for i in object_names:
            if object_type == 'm':
                label = 'measured'
            elif object_type == 's':
                label = 'simulated'
            else:
                label = "???"

            _text = "Select " + label + " " + i + " data: \n"
            user_message(_text, "prompt")
            name = i
            obj = select_data(dir_DATA, name=name)
            obj = extract_data(obj, frequencies)
            obj = calc_stats(obj)
            RCS_Data.update({name: obj})
        # End:  store objects to RCS data dictionary

        """ Save Objects"""
        ask_save = input("Save RCS Data dictionary? [y/N] \n")
        if ask_save == 'y':
            object_name = input("Type name for RCS dictionary:\n")
            save_object(RCS_Data, dir_DATA, object_name + '_' + now)
            print("Saved " + object_name + ' as ' + object_name + '_' + now + '\n')

    else:
        RCS_Data = simple_load(dir_DATA)

    """ Plot data """
    call_plots = 'n'  # input('Plot data? [y/N] \n')
    if call_plots == 'y':
        for target in RCS_Data:
            d = RCS_Data[target]
            # plot_contour(d, amp="Nf")
            # plot_contour(d, amp="Na")

            plot_contour(d, amp='Nfs')
            # plot_contour(d, amp='Nas')

            # plot_contour(d, amp="dBm")
            # plot_contour(d, amp="RCS")

        plt.show()

    pack_data = 'y'  # input('Prepare data for the ML model? [y/n] \n')
    if pack_data == 'y':

        # Organize data into simulated, and measured groupings
        simulated_targets = deepcopy(RCS_Data)
        measured_targets = deepcopy(RCS_Data)
        for target in RCS_Data:
            if target[-1] == 'm':
                del simulated_targets[target]
            elif target[-1] == 's':
                del measured_targets[target]
        # END:  data grouping

        # Generate training and test data
        sim_data = data_generator(simulated_targets, polarizations, T=68, aug='Nfs')
        ask_save = input("Save simulated RCS Data ? [y/N] \n")
        if ask_save == 'y':
            object_name = "Sim_Data"  #input("Type name for RCS dictionary:\n")
            save_object(sim_data, dir_DATA, object_name + '_' + now)
            print("Saved " + object_name + ' as ' + object_name + '_' + now + '\n')

        sim_data = data_generator(measured_targets, polarizations, T=68, aug='Nfs')
        ask_save = input("Save measured RCS Data ? [y/N] \n")
        if ask_save == 'y':
            object_name = "Meas_Data"  # input("Type name for RCS dictionary:\n")
            save_object(sim_data, dir_DATA, object_name + '_' + now)
            print("Saved " + object_name + ' as ' + object_name + '_' + now + '\n')


    print('Program complete')

