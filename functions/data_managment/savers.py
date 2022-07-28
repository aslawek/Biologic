def saver_data(data, filename):
    prefix = 'out_'
    output_filename = filename.replace("/", " ").split()[0] + "/" + f'{prefix}{filename.replace("/", " ").split()[1]}'
    print(f'\n Saving data as {output_filename}')
    data.to_csv(f'{output_filename}', sep='\t', index=False)

def saver_SRDP(data, filename):
    prefix = 'SRDP_'
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