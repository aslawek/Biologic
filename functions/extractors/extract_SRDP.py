import pandas as pd

def extract_SRDP_each_dt(data, dt, freq):
    # For read_cycles
    data_SRDP = pd.DataFrame({'cycle': pd.Series(dtype='int32'), 'dt/s': pd.Series(dtype='float64'), 'f/Hz': pd.Series(dtype='float64'), 'I_odd/mA': pd.Series(dtype='float64'), 'I_even/mA': pd.Series(dtype='float64'), 'I_first/mA': pd.Series(dtype='float64'), 'I_last/mA': pd.Series(dtype='float64')})
    number_of_peaks = data['peak_cycle'].max() / data['read_cycle'].max() * 2
    for cycle in range(int(data['read_cycle'].max() / 2)):
        data_SRDP = data_SRDP.append({
            'cycle': cycle + 1,
            'dt/s': dt,
            'f/Hz': freq,
            'I_odd/mA': data.loc[data['read_cycle'] == (cycle * 2 + 1)]['I/mA'].median(),
            'I_even/mA': data.loc[data['read_cycle'] == (cycle * 2 + 2)]['I/mA'].median(),
            'I_first/mA': data.loc[data['peak_cycle'] == (cycle * number_of_peaks + 1)]['I/mA'].mean(),
            'I_last/mA': data.loc[data['peak_cycle'] == (number_of_peaks * (cycle + 1))]['I/mA'].mean()}, ignore_index=True)
    data_SRDP['cycle'] = data_SRDP['cycle'].astype('int32')

    return data_SRDP