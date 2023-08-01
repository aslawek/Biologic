import matplotlib.pyplot as plt     # for some reason this line is important...
from functions.data_managment.loaders import load_from_mpt
from functions.data_managment.savers import saver_data, saver_on_offs
from functions.assigners.assign_states_by_sequence import assign_by_sequence
from functions.extractors.extract_on_offs import extract_on_offs
from functions.plotters.plotter_CA import plotter_CA_simple
from functions.plotters.plotter_on_off import plotter_on_offs

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    print('\n \tSTARTING ON_OFF.py script...')
    print('\nThis is more automated script for dealing with ON-OFFs. Please list your CAs (list_filenames) or type a path...')

    # Here you put list of files with CV data. If it is empty it will ask for path.
    list_filenames = [
        'data_examples/CA_on-off.mpt'
    ]

    # Put your on-off sequence here:
    sequence = ['bias', 'set', 'bias', 'read_set', 'bias', 'reset', 'bias', 'read_reset']

    save_data = False           # <- for saving data (as out_{filename})
    save_on_offs = False        # <- for saving on-offs (as ON-OFF_{filename})

    # For plotting:
    plot_CA_simple = True
    plot_on_offs = True

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

        # Extract states for ON-OFFs
        on_offs = extract_on_offs(data)

        print(f'Here\'s what it look like:\n{data}')

        if save_data == True:
            saver_data(data, filename)

        if save_on_offs == True:
            saver_on_offs(on_offs, filename)

        # Plotting data
        plotter_CA_simple(data, filename) if plot_CA_simple == True else None
        plotter_on_offs(on_offs, filename) if plot_on_offs == True else None

    return data

del(main)