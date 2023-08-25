import pandas as pd
import matplotlib.pyplot as plt     # for some reason this line is important...

from functions.data_managment.loaders import load_from_txt
from functions.plotters.plotter_CA import plotter_CA_Autolab, plotter_CA_Autolab_assign_cycles
from functions.assigners.assign_cycles_STDP import assign_STDP_states

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data, STDP

    print('\nSTARTING STDP.py script...')
    print('\nThis is more automated script for dealing with STDP data. Please list .txt files from your experiment...')

    # Here you put list of files with STDP data. If it is empty it will ask for path.
    list_filenames = [
        'data/stdp(12)_ratio0to1-tri.txt',
        'data/stdp(19)_ratio5to1-tri.txt',
        'data/stdp(26)_ratio0to1-tri.txt',
        'data/stdp(28)_dev1-el16-ratio6to1.txt',
        'data/stdp(29)_ratio4p5to1-tri.txt',
        'data/stdp(29)_ratio5to1-tri.txt',
        'data/stdp(29)_ratio5to1-tri_a.txt',
        'data/stdp(6)_ratio4p5to1-tri.txt'
    ]

    list_filenames = [
        'data/stdp(29)_ratio5to1-tri_a.txt'
    ]

    V_bias = 0
    V_set = 0.96
    V_reset = -0.96
    V_read = 0.09
    V_err = 0.005

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    for index, filename in enumerate(list_filenames):
        print(f'\n \t ### STARTING LOOP {index + 1} ###\n\nLoading data {index + 1} of {len(list_filenames)} from file {filename}\n')

        # Load the data
        data = load_from_txt(filename)

        data = assign_STDP_states(data, V_bias, V_set, V_reset, V_read, V_err)

        plotter_CA_Autolab_assign_cycles(data, filename)