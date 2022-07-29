from functions.filters.filters_simple import *

def assign_SRDP_cycles(data, read_V, peak_V):
    # Read cycles:
    data = data.assign(read_cycle=pd.Series())
    data_filtered = filter_by_voltage_value(data, read_V)
    data_filtered = data_filtered.assign(read_cycle=pd.Series())
    data_filtered = filter_by_voltage_value(data, read_V)
    read_V_resolution = data_filtered['time/s'].diff(periods=-1).median()
    data_filtered = data_filtered.assign(read_cycle=pd.Series())
    data_filtered['read_cycle'] = data_filtered['time/s'].shift().diff(periods=-1).lt(1.1 * read_V_resolution).cumsum() + 1
    for cycle in range(data_filtered['read_cycle'].max()):
        cycle_index_min = data_filtered.loc[data_filtered['read_cycle'] == cycle + 1].idxmin()['time/s']
        cycle_index_max = data_filtered.loc[data_filtered['read_cycle'] == cycle + 1].idxmax()['time/s']
        data.loc[cycle_index_min:cycle_index_max, ('read_cycle')] = cycle + 1

    # Peak cycles:
    data = data.assign(peak_cycle=pd.Series())
    data_filtered = filter_by_voltage_value(data, peak_V)
    peak_V_resolution = data_filtered['time/s'].diff(periods=-1).median()
    data_filtered = data_filtered.assign(peak_cycle=pd.Series())
    data_filtered['peak_cycle'] = data_filtered['time/s'].shift().diff(periods=-1).lt(1.1 * peak_V_resolution).cumsum() + 1
    for cycle in range(data_filtered['peak_cycle'].max()):
        cycle_index_min = data_filtered.loc[data_filtered['peak_cycle'] == cycle + 1].idxmin()['time/s']
        cycle_index_max = data_filtered.loc[data_filtered['peak_cycle'] == cycle + 1].idxmax()['time/s']
        data.loc[cycle_index_min:cycle_index_max, ('peak_cycle')] = cycle + 1

    return data