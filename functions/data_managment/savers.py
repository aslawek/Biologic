import numpy as np

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

def saver_SRDP(data, filename):
    prefix = 'SRDP_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)