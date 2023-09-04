import os

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    # Here You put the name of the folder where the data is kept (relative to ../Biologic/)
    data_folder = "data_examples"

    list_filenames = os.listdir(f'./{data_folder}')

    print(f'\nList of files in {data_folder}:')
    for index, filename in enumerate(list_filenames):
        if index != len(list_filenames) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")

    # 1st phrase for filtering
    filter_phrase_1 = input('\nType 1st phrase for filtering criteria (or press Enter): ')
    list_filenames = list(filter(lambda str: filter_phrase_1 in str, list_filenames))

    print('\nlist_filenames = [')
    for index, filename in enumerate(list_filenames):
        if index != len(list_filenames) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")
    print(']')

    # 2nd phrase for filtering
    filter_phrase_2 = input('\nType any additional filtering criteria (or press Enter): ')
    list_filenames = list(filter(lambda str: filter_phrase_2 in str, list_filenames))

    print('\nlist_filenames = [')
    for index, filename in enumerate(list_filenames):
        if index != len(list_filenames) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")
    print(']')

del(main)