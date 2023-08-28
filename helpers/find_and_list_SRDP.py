import os

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    # Here You put the name of the folder where the data is kept (relative to ../Biologic/)
    data_folder = "test"

    # Here type phrases that appear in files that you DO care about:
    phrases = [
        'start_CV_04_CA_C01',
        'start_CV_07_CA_C01',
        'start_CV_10_CA_C01',
        'start_CV_13_CA_C01',
        'start_CV_16_CA_C01',
        'end_CV_02_CA_C01',
        'end_CV_05_CA_C01',
        'end_CV_08_CA_C01',
        'end_CV_11_CA_C01',
        'end_CV_14_CA_C01'
    ]

    list_filenames = os.listdir(f'./{data_folder}')

    print('\nALL files:')
    print('\nlist_filenames = [')
    for index, filename in enumerate(list_filenames):
        if index != len(list_filenames) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")
    print(']')

    list_filenames_good = []
    for filename in list_filenames:
        for phrase in phrases:
            if phrase in filename:
                list_filenames_good.append(filename)

    print('\nGOOD files:')
    print('\nlist_filenames = [')
    for index, filename in enumerate(list_filenames_good):
        if index != len(list_filenames_good) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")
    print(']')

    #print(f'\nList of files in {data_folder}:')
    #for index, filename in enumerate(list_filenames):
    #    if index != len(list_filenames) - 1:
    #        print(f"'{data_folder}/{filename}',")
    #    else:
    #        print(f"'{data_folder}/{filename}'")

    # 1st phrase for filtering
    #list_filenames = list(filter(lambda x: x.startswith(filter_phrases), list_filenames))

    #print(list_filenames)

del(main)