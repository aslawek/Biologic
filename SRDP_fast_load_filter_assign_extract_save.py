import pandas as pd
import numpy as np

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    global data

    # Please give me list of files with SRDP that you want to work with:
    list_files = [
        'data/test_CA_Tomek.mpt',
        'data/test_CA_Tomek_2.mpt',
        'data/test_CA_Tomek_3.mpt'
    ]

    # Please give me the read voltage (V) and its error (+/-)
    read_V = 0.2
    err_V = 0.01

    for filename in list_files:
        #filename = input('Yo! Give me the file path here quickly: ')

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

        print(f'Loaded data from file {filename}, here\'s what it look like:\n{data}')

        data_filtered = data.loc[
            (data['control/V'] > read_V - err_V) & (data['control/V'] < read_V + err_V)].reset_index()

        print(f'\nI just filtered your data according to control/V, from {read_V - err_V} to {read_V + err_V} :)')

        # Take median() for time/s change
        time_change_median = data_filtered['time/s'].diff(periods=-1).median()
        print(
            f'\nI calculated the change in time/s for every two consecutive points and took median: {time_change_median}')

        # Make copy of global variable and assign state (if the next time/s is larger than 1.1 * median from time change
        data_filtered['cycle'] = data_filtered['time/s'].diff(periods=-1).lt(1.1 * time_change_median).cumsum() + 1

        print(f'Your modified filtered data: \n{data_filtered}')

        print(
            '\nHi! For data_filtered global variable I will calculate median() for I/mA for each cycle and split the values for odd (1,3,5..) and even (2,4,6...) integers.\n')

        data_time_reads = pd.DataFrame({'cycle': pd.Series(dtype='int32'), 'I_odd/mA': pd.Series(dtype='float64'),
                                        'I_even/mA': pd.Series(dtype='float64')})

        for cycle in range(int(data_filtered['cycle'].max() / 2)):
            print(
                f'Working on cycle {cycle + 1} out of {int(data_filtered["cycle"].max() / 2 + 1)}:\n\tI_odd/mA  is taken from data_filtered cycle: {cycle * 2 + 1}\n\tI_even/mA is taken from data_filtered cycle: {cycle * 2 + 2}')

            data_time_reads = data_time_reads.append({
                'cycle': cycle + 1,
                'I_odd/mA': data_filtered.loc[data_filtered['cycle'] == (cycle * 2 + 1)]['I/mA'].median(),
                'I_even/mA': data_filtered.loc[data_filtered['cycle'] == (cycle * 2 + 2)]['I/mA'].median()},
                ignore_index=True)

        data_time_reads['cycle'] = data_time_reads['cycle'].astype('int32')

        print(f'\nYour output "data_time_reads":\n{data_time_reads}')

        data_time_reads.to_csv(f'{filename}_SRDP', sep='\t', index=False)
        print(f'\nYour dataframe called "data_time_reads" was saved as {filename}_SRDP')

    return

del(main)