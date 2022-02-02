import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Name of the file (testing reasons)
# filename = 'ITO_Ni[Me2Ph2Benz]_1kRPM_Cu_test_ON-OFF_02_CA_C01.mpt'
filename = 'data_test/test.mpt'
E_set = 1.6
E_reset = -1.6
E_bias = 0
E_read = -0.5
E_err = 0.01

# Find numbers of rows to skip (header): open file, read 2nd line, split str to array, read last element, convert to int
rows_to_skip = int(open(f'data_test/{filename}').readlines()[1].split()[-1]) - 1

# Read the data, select the necessary columns
data = pd.read_csv(f'data_test/{filename}', encoding="ISO-8859-1", skiprows=rows_to_skip, sep='\t')[['time/s', 'control/V', 'Ewe/V', 'I/mA']]

# Function to assign bias / read / set / reset state according to E and E_err
def assign_on_off_state(data, E_bias, E_set, E_reset, E_read, E_err):
    data.loc[(data['control/V'] < E_bias  + E_err) & (data['control/V'] > E_bias  - E_err), 'state'] = 'bias'
    data.loc[(data['control/V'] < E_read  + E_err) & (data['control/V'] > E_read  - E_err), 'state'] = 'read'
    data.loc[(data['control/V'] < E_set   + E_err) & (data['control/V'] > E_set   - E_err), 'state'] = 'set'
    data.loc[(data['control/V'] < E_reset + E_err) & (data['control/V'] > E_reset - E_err), 'state'] = 'reset'
    data = data.fillna('noise')
    return(data)

def show_sequence(data):
    experiment_sequence = 'Your experiment sequence was:'
    prev_state = False
    for index, row in data.iterrows():
        if prev_state != row['state'] : experiment_sequence += f' {row["state"]}'; prev_state = row['state']
    print(experiment_sequence)

# Function to cut the rows only for E_read (+/- E_err)
def filter_by_control_V(data, E_read, E_err):
    return data.loc[(data['control/V'] < E_read + E_err) & (data['control/V'] > E_read - E_err)]

# Function to add cycle column to data, according to the length of sequence (bias states included)
def assign_cycles_to_sequence(data, sequence):
    data['cycle'] = np.floor((data['state'].ne(data['state'].shift()).cumsum() - 1) / len(sequence) + 1).astype('int')
    return data

# Function for extracting on-off data: median for each 'read_cycle'
def extract_on_off_data(data, sequence):
    for cycle in data['cycle']:
        data.loc[data['cycle'] == cycle, 'state'] = np.floor((data.loc[data['cycle'] == cycle, 'state'].ne(data.loc[data['cycle'] == cycle, 'state'].shift()).cumsum())).astype('int')

    data.loc[data['state'] == 1, 'state'] = sequence[1]
    # CHANGE numbers for place in sequence?
    #for i in range(len(sequence)):
    #    print(i)
    #    data.loc[data['state'] == i, 'state'] = data['state'].astype(int) + sequence[i].astype(int)

    print(data)
    #new_data = pd.DataFrame({'read_cycle': pd.Series(dtype='int'), 'I/mA': pd.Series(dtype='float64')})
    #for cycle in range(data['read_cycle'].max()):
    #    print(f'cycle: {cycle}')
    #    print(f'mean: {data.loc[data["read_cycle"] == cycle]["I/mA"].mean()}')
    #    print(f'median: {data.loc[data["read_cycle"] == cycle]["I/mA"].median()}')
    #    new_data = new_data.append({'read_cycle': cycle, 'I/mA': data.loc[data["read_cycle"] == cycle]["I/mA"].median()}, ignore_index=True)
    return data

#data = add_on_off_cycle_columns(data, E_bias, E_set, E_reset, E_read, E_err)
#data = filter_by_control_V(data, E_read, E_err)
data = assign_on_off_state(data, E_bias, E_set, E_reset, E_read, E_err)
data = assign_cycles_to_sequence(data, sequence=['reset', 'bias', 'read', 'bias', 'set', 'bias', 'read', 'bias'])
data = extract_on_off_data(data, sequence=['reset', 'bias', 'read', 'bias', 'set', 'bias', 'read', 'bias'])
#show_sequence(data)

#print(data)
#print(data.info())

#plt.scatter(data['cycle'], data['control/V'])
#plt.plot(data['time/s'], data['control/V'])
#plt.plot(data['cycle'], data['control/V'])
#plt.show()

data.to_csv('data_test/data_tmp.csv', sep='\t', index=False)