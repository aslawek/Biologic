from functions.data_managment.loaders import *
from functions.data_managment.savers import *
from functions.filters.simple_filters import *
from functions.assigners.assign_states_cycles_on_off import assign_on_off_by_sequence
from functions.plotters.plot_CVs import *

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    print('\n \tSTARTING CV.py script...')
    print('\nThis is more automated script for dealing with CVs. Please list your CVs (list_filenames) or type a path...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [
        'data/test_CA.mpt'
    ]

    # Put your on-off sequence here:
    sequence = ['bias', 'set', 'bias', 'read_set', 'bias', 'reset', 'bias', 'read_reset']
    #sequence = ['bias', 'set', 'read_set', 'bias', 'reset', 'read_reset']

    filter_by_cycles_ranges = []        # <- here put pairs of ranges for filtering cycles (leave [] if not neccesary)
    save_data = False

    # For plotting:
    plot_CA_simple = True

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
        data = assign_on_off_by_sequence(data)

        print(data)

        # Filtering over cycles
        if filter_by_cycles_ranges != []:
            data = filter_by_cycles(data, filter_by_cycles_ranges)

        print(f'Here\'s what it look like:\n{data}')

        if save_data == True:
            save_data(data, filename)

        # Plotting data
        #plotter_CV_simple(data, filename) if plot_CV_simple == True else None

    return data

del(main)