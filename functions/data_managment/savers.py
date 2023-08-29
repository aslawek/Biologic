import os

import numpy as np
import pandas as pd


def saver_data(data, filename):
    prefix = 'data_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_CV(data, filename):
    prefix = 'CV_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_on_offs(data, filename):
    prefix = 'ON-OFF_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_retention(data, filename):
    prefix = 'retention_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_data_SRDP(data, filename, dt):
    prefix = f'data_SRDP_{np.round(dt, 3)}_s_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_SRDP_each_dt(data, filename, dt):
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'SRDP_dt_{np.round(dt, 3)}_s' + '.txt'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_SRDP_summary(data, filename):
    output_filename = filename.replace("/", " ").split()[0] + "/SRDP_summary.txt"
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_data_STDP(data, filename, dt):
    # making folder for saving data_STDP
    folder_name = filename.replace("/", " ").split()[0] + "/data_STDP_" + "/"
    os.makedirs(folder_name, exist_ok=True)

#    prefix = f'data_STDP_{np.round(dt, 5)}_s_'
    prefix = f'data_STDP_' #alternative no dt in the filename
    output_filename =  folder_name + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')

    defined_dt = f'{np.round(dt, 5)}_s_'
    defined_dt_df = pd.DataFrame({'defined_dt': [defined_dt]})

    data = pd.concat([data, defined_dt_df])

    data.to_csv(f'{output_filename}', sep='\t', index=False,)

def saver_STDP(data, filename):
    full_name = '00_STDP_summary.txt'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{full_name}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_peaks_STDP(data, filename, peaks_name):
    prefix = peaks_name
    output_filename = filename.replace("/", " ").split()[
                          0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)
