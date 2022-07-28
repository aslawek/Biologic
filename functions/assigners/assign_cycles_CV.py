import numpy as np

def assign_cycles_CV(data):
    print('Hi! I will assign cycles to your CV data.')
    # Drop (remove) last row no to have empty (1-point) last CV cycle
    data.drop(data.tail(1).index, inplace=True)
    data['cycle'] = np.ceil(np.sign(data['control/V']).diff().ne(0).astype('int').cumsum() / 2).astype('int')
    return data