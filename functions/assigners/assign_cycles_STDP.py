from functions.filters.filters_simple import *


def assign_STDP_cycles(data, variation, voltage, cycle_name):

    #ANY name of the cycles:

    data = data.assign(cycle=pd.Series()) #array for storing cycles
    data_filtered = filter_by_voltage_value_STDP(data, voltage, variation)
    voltage_resolution = data_filtered['Corrected time (s)'].diff(periods=-1).median()

    print('Working on: ', cycle_name)
    data_filtered = data_filtered.assign(cycle=pd.Series())
    data_filtered[cycle_name] = data_filtered['Corrected time (s)'].shift().diff(periods=-1).lt(1.1 * voltage_resolution).cumsum() + 1

    for cycle in range(data_filtered[cycle_name].max()):
        cycle_index_min = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmin()['Corrected time (s)']
        cycle_index_max = data_filtered.loc[data_filtered[cycle_name] == cycle + 1].idxmax()['Corrected time (s)']
        data.loc[cycle_index_min:cycle_index_max, (cycle_name)] = cycle + 1
    return data

# def get_variable_name(var):
#     for name, value in globals().items():
#         if value is var:
#             return name
#     return None


