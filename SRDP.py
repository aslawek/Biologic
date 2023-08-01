import pandas as pd
import matplotlib.pyplot as plt     # for some reason this line is important...
from functions.data_managment.loaders import load_from_mpt
from functions.data_managment.savers import saver_data_SRDP, saver_SRDP_each_dt, saver_SRDP_summary
from functions.assigners.assign_cycles_SRDP import assign_SRDP_cycles
from functions.extractors.extract_SRDP import extract_SRDP_each_dt
from functions.plotters.plotter_SRDP import plotter_SRDP_CA_assigning_cycles, plotter_SRDP_I_vs_peak, plotter_SRDP_reads_peaks_dt

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data, SRDP_summary
    print('\nSTARTING SRDP.py script...')
    print('\nThis is more automated script for dealing with SRDP data. Please list .mpt files from your experiment...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [
        'data_examples/SRDP_10ms.mpt',
        'data_examples/SRDP_50ms.mpt',
        'data_examples/SRDP_100ms.mpt',
        'data_examples/SRDP_200ms.mpt',
        'data_examples/SRDP_500ms.mpt'
    ]

    save_data = False           # this saves 4-column data with SRDP peaks and reads assigned
    save_SRDP_each_dt = False   # this saves SRDP for each dt
    save_SRDP_summary = False   # this saves SRDP summary with std and more

    plot_assigning = True       # this plots I(t) with reads and peaks assigned
    plot_I_vs_peak = False      # this plots I vs peak
    plot_SRDP_dt = True         # this plots SRDP summary

    # Here you can hardcode your voltages (leave None if script works)
    hardcoded_bias_V = None
    hardcoded_read_V = None
    hardcoded_peak_V = None

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    SRDP_summary = pd.DataFrame()
    for index, filename in enumerate(list_filenames):
        print(f'\n \t ### STARTING LOOP {index + 1} ###\n\nLoading data {index + 1} of {len(list_filenames)} from file {filename}\n')

        # Load the data
        data = load_from_mpt(filename)

        if len(data) == 0:
            print('\033[93m' + f'\nNo data found for {filename}. Skipping...\n' + '\x1b[0m')
            continue

        # get voltages or use hardcoded values:
        bias_V = data['control/V'].unique()[0] if hardcoded_bias_V == None else hardcoded_bias_V
        read_V = data['control/V'].unique()[1] if hardcoded_read_V == None else hardcoded_read_V
        peak_V = data['control/V'].unique()[2] if hardcoded_peak_V == None else hardcoded_peak_V
        print(f'Voltage values are: {bias_V} V for bias, {read_V} V for read and {peak_V} V for peak.')

        # Assign SRDP cycles for reads and peaks
        data = assign_SRDP_cycles(data, read_V, peak_V)

        # Get dt from the first two peak_cycles
        t1_dt = data.loc[(data['peak_cycle'] == 1) & (data['control/V'] == peak_V)]['time/s'].max()
        t2_dt = data.loc[(data['peak_cycle'] == 2) & (data['control/V'] == peak_V)]['time/s'].min()
        dt = t2_dt - t1_dt

        # Get the frequency = 1/(t + dt)
        t1_freq = data.loc[(data['peak_cycle'] == 1) & (data['control/V'] == peak_V)]['time/s'].min()
        t2_freq = data.loc[(data['peak_cycle'] == 2) & (data['control/V'] == peak_V)]['time/s'].min()
        freq = 1/(t2_freq - t1_freq)

        # Extract SRDP for reads and peaks:
        SRDP_each_dt = extract_SRDP_each_dt(data, dt, freq)

        # Get SRDP summary with statistics
        SRDP_summary = SRDP_summary.append({
            'dt/s': dt,
            'f/Hz': freq,
            'I_odd/mA': SRDP_each_dt['I_odd/mA'].mean(),
            'std_I_odd/mA': SRDP_each_dt['I_odd/mA'].std(),
            'I_even/mA': SRDP_each_dt['I_even/mA'].mean(),
            'std_I_even/mA': SRDP_each_dt['I_even/mA'].std(),
            'I_first/mA': SRDP_each_dt['I_first/mA'].mean(),
            'std_I_first/mA': SRDP_each_dt['I_first/mA'].std(),
            'I_last/mA': SRDP_each_dt['I_last/mA'].mean(),
            'std_I_last/mA': SRDP_each_dt['I_last/mA'].std(),
            'odd_to_even': (SRDP_each_dt['I_odd/mA'] / SRDP_each_dt['I_even/mA']).mean(),
            'std_odd_to_even': (SRDP_each_dt['I_odd/mA'] / SRDP_each_dt['I_even/mA']).std(),
            'even_to_odd': (SRDP_each_dt['I_even/mA'] / SRDP_each_dt['I_odd/mA']).mean(),
            'std_even_to_odd': (SRDP_each_dt['I_even/mA'] / SRDP_each_dt['I_odd/mA']).std(),
            'first_to_last': (SRDP_each_dt['I_first/mA'] / SRDP_each_dt['I_last/mA']).mean(),
            'std_first_to_last': (SRDP_each_dt['I_first/mA'] / SRDP_each_dt['I_last/mA']).std(),
            'last_to_first': (SRDP_each_dt['I_last/mA'] / SRDP_each_dt['I_first/mA']).mean(),
            'std_last_to_first': (SRDP_each_dt['I_last/mA'] / SRDP_each_dt['I_first/mA']).std(),
            'filename': filename},
            ignore_index=True)
        SRDP_summary = SRDP_summary.sort_values(by=['dt/s'])

        # Plotting data and assigning cycles
        plotter_SRDP_CA_assigning_cycles(data, filename, dt) if plot_assigning == True else None
        plotter_SRDP_I_vs_peak(data, filename, dt) if plot_I_vs_peak == True else None

        # Saving data
        saver_data_SRDP(data, filename, dt) if save_data == True else None
        saver_SRDP_each_dt(SRDP_each_dt, filename, dt) if save_SRDP_each_dt == True else None


    # Plotting and saving SRDP summary
    plotter_SRDP_reads_peaks_dt(SRDP_summary) if plot_SRDP_dt == True else None
    saver_SRDP_summary(SRDP_summary, list_filenames[-1]) if save_SRDP_summary == True else None

    return data, SRDP_summary

del(main)
