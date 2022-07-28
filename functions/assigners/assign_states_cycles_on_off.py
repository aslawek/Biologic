import numpy as np

def assign_on_off_by_sequence(data, sequence):
    print('Hi! I will assign states and group them into cycles according to the sequence:')
    for i in range(len(sequence)):
        print(f'{i+1}\t{sequence[i]}')

    data['cycle'] = np.floor(
        (data['control/V'].ne(data['control/V'].shift()).cumsum() - 1) / len(sequence) + 1).astype('int')
    data['state'] = np.mod(data['control/V'].ne(data['control/V'].shift()).cumsum() - 1, len(sequence)).astype(
        'int')
    for i in range(len(sequence)):
        data['state'].replace({i: sequence[i]}, inplace=True)
    return data