import pandas as pd
import matplotlib.pyplot as plt     # for some reason this line is important...

from functions.data_managment.loaders import load_from_txt
from functions.plotters.plotter_CA import plotter_CA_Autolab, plotter_CA_Autolab_assign_states, plotter_CA_Autolab_assign_read_cycles
from functions.assigners.assign_cycles_STDP import assign_STDP_states,  count_STDP_read_cycles

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data, STDP

    print('\nSTARTING STDP.py script...')
    print('\nThis is more automated script for dealing with STDP data. Please list .txt files from your experiment...')

    # Here you put list of files with STDP data. If it is empty it will ask for path.
    list_filenames = [
        'data_examples/STDP_0.txt',
        'data_examples/STDP_4.txt',
        'data_examples/STDP_9.txt',
        'data_examples/STDP_14.txt',
        'data_examples/STDP_19.txt',
        'data_examples/STDP_24.txt',
        'data_examples/STDP_29.txt'
    ]

    # Hardcoded voltages
    V_bias = 0
    V_set = 1.95
    V_reset = -1.96
    V_read = 0.195
    V_err = 0.05
    # n stands for a number of plateau points (to the left OR right) for assigning states for STDP. More points in CA - higher n.
    n = 30

    plot_CA_raw = False
    plot_CA_assigning = True
    plot_CA_read_cycles = False

    starting_dt = 0.0000  # change if your first file is connected with dt other than 0!!!
    number_of_sequences = 5  # number of sequences to be taken into calculations
    variation = 0.15  # typically you should put +/- 15% variations of the of the signals
    bsl_corr = 0.0000  # adding several uA or mA to the backgoround / USE ONLY IF NECESSARY /  TO DO: change it to average of the backgorund

    STDP = pd.DataFrame({
        'dt/s': pd.Series(dtype='float64'),
        'READ_before': pd.Series(dtype='float64'),
        'READ_after': pd.Series(dtype='float64'),
        'WEIGHT_change': pd.Series(dtype='float64'),
        'filename': pd.Series(dtype='string'),
    })

    print(f'Voltage values are: {V_bias} V for bias, '
          f'{V_read} V for read, '
          f'{V_set} V for positive set, '
          f'{V_reset} V for negative set, '
          f'and {V_err} V for bias voltage.')

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    for index, filename in enumerate(list_filenames):
        print(f'\n \t ### STARTING LOOP {index + 1} ###\n\nLoading data {index + 1} of {len(list_filenames)} from file {filename}\n')

        # Load the data, do poor version of background shifting
        data = load_from_txt(filename, bsl_corr)

        plotter_CA_Autolab(data, filename) if plot_CA_raw == True else None

        # Assign STDP states according to V_ +/- V_err for plateau parts that are "flat" n-points to the left OR right
        data = assign_STDP_states(data, n, V_bias, V_set, V_reset, V_read, V_err)
        plotter_CA_Autolab_assign_states(data, filename, V_bias, V_set, V_reset, V_read, V_err) if plot_CA_assigning == True else None

        # Counting STDP read cycles
        data =  count_STDP_read_cycles(data)
        plotter_CA_Autolab_assign_read_cycles(data, filename, V_bias, V_set, V_reset, V_read, V_err) if plot_CA_read_cycles == True else None