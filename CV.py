import numpy as np
import pandas as pd
from plotters.plot_CVs import plot_CVs

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data
    print('\nThis is more automated function for dealing with CVs. Please list your CVs (list_inputs) or type a path...')

    assign_cycles = False
    plot_data = True
    save_data = False

    list_filenames = [
        'data/test_CV_just_one.mpt'
    ]

    if len(list_filenames) == 0:
        list_filenames.append(input('\nNo element found in list_data, please give me a path to Your data: '))

    for index, filename in enumerate(list_filenames):
        ### LOADING DATA ###

        # If you load "raw" Biologic .mpt then it will automatically find how many rows have to be skipped
        if open(filename).readline().rstrip('\n') == 'EC-Lab ASCII FILE':
            rows_to_skip = int(open(filename).readlines()[1].split()[-1]) - 1
            print(f'Got raw EC-Lab ASCII FILE, skipping {rows_to_skip} rows...')
        else:
            rows_to_skip = 0
            print(f'Got something else than EC-Lab ASCII FILE, no rows skipped.')

        # Check label for current column (for CV is different than for CA)
        labels = open(filename).readlines()[rows_to_skip]
        if labels.__contains__('I/mA'):
            label_I = 'I/mA'
        elif labels.__contains__('<I>/mA'):
            label_I = '<I>/mA'
            print(f'Changed column header for current from {label_I} to I/mA')

        data = pd.read_csv(f'{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[
            ['time/s', 'control/V', 'Ewe/V', label_I]] \
            .rename(columns={'<I>/mA': 'I/mA'})

        # Change '.' for "," for all columns (if needed):
        for column in data:
            if data[column].dtype == object:
                data[column] = data[column].str.replace(',', '.').astype(float)

        print(f'Loaded data {index + 1} of {len(list_filenames)} from file {filename}')

        # Assigning states for CV data
        if assign_cycles == True:
            print('Hi! I will assign cycles to your CV data.')
            # Drop (remove) last row no to have empty (1-point) last CV cycle
            data.drop(data.tail(1).index, inplace=True)
            data['cycle'] = np.ceil(np.sign(data['control/V']).diff().ne(0).astype('int').cumsum() / 2).astype('int')

        print(f'Here\'s what it look like:\n{data}')

        # Plotting data
        if plot_data == True:
            plot_CVs(data, filename)

    return data

del(main)