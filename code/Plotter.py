# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 12:30:29 2022

Custom plotter code that will allow for consistant plots and 
universal changes

@author: Administrator
"""

import matplotlib.pyplot as plt

def plotter(_fig_num, _data, _labels):
    
    plt.rcParams.update({'font.size': 22})
    
    plt.figure(_fig_num)
    plt.plot(_data[0], _data[1])
    plt.title(_labels[0])
    plt.ylabel(_labels[1])
    plt.xlabel(_labels[2])
    plt.grid(which='both', axis='both', linestyle=':')
    plt.legend()
