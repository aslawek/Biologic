import numpy as np

from functions.filters.filters_simple import *
import pandas as pd
import warnings

from functions.filters.filters_simple import filter_by_voltage_value_STDP

def assign_STDP_states(data, n, V_bias, V_set, V_reset, V_read, V_err):
    states = []
    for i in range(len(data)):
        # Here are fragments of data n-points before and after
        V_before = data['WE(1).Potential (V)'].iloc[max(i - n, 0):i]
        V_after = data['WE(1).Potential (V)'].iloc[i:min(i + n + 1, len(data))]
        if V_bias - V_err <= data['WE(1).Potential (V)'].iloc[i] <= V_bias + V_err and (
                all(V_bias - V_err <= V <= V_bias + V_err for V in V_before) or all(
                V_bias - V_err <= V <= V_bias + V_err for V in V_after)):
            states.append('bias')
        elif V_set - V_err <= data['WE(1).Potential (V)'].iloc[i] <= V_set + V_err and (
                all(V_set - V_err <= V <= V_set + V_err for V in V_before) or all(
                V_set - V_err <= V <= V_set + V_err for V in V_after)):
            states.append('set')
        elif V_reset - V_err <= data['WE(1).Potential (V)'].iloc[i] <= V_reset + V_err and (
                all(V_reset - V_err <= V <= V_reset + V_err for V in V_before) or all(
                V_reset - V_err <= V <= V_reset + V_err for V in V_after)):
            states.append('reset')
        elif V_read - V_err <= data['WE(1).Potential (V)'].iloc[i] <= V_read + V_err and (
                all(V_read - V_err <= V <= V_read + V_err for V in V_before) or all(
                V_read - V_err <= V <= V_read + V_err for V in V_after)):
            states.append('read')
        else:
            states.append('unknown')
    data['state'] = pd.Series(states, name='state')
    return data

def count_STDP_read_cycles(data):
    # Read cycles:
    data = data.assign(read_cycle=pd.Series())
    data_filtered = data.loc[data['state'] == 'read']
    data_filtered = data_filtered.assign(read_cycle=pd.Series())
    read_V_resolution = data_filtered['Time (s)'].diff(periods=-1).median()
    data_filtered['read_cycle'] = data_filtered['Time (s)'].shift().diff(periods=-1).lt(1.1 * read_V_resolution).cumsum() + 1
    if len(data_filtered) == 0:
        warnings.warn('\nNo read_cycles found. Check if your V_read is within V_err! Have a beautiful day :)')
    else:
        for cycle in range(data_filtered['read_cycle'].max()):
            cycle_index_min = (data_filtered['read_cycle'] == cycle + 1).idxmax()
            cycle_index_max = (data_filtered['read_cycle'] == cycle + 1)[::-1].idxmax()
            data.loc[cycle_index_min:cycle_index_max, 'read_cycle'] = cycle + 1
    return data

def assign_STDP_reset_cycles(data, variation, voltage, cycle_name):

    #ANY name of the cycles:

    data = data.assign(cycle=pd.Series()) #array for storing cycles
    data_filtered = filter_by_voltage_value_STDP(data, voltage, variation)
    voltage_resolution = data_filtered['Corrected time (s)'].diff(periods=-1).median()
    time_threshold = 1.1 #meaning +/- 10%

    print('Working on: ', cycle_name)
    data_filtered = data_filtered.assign(cycle=pd.Series())

    data_filtered[cycle_name] = data_filtered['Corrected time (s)'].shift().diff(periods=-1).lt(time_threshold * voltage_resolution).cumsum() + 1

    for cycle in range(data_filtered[cycle_name].max()):
        cycle_index_min = min(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
                        key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])
        cycle_index_max = max(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
                              key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])
        # cycle_index_min = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmin()['Corrected time (s)']
        # cycle_index_max = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmax()['Corrected time (s)']
        data.loc[cycle_index_min:cycle_index_max, (cycle_name)] = cycle + 1

    # data = data_filtered

    return data

def assign_STDP_cycles(data, variation, voltage, cycle_name):

    #ANY name of the cycles:

    data = data.assign(cycle=pd.Series()) #array for storing cycles
    data_filtered = filter_by_voltage_value_STDP(data, voltage, variation)
    voltage_resolution = data_filtered['Corrected time (s)'].diff(periods=-1).median()

    print('Working on: ', cycle_name)
    data_filtered = data_filtered.assign(cycle=pd.Series())

    #TO DO: maybe we should change this to something easier to interpret ???
    data_filtered[cycle_name] = data_filtered['Corrected time (s)'].shift().diff(periods=-1).lt(1.1 * voltage_resolution).cumsum() + 1

    # Calculate the mean value of each cycle
    cycle_means = data_filtered.groupby(cycle_name)['WE(1).Potential (V)'].transform('mean')
    print('cycle means:', cycle_means, "cycle size:", cycle_means.size)

    # Exclude voltage values exceeding X% of the mean value
    # limiting_factor = 0.02 # +/- 2%
    # upper_limit = (1 + limiting_factor) * cycle_means
    # lower_limit = (1 - limiting_factor) * cycle_means
    # data_filtered = data_filtered[
    #     (data_filtered['WE(1).Potential (V)'] <= upper_limit) & (data_filtered['WE(1).Potential (V)'] >= lower_limit)]


    # Update the cycle numbering
    # data_filtered[cycle_name] = data_filtered.groupby(cycle_name).ngroup() + 1
    # max_cycle = data_filtered[cycle_name].max()

    # all_cycles = range(1, max_cycle + 1)
    # data['cycle'] = pd.Series(all_cycles)
    data_iterator = 0

    # for cycle in range(data_filtered[cycle_name].max()):
    #     cycle_index_min = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmin()['Corrected time (s)']
    #     cycle_index_max = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmax()['Corrected time (s)']
    #     data.loc[cycle_index_min:cycle_index_max, (cycle_name)] = cycle + 1

    for cycle in range(data_filtered[cycle_name].max()):
        cycle_index_min = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmin()['Corrected time (s)']
        cycle_index_max = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmax()['Corrected time (s)']

        cycle_length = cycle_index_max - cycle_index_min + 1  # Calculate cycle length

        if cycle_length >= 5:  # Include cycles with at least 10 points
            cycle_values = data_filtered.loc[cycle_index_min:cycle_index_max, 'WE(1).Potential (V)']
            mean_value = cycle_values.mean()
            threshold = 0.02 * mean_value  # Threshold for excluding points (2% of the mean value)
            # Exclude points that are under/over 5% from the mean value
            cycle_values = cycle_values[abs(cycle_values - mean_value) <= threshold]

            # cycle_values = cycle +1
            data.loc[cycle_values.index, cycle_name] = data_iterator + 1
            data_iterator = data_iterator + 1

            # data_filtered.loc[cycle_values.index, (cycle_name)] = cycle + 1

    data_filtered = data
    data_filtered = data_filtered[data_filtered[cycle_name].notna()]
    print('data_unfiltered:', data)
    print('data_filtered:', data_filtered)
    data_filtered.to_csv("filtered_data.txt", index=False)

    return data

# def get_variable_name(var):
#     for name, value in globals().items():
#         if value is var:
#             return name
#     return None


