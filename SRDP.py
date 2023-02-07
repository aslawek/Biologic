import pandas as pd
from functions.data_managment.loaders import load_from_mpt
from functions.data_managment.savers import saver_data_SRDP, saver_SRDP
from functions.assigners.assign_cycles_SRDP import assign_SRDP_cycles
from functions.extractors.extract_SRDP import extract_SRDP
from functions.plotters.plotter_SRDP import plotter_SRDP_CA_assigning_cycles, plotter_SRDP_I_vs_peak, plotter_SRDP_reads_peaks_dt

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data, SRDP
    print('\nSTARTING SRDP.py script...')
    print('\nThis is more automated script for dealing with SRDP data. Please list .mpt files from your experiment...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [
        'data/test_SRDP_100ms.mpt',
        'data/test_SRDP_10ms.mpt',
        'data/test_SRDP_200ms.mpt',
        'data/test_SRDP_500ms.mpt',
        'data/test_SRDP_50ms.mpt'
    ]

    save_data = False
    save_SRDP = False

    plot_assigning = True
    plot_I_vs_peak = False
    plot_SRDP_dt = True

    # Here you can hardcode your voltages (leave None if script works)
    hardcoded_bias_V = None
    hardcoded_read_V = None
    hardcoded_peak_V = None

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    SRDP = pd.DataFrame({'dt/s': pd.Series(dtype='float64'), 'odd_to_even': pd.Series(dtype='float64'), 'first_to_last': pd.Series(dtype='float64')})
    for index, filename in enumerate(list_filenames):
        print(f'\n \t ### STARTING LOOP {index + 1} ###\n\nLoading data {index + 1} of {len(list_filenames)} from file {filename}\n')

        # Load the data
        data = load_from_mpt(filename)

        if len(data) == 0:
            print('\033[93m' + f'\nNo data found for {filename}. Skipping...\n' + '\x1b[0m')
            continue

        # get voltages or use hardcoded values:
        bias_V = data['control/V'].unique()[0] if hardcoded_bias_V == None else None
        read_V = data['control/V'].unique()[1] if hardcoded_read_V == None else None
        peak_V = data['control/V'].unique()[2] if hardcoded_peak_V == None else None
        print(f'Voltage values are: {bias_V} V for bias, {read_V} V for read and {peak_V} V for peak.')

        # Assign SRDP cycles for reads and peaks
        data = assign_SRDP_cycles(data, read_V, peak_V)

        # Get dt from the first two peak_cycles
        t1 = data.loc[(data['peak_cycle'] == 1) & (data['control/V'] == peak_V)]['time/s'].max()
        t2 = data.loc[(data['peak_cycle'] == 2) & (data['control/V'] == peak_V)]['time/s'].min()
        dt = t2 - t1

        # Extract SRDP for reads and peaks:
        data_SRDP = extract_SRDP(data)
        print(f'data_SRDP:\n{data_SRDP}')

        # Get mean values of SRDP
        SRDP = SRDP.append({
            'dt/s': dt, 'I_odd': data_SRDP['I_odd/mA'].mean(), 'I_even': data_SRDP['I_even/mA'].mean(),
            'odd_to_even': (data_SRDP['I_odd/mA'] / data_SRDP['I_even/mA']).mean(),
            'even_to_odd': (data_SRDP['I_even/mA'] / data_SRDP['I_odd/mA']).mean(),
            'first_to_last': (data_SRDP['I_first/mA'] / data_SRDP['I_last/mA']).mean(), 'filename': filename},
            ignore_index=True)

        # Plotting data
        plotter_SRDP_CA_assigning_cycles(data, filename, dt) if plot_assigning == True else None
        plotter_SRDP_I_vs_peak(data, filename, dt) if plot_I_vs_peak == True else None

        if save_data == True:
            saver_data_SRDP(data, filename, dt)

    SRDP = SRDP.sort_values(by=['dt/s'])
    print(f'\nYour output "SRDP":\n{SRDP}')
    plotter_SRDP_reads_peaks_dt(SRDP) if plot_SRDP_dt == True else None

    if save_SRDP == True:
        saver_SRDP(SRDP, list_filenames[-1])

    return data, SRDP

del(main)
