import pandas as pd
import numpy as np

def filter_by_cycles(data, ranges):
    data_filtered = pd.DataFrame()
    for i in range(int(np.floor(len(ranges)/2))):
        print(f'Filtering for pairs: {2*i} - {2*i+1} ==== {ranges[2*i]} - {ranges[2*i + 1]}')
        data_filtered = pd.concat([data_filtered, data.loc[(data['cycle'] >= ranges[2*i]) & (data['cycle'] <= ranges[2*i + 1])].reset_index()])
    print(f'len: {len(data_filtered)}')
    if len(data_filtered) == 0:
        raise TypeError("filter_by_cycles: I filtered to empty dataset, check ranges.")
    else:
        return data_filtered

def filter_by_voltage_value(data, filter_V):
    data_filtered = data.loc[data['control/V'] == filter_V]
    if len(data_filtered) == 0:
        raise TypeError("filter_by_cycles: I filtered to empty dataset, check ranges.")
    else:
        return data_filtered

def filter_by_voltage_range(data, filter_V, err_V=0.001):
    data_filtered = data.loc[(data['control/V'] <= filter_V + err_V) & (data['control/V'] >= filter_V - err_V)]
    if len(data_filtered) == 0:
        raise TypeError("filter_by_cycles: I filtered to empty dataset, check ranges.")
    else:
        return data_filtered