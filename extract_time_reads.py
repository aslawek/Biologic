import pandas as pd
import numpy as np

try:
    data_filtered
except:
    exit("There is no data loaded. Use load_data.py script.")
else:
    print(f'Data loaded!')

# sth similar to IIFE
main = lambda f: f(data_filtered)
@main
def main(data_filtered):
    global data_time_reads

    print('Hi! For data_filtered global variable I will calculate median() for I/mA for each cycle and split the values for odd (1,3,5..) and even (2,4,6...) integers.\n')

    data_time_reads = pd.DataFrame({'cycle': pd.Series(dtype='int32'), 'I_odd/mA': pd.Series(dtype='float64'), 'I_even/mA': pd.Series(dtype='float64')})

    for cycle in range(int(data_filtered['cycle'].max() / 2)):
        print(f'Working on cycle {cycle} out of {int(data_filtered["cycle"].max() / 2)}:\n\tI_odd/mA  is taken from data_filtered cycle: {cycle * 2 + 1}\n\tI_even/mA is taken from data_filtered cycle: {cycle * 2 + 2}')

        data_time_reads = data_time_reads.append({
            'cycle': cycle + 1,
            'I_odd/mA': data_filtered.loc[data_filtered['cycle'] == (cycle * 2 + 1)]['I/mA'].median(),
            'I_even/mA': data_filtered.loc[data_filtered['cycle'] == (cycle * 2 + 2)]['I/mA'].median()}, ignore_index=True)

    data_time_reads['cycle'] = data_time_reads['cycle'].astype('int32')

    print(f'\nYour output "data_time_reads":\n{data_time_reads}')
    return data_time_reads

del(main)