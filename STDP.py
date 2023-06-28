import os

import pandas as pd
import numpy as np
from functions.data_managment.loaders import *
from functions.data_managment.savers import saver_data_STDP, saver_STDP
from functions.assigners.assign_cycles_STDP import assign_STDP_cycles
import csv
from functions.extractors.extract_STDP import extract_STDP
from functions.plotters.plotter_SRDP import plotter_SRDP_CA_assigning_cycles, plotter_SRDP_I_vs_peak, plotter_SRDP_reads_peaks_dt

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data, STDP
    print('\nSTARTING STDP.py script...')
    print('\nThis is more automated script for dealing with STDP data. Please list .txt files from your experiment...')

    # Here you put list of files with STDP data. If it is empty it will ask for path.
    list_filenames = [

        # 'data/stdp-exp02(1).txt',
        # 'data/stdp-exp02.txt',
        # 'data/stdp-exp02(3).txt',
        # 'data/exp01_stdp(1).txt',


        'data/STDP-EXP1-(41).txt',
        'data/STDP-EXP1-(42).txt',
        'data/STDP-EXP1-(43).txt',
        'data/STDP-EXP1-(44).txt',
        'data/STDP-EXP1-(45).txt',
        'data/STDP-EXP1-(46).txt',
        'data/STDP-EXP1-(47).txt',
        'data/STDP-EXP1-(48).txt',
        'data/STDP-EXP1-(49).txt',
        'data/STDP-EXP1-(50).txt',
        'data/STDP-EXP1-.txt',
        'data/STDP-EXP1-(1).txt',
        'data/STDP-EXP1-(2).txt',
        'data/STDP-EXP1-(3).txt',
        'data/STDP-EXP1-(4).txt',
        'data/STDP-EXP1-(5).txt',
        'data/STDP-EXP1-(6).txt',
        'data/STDP-EXP1-(7).txt',
        'data/STDP-EXP1-(8).txt',
        'data/STDP-EXP1-(9).txt',
        'data/STDP-EXP1-(10).txt',
        'data/STDP-EXP1-(11).txt',
        'data/STDP-EXP1-(12).txt',
        'data/STDP-EXP1-(13).txt',
        'data/STDP-EXP1-(14).txt',
        'data/STDP-EXP1-(15).txt',
        'data/STDP-EXP1-(16).txt',
        'data/STDP-EXP1-(17).txt',
        'data/STDP-EXP1-(18).txt',
        'data/STDP-EXP1-(19).txt',
        'data/STDP-EXP1-(20).txt',
        'data/STDP-EXP1-(21).txt',
        'data/STDP-EXP1-(22).txt',
        'data/STDP-EXP1-(23).txt',
        'data/STDP-EXP1-(24).txt',
        'data/STDP-EXP1-(25).txt',
        'data/STDP-EXP1-(26).txt',
        'data/STDP-EXP1-(27).txt',
        'data/STDP-EXP1-(28).txt',
        'data/STDP-EXP1-(29).txt',
        'data/STDP-EXP1-(30).txt',
        'data/STDP-EXP1-(31).txt',
        'data/STDP-EXP1-(32).txt',
        'data/STDP-EXP1-(33).txt',
        'data/STDP-EXP1-(34).txt',
        'data/STDP-EXP1-(35).txt',
        'data/STDP-EXP1-(36).txt',
        'data/STDP-EXP1-(37).txt',

    ]

    #initialization of variables
    save_data = None
    save_STDP = None
    save_reads = None
    save_resets = None
    plot_assigning = None
    plot_I_vs_peak = None
    plot_STDP_dt = None

    #The following variables need to be commented/uncommented
    save_data = True
    save_STDP = True
    save_reads = True
    save_resets = True

    # plot_assigning = True
    # plot_I_vs_peak = True
    # plot_STDP_dt = True

    # Here you can hardcode your voltages - for the STDP ot is obligatory (for now - 06.2023)
    # hardcoded_bias_V = None
    # hardcoded_read_V = None
    # hardcoded_stdp1_V = None
    # hardcoded_stdp2_V = None
    # hardcoded_reset_V = None
    hardcoded_bias_V = 0
    hardcoded_read_V = 0.05
    hardcoded_stdp1_V = -0.3
    hardcoded_stdp2_V = 0.3
    hardcoded_reset_V = +0.5

    variation = 0.1 # typically you should put +/- 10% variations of the of the signals

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    STDP = pd.DataFrame({
        'dt/s': pd.Series(dtype='float64'),
        'READ_before': pd.Series(dtype='float64'),
        'READ_after': pd.Series(dtype='float64'),
        'WEIGHT_change': pd.Series(dtype='float64'),
        'filename': pd.Series(dtype='string'),
    })

    for index, filename in enumerate(list_filenames):
        print(f'\n \t ### STARTING LOOP {index + 1} ###\n\nLoading data {index + 1} of {len(list_filenames)} from file {filename}\n')

        # Load the data
        data = load_from_txt(filename)
        # print(data)

        if len(data) == 0:
            print('\033[93m' + f'\nNo data found for {filename}. Skipping...\n' + '\x1b[0m. Did you put proper VOLTAGE parameters?')
            continue


        # this is yet to be changed - the .unique() method is not needed here
        # get voltages or use hardcoded values (for STDP is actually only the second option - hardcoded values)
        bias_V = data['WE(1).Potential (V)'].unique()[0] if hardcoded_bias_V == None else hardcoded_bias_V
        read_V = data['WE(1).Potential (V)'].unique()[1] if hardcoded_read_V == None else hardcoded_read_V
        stdp1_V = data['WE(1).Potential (V)'].unique()[2] if hardcoded_stdp1_V == None else hardcoded_stdp1_V
        stdp2_V = data['WE(1).Potential (V)'].unique()[3] if hardcoded_stdp2_V == None else hardcoded_stdp2_V
        reset_V = data['WE(1).Potential (V)'].unique()[4] if hardcoded_reset_V == None else hardcoded_reset_V

        print(f'Voltage values are: {bias_V} V for bias, '
              f'{read_V} V for read, '
              f'{stdp1_V} V for stdp1, '
              f'{stdp2_V} V for stdp2, '
              f'and {reset_V} V for reset.')


        # Assign STDP cycles for reset peaks - after SECOND Reset peak the data will be taken further to calculations. Only after second peak we have 100% probability taht the peak was executed in full.

        cycle_name = 'reset_cycle'
        data = assign_STDP_cycles(data, variation, reset_V, cycle_name)
        peaks = data[data[cycle_name].notna()]  # show only peaks for reset cycles
        # print('RESET peaks: ', peaks)

        if save_resets == True:
            prefix = "reset_peaks_"

            #making folder for saving RESETs
            folder_name = filename.replace("/", " ").split()[0] + "/" + prefix +"/"
            os.makedirs(folder_name, exist_ok=True)


            output_filename = filename.replace("/", " ").split()[0] + "/" + prefix +"/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
            print(f'\n Saving RESET peaks as {output_filename}')

            with open(output_filename, 'w', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["Peak Index", "Corrected time", "WE(1).Potential (V)", "WE(1).Current (A)"])
                for i in range(len(peaks)):
                    writer.writerow([peaks.index[i],
                                     peaks['Corrected time (s)'].values[i],
                                     peaks['WE(1).Potential (V)'].values[i],
                                     peaks['WE(1).Current (A)'].values[i]
                                     ])

        #new data Dataframe - only points after 2nd RESET pulse - that way it is always OK and 5
        # Create a mask to identify the rows where the cycle changes
        mask = data['reset_cycle'].shift() != data['reset_cycle']
        # Find the index of the second cycle
        print('mask: ',mask)
        first_true_index = (~mask).idxmax()
        # print('first true index:',first_true_index)


        # Truncate the DataFrame to show data only after the second cycle
        truncated_data = data.iloc[first_true_index:]
        print(truncated_data)

        # Assign STDP cycles for read peaks
        cycle_name = 'read_cycle'
        data = assign_STDP_cycles(truncated_data, variation, read_V, cycle_name)
        peaks = data[data[cycle_name].notna()] #show only peaks for read cycles
        # print('READ peaks: ', peaks)

        if save_reads == True:
            prefix = "read_peaks_"

            #making folder for saving READs
            folder_name = filename.replace("/", " ").split()[0] + "/" + prefix +"/"
            os.makedirs(folder_name, exist_ok=True)

            output_filename = filename.replace("/", " ").split()[0] + "/" + prefix +"/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
            print(f'\n Saving READ peaks as {output_filename}')

            with open(output_filename, 'w', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerow(["Peak Index", "Corrected time", "WE(1).Potential (V)", "WE(1).Current (A)"])
                for i in range(len(peaks)):
                    writer.writerow([peaks.index[i],
                                     peaks['Corrected time (s)'].values[i],
                                     peaks['WE(1).Potential (V)'].values[i],
                                     peaks['WE(1).Current (A)'].values[i]
                                     ])

        # Get dt from the first two stdp pulses
        #this dt is not a REAL dt - one should know for which file the dt is equal to ZERO and the normalize the whole series accoridngly.
        t1 = data.loc[(data['read_cycle'] == 3)]['Corrected time (s)'].max()
        t2 = data.loc[(data['read_cycle'] == 4)]['Corrected time (s)'].max()
        dt = t2 - t1
        # print('dt - 2nd and 3rd last read:', dt)

        # Extract STDP for reads and peaks:
        data_STDP = extract_STDP(data)
        # print(f'data_STDP:\n{data_STDP}')

        if save_data == True:
            saver_data_STDP(data_STDP, filename, dt)

        # Get mean values of STDP
        STDP = STDP.append({
            'dt/s': dt,
            'READ_before': data_STDP['READ_before_MEAN/mA'].mean(),
            'READ_after': data_STDP['READ_after_MEAN/mA'].mean(),
            'WEIGHT_change': data_STDP['WEIGHT_change'].mean(),
            'filename': filename
            },ignore_index=True)

    STDP = STDP.sort_values(by=['dt/s'])
    print(f'\nYour output "STDP":\n{STDP}')

    # TO DO - add plotters
    # # Plotting data
    # plotter_SRDP_CA_assigning_cycles(data, filename, dt) if plot_assigning == True else None
    # plotter_SRDP_I_vs_peak(data, filename, dt) if plot_I_vs_peak == True else None
    # plotter_SRDP_reads_peaks_dt(STDP) if plot_SRDP_dt == True else None





    if save_STDP == True:
        saver_STDP(STDP, list_filenames[-1])

    return data, STDP

del(main)
