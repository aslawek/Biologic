from functions.filters.filters_simple import *
import pandas as pd

from functions.filters.filters_simple import filter_by_voltage_value_STDP


# assigning RESET cycles
def assign_STDP_reset_cycles(data, variation, voltage, cycle_name):

    #ANY name of the cycles:

    data = data.assign(cycle=pd.Series()) #array for storing cycles
    data_filtered = filter_by_voltage_value_STDP(data, voltage, variation)
    voltage_resolution = data_filtered['Corrected time (s)'].diff(periods=-1).median()
    time_threshold = 1.1 #meaning +/- 10%

    print('Working on: ', cycle_name)
    data_filtered = data_filtered.assign(cycle=pd.Series())

    data_filtered[cycle_name] = data_filtered['Corrected time (s)'].shift().diff(periods=-1).lt(time_threshold * voltage_resolution).cumsum() + 1

    reset_cycles = []

    for cycle in range(data_filtered[cycle_name].max()):
        cycle_index_min = min(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
                              key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])
        cycle_index_max = max(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
                              key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])

        cycle_length = cycle_index_max - cycle_index_min + 1

        if cycle_length >= 80:
            reset_cycles.append((cycle_index_min, cycle_index_max))

        # Assign the reset cycles with 50+ points
    for new_cycle_num, (min_index, max_index) in enumerate(reset_cycles):
        data.loc[min_index:max_index, cycle_name] = new_cycle_num + 1

    return data

    # for cycle in range(data_filtered[cycle_name].max()):
    #     cycle_index_min = min(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
    #                     key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])
    #     cycle_index_max = max(data_filtered[data_filtered[cycle_name] == cycle + 1].index,
    #                           key=lambda x: data_filtered.loc[x, 'Corrected time (s)'])
    #     # cycle_index_min = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmin()['Corrected time (s)']
    #     # cycle_index_max = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmax()['Corrected time (s)']
    #
    #     cycle_length = cycle_index_max - cycle_index_min + 1  # Calculate cycle length
    #
    #
    #     data.loc[cycle_index_min:cycle_index_max, (cycle_name)] = cycle + 1





    return data


# assigning READ cycles(3x read)
def assign_STDP_read_cycles(data, variation, voltage, cycle_name):

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

        if cycle_length >= 20:  # Include cycles with at least XYZ points
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
    # print('data_unfiltered:', data)
    print('data_filtered:', data_filtered)
    # data_filtered.to_csv("filtered_data.txt", index=False)

    return data

# def get_variable_name(var):
#     for name, value in globals().items():
#         if value is var:
#             return name
#     return None


