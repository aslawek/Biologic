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

    print('Hi! I will extract time reads data for each cycle using median() for \n')

    data_time_reads = pd.DataFrame({'cycle': pd.Series(dtype='int'), 'I_odd/mA': pd.Series(dtype='float64'), 'I_even/mA': pd.Series(dtype='float64')})
    for cycle in range(data_filtered['cycle'].max()):
        print(f'Working on cycle {cycle} out of  {data_filtered["cycle"].max()}...')

        #row = pd.Series({
        #    'cycle': np.ceil((cycle + 1) / 2),
        #    'I_odd/mA' : data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 0)]['I/mA'].median(),
        #    'I_even/mA': data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 1)]['I/mA'].median()})

        #data_time_reads = data_time_reads.append(row, index=cycle)

        data_time_reads = data_time_reads.append(pd.Series({
            'cycle': np.ceil((cycle + 1) / 2),
            'I_odd/mA' : data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 0)]['I/mA'].median(),
            'I_even/mA': data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 1)]['I/mA'].median()}, name=int(np.ceil((cycle + 1) / 2))))

        #data_time_reads = data_time_reads.append({
        #    'cycle': np.ceil((cycle + 1) / 2),
        #    'I_odd/mA' : data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 0)]['I/mA'].median(),
        #    'I_even/mA': data_filtered.loc[(data_filtered['cycle'] == cycle + 1) & (cycle % 2 == 1)]['I/mA'].median()}, ignore_index=True)

    print(f'\n{data_time_reads}')
    #return data_time_reads

del(main)