import numpy as np
import pandas as pd


def extract_STDP(data, number_of_sequences):
    # For read_cycles
    data_STDP = pd.DataFrame({
        'cycle': pd.Series(dtype='int32'),
        'READ_before_1/mA': pd.Series(dtype='float64'),
        'READ_before_2/mA': pd.Series(dtype='float64'),
        'READ_before_3/mA': pd.Series(dtype='float64'),
        'READ_after_1/mA': pd.Series(dtype='float64'),
        'READ_after_2/mA': pd.Series(dtype='float64'),
        'READ_after_3/mA': pd.Series(dtype='float64'),

    })

    # data_STDP = pd.DataFrame()

    for cycle in range(int(data['read_cycle'].max() / 6)):

        #print(f'Working on cycle {cycle + 1} out of {int(data["read_cycle"].max() / 2)}:\n\tI_odd/mA  is taken from read_cycle: {cycle * 2 + 1}\n\tI_even/mA is taken from read_cycle: {cycle * 2 + 2}\n\tI_first/mA is taken from peak_cycle: {int(cycle * number_of_peaks + 1)}\n\tI_last/mA is taken from peak_cycle: {int(cycle * number_of_peaks + 30)}')
        #read 3x READ_before


        if cycle < number_of_sequences: #if changed in the future, one shouldmodify the whole function to take number_of_sequences variable from the main function
            data_STDP = data_STDP.append({
                'cycle': cycle+1,

                'READ_before_1/mA': data.loc[data['read_cycle'] == (cycle * 6 + 1)]['WE(1).Current (A)'].median(),
                'READ_before_2/mA': data.loc[data['read_cycle'] == (cycle * 6 + 2)]['WE(1).Current (A)'].median(),
                'READ_before_3/mA': data.loc[data['read_cycle'] == (cycle * 6 + 3)]['WE(1).Current (A)'].median(),
                'READ_after_1/mA': data.loc[data['read_cycle'] == (cycle * 6 + 4)]['WE(1).Current (A)'].median(),
                'READ_after_2/mA': data.loc[data['read_cycle'] == (cycle * 6 + 5)]['WE(1).Current (A)'].median(),
                'READ_after_3/mA': data.loc[data['read_cycle'] == (cycle * 6 + 6)]['WE(1).Current (A)'].median(),


            }, ignore_index=True)

            data_STDP['cycle'] = data_STDP['cycle'].astype('int32')

            row = [cycle]

            columns_before = [1, 2, 3] #columns of READ_before_1 , 2 and 3
            selected_before = data_STDP.iloc[row, columns_before]
            # print('data', data_STDP.iloc[row, columns_before])
            read_before_mean = selected_before.values.mean()
            # print('mean seleceted before',  read_before_mean)
            # append to data_STDP
            data_STDP.at[row, 'READ_before_MEAN/mA'] = read_before_mean

            columns_after = [4, 5, 6] #columns of READ_after_1 , 2 and 3
            selected_after = data_STDP.iloc[row, columns_after]
            read_after_mean = selected_after.values.mean()
            # append to data_STDP
            data_STDP.at[row, 'READ_after_MEAN/mA'] = read_after_mean

            weight_change = ((read_after_mean/read_before_mean) - 1) * 100
            print('weight change',  read_before_mean, read_after_mean,  weight_change)
            data_STDP.at[row, 'WEIGHT_change'] = weight_change



    return data_STDP