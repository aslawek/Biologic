import matplotlib.pyplot as plt     # for some reason this line is important...
from functions.data_managment.loaders import *
from functions.data_managment.savers import saver_data, saver_retention
from functions.assigners.assign_states_by_sequence import assign_by_sequence
from functions.extractors.extract_retention import extractor_retention
from functions.plotters.plotter_CA import plotter_CA_simple
from functions.plotters.plotter_retention import plotter_retention

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    print('\n \tSTARTING ON_OFF.py script...')
    print('\nThis is more automated script for dealing with ON-OFFs. Please list your CAs (list_filenames) or type a path...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [

        './el04_on-off_retention_06_CA_C01.txt',
    ]

    # Put your on-off sequence here:
    sequence = ['bias', 'read']
    #sequence = ['bias', 'set', 'bias', 'read']

    extract_retention = True    # <- for extracting retention
    save_data = False           # <- for saving data (as out_{filename})
    save_retention = True      # <- for saving on-offs (as ON-OFF_{filename})

    # For plotting:
    plot_CA_simple = True
    plot_retention = True

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    for index, filename in enumerate(list_filenames):
        print(f'Loading data {index + 1} of {len(list_filenames)} from file {filename}')

        # Load the data
        data = load_from_mpt(filename)

        if len(data) == 0:
            print('\033[93m' + f'\nNo data found for {filename}. Skipping...\n' + '\x1b[0m')
            continue

        # Assigning states for ON-OFFs data
        data = assign_by_sequence(data, sequence)
        print(f'Here\'s what it look like:\n{data}')

        # Extract states for ON-OFFs
        if extract_retention == True:
            data_retention = extractor_retention(data)
            print(f'\n{data_retention}')

        if save_data == True:
            saver_data(data, filename)

        if save_retention == True:
            saver_retention(data_retention, filename)

        # Plotting data
        plotter_CA_simple(data, filename) if plot_CA_simple == True else None
        plotter_retention(data_retention, filename) if plot_retention == True else None

    return data

del(main)