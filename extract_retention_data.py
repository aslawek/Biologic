import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    data
except:
    exit("There is no data loaded. Use load_data.py script.")
else:
    print(f'Data loaded!')

# sth similar to IIFE
main = lambda f: f(data)
@main
def main(data):
    global data_retention

    print('Hi! I will extract retention data for each read using median() for read and time\n')

    data_retention = pd.DataFrame({'cycle': pd.Series(dtype='int'), 'time/s': pd.Series(dtype='float64'), 'I_read/mA': pd.Series(dtype='float64')})
    for cycle in range(data['cycle'].max()):
        print(f'Working on cycle {cycle} out of {data["cycle"].max()}...')
        data_retention = data_retention.append({'cycle': cycle + 1,
                                          'time/s'   : data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read')]['time/s'].median(),
                                          'I_read/mA': data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read')]['I/mA'].median()}, ignore_index=True)

    print(f'\n{data_retention}')
    return data_retention

del(main)