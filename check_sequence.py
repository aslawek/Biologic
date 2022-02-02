import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    data
except:
    exit("There is no data loaded. Use load_data.py script.")
else:
    print(f'Data loaded!')

x_arr = []

# sth similar to IIFE
main = lambda f: f(data)
@main
def main(data):
    return True

# Name of the file (testing reasons)
E_set = 1.6
E_reset = -1.6
E_bias = 0
E_read = -0.5
E_err = 0.01

# Find numbers of rows to skip (header): open file, read 2nd line, split str to array, read last element, convert to int
rows_to_skip = int(open(f'data_test/{filename}').readlines()[1].split()[-1]) - 1

# Read the data, select the necessary columns
data = pd.read_csv(f'data_test/{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[['time/s', 'control/V', 'Ewe/V', 'I/mA']]

# Filter for time less than 1176.5 s
data = data.loc[data['time/s'] < 1176.5]

# Assign state to data and enumerate cycles accoring to change in control/V and a given sequence
def find_seq_in_data(data, sequence):
    data['cycle'] = np.floor((data['control/V'].ne(data['control/V'].shift()).cumsum() - 1) / len(sequence) + 1).astype('int')
    data['state'] = np.mod(data['control/V'].ne(data['control/V'].shift()).cumsum() - 1, len(sequence)).astype('int')
    for i in range(len(sequence)):
        data['state'].replace({i: sequence[i]}, inplace=True)
    return data

def extract_on_ff(data):
    new_data = pd.DataFrame({'cycle': pd.Series(dtype='int'), 'I_set/mA': pd.Series(dtype='float64'), 'I_reset/mA': pd.Series(dtype='float64')})
    for cycle in range(data['cycle'].max()):
        new_data = new_data.append({'cycle': cycle + 1,
                                    'I_set/mA': data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read_set')]['I/mA'].median(),
                                    'I_reset/mA': data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read_reset')]['I/mA'].median()}, ignore_index=True)
    return new_data

#data = find_seq_in_data(data, sequence=['bias', 'reset', 'bias', 'read_reset', 'bias', 'set', 'bias', 'read_set'])
data = find_seq_in_data(data, sequence=['bias', 'set', 'bias', 'read_set', 'bias', 'reset', 'bias', 'read_reset'])
data.to_csv(f'data_test/seq_{filename}', sep='\t', index=False)

on_off_data = extract_on_ff(data)
on_off_data.to_csv(f'data_test/on-off_{filename}', sep='\t', index=False)

#print(on_off_data)

#plt.scatter(data['cycle'], data['control/V'])
#plt.plot(data['time/s'], data['control/V'])
#plt.plot(data['cycle'], data['control/V'])
#plt.show()