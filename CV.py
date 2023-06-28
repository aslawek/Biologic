from functions.data_managment.loaders import load_from_mpt
from functions.data_managment.savers import saver_CV
from functions.filters.filters_simple import filter_cycles_by_ranges
from functions.assigners.assign_cycles_CV import assign_cycles_CV
from functions.plotters.plotter_CV import *

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    print('\n \tSTARTING CV.py script...')
    print('\nThis is more automated script for dealing with CVs. Please list your CVs (list_filenames) or type a path...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [
        'data_n/ITO_Ni[Et4Benzo]_Au_el5_CV_stability_02_CV_C02.mpt',
        'data_n/ITO_Ni[Et4Benzo]_Au_el6_on-off_500cycles_01_CV_C02.mpt',
        'data_n/ITO_Ni[Et4Benzo]_Au_el6_on-off_500cycles_03_CV_C02.mpt',
        'data_n/ITO_Ni[Et4Benzo]_Au_el7_retention_long_01_CV_C02.mpt',
        'data_n/ITO_Ni[Et4Benzo]_Au_el7_retention_long_07_CV_C02.mpt',
        'data_n/ITO_Ni[Me2Ph2Benzo]_Au_el3_CV_stability_02_CV_C01.mpt',
        'data_n/ITO_Ni[Me2Ph2Benzo]_Au_el4_on-off_500cycles_01_CV_C01.mpt',
        'data_n/ITO_Ni[Me2Ph2Benzo]_Au_el4_on-off_500cycles_03_CV_C01.mpt',
        'data_n/ITO_Ni[Me2Ph2Benzo]_Au_el6_retention_both_states_01_CV_C01.mpt',
        'data_n/ITO_Ni[Me2Ph2Benzo]_Au_el6_retention_both_states_07_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el11_test_CV_channel_1_02_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el11_test_CV_channel_2_02_CV_C02.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_CV_stability_02_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_on-off_500cycles_01_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_on-off_500cycles_03_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_retention_long_01_CV_C01.mpt',
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_retention_long_07_CV_C01.mpt'
    ]

    list_filenames = [
        'data_n/ITO_Ni[Me4Benzo]_Au_el2_retention_long_07_CV_C01.mpt'
    ]

    assign_cycles = True                # <- number cycles of CV
    filter_by_cycles_ranges = []        # <- here put pairs of ranges for filtering cycles (leave [] if not necessary)
    save_data = True                   # <- for saving data (as out_{filename})

    # For plotting:
    plot_CV_simple = False
    plot_CV_simple_with_log_scale = False
    plot_CV_cycles = True
    plot_CV_cycles_with_log_scale = False
    plot_CV_direction = False
    plot_CV_direction_cycles = False

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    for index, filename in enumerate(list_filenames):
        print(f'Loading data {index + 1} of {len(list_filenames)} from file {filename}')

        # Load the data
        data = load_from_mpt(filename)

        if len(data) == 0:
            print('\033[93m' + f'\nNo data found for {filename}. Skipping...\n' + '\x1b[0m')
            continue

        # Assigning states for CV data
        if assign_cycles == True:
            data = assign_cycles_CV(data)

        # Filtering over cycles
        if filter_by_cycles_ranges != []:
            data = filter_cycles_by_ranges(data, filter_by_cycles_ranges)

        print(f'Here\'s what it look like:\n{data}')

        if save_data == True:
            saver_CV(data, filename)

        # Plotting data
        plotter_CV_simple(data, filename) if plot_CV_simple == True else None
        plotter_CV_simple_with_log(data, filename) if plot_CV_simple_with_log_scale == True else None
        plotter_CV_cycles(data, filename) if plot_CV_cycles == True else None
        plotter_CV_cycles_with_log(data, filename) if plot_CV_cycles_with_log_scale == True else None
        plotter_CV_direction(data, filename) if plot_CV_direction == True else None
        plotter_CV_direction_cycles(data, filename) if plot_CV_direction_cycles == True else None

    return data

del(main)