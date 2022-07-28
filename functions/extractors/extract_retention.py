import pandas as pd

def extractor_retention(data):

    print('Hi! I will extract retention data for each read using median() for read and time\n')

    data_retention = pd.DataFrame({'cycle': pd.Series(dtype='int'), 'time/s': pd.Series(dtype='float64'), 'I_read/mA': pd.Series(dtype='float64')})
    for cycle in range(data['cycle'].max()):
        print(f'Working on cycle {cycle} out of {data["cycle"].max()}...')
        data_retention = data_retention.append({'cycle': cycle + 1,
                                          'time/s'   : data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read')]['time/s'].median(),
                                          'I_read/mA': data.loc[(data['cycle'] == cycle + 1) & (data['state'] == 'read')]['I/mA'].median()}, ignore_index=True)
    return data_retention