import pandas as pd

def extract_on_offs(data):

    print('Hi! I will extract on-off data for each cycle using median() for read_set and read_reset\n')

    data_on_off = pd.DataFrame({'cycle': pd.Series(dtype='int'), 'I_set/mA': pd.Series(dtype='float64'), 'I_reset/mA': pd.Series(dtype='float64')})
    for cycle in range(data['cycle'].max()):
        print(f'Working on cycle {cycle} out of  {data["cycle"].max()}...')
        data_on_off = data_on_off.append({'cycle': cycle + 1,
                                          'I_set/mA'  : data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read_set'  )]['I/mA'].median(),
                                          'I_reset/mA': data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read_reset')]['I/mA'].median()}, ignore_index=True)
    return data_on_off
