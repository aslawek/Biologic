import os

# sth similar to IIFE
main = lambda f: f()
@main
def main():
    # Here You put the name of the folder where the data is kept (relative to ../Biologic/)
    data_folder = "data"
    # Here You put the type of Biologic data (_CV_, _CA_, etc.), set to "" if not important
    data_type = ""
    # Additional filter, i.e. part of filename
    filter_phrase = input('Type any additional filtering criteria (or press Enter): ')

    list_filenames = os.listdir(f'./{data_folder}')
    list_filenames = list(filter(lambda str: data_type in str, list_filenames))
    list_filenames = list(filter(lambda str: filter_phrase in str, list_filenames))

    print('list_filenames = [')
    for index, filename in enumerate(list_filenames):
        if index != len(list_filenames) - 1:
            print(f"'{data_folder}/{filename}',")
        else:
            print(f"'{data_folder}/{filename}'")
    print(']')

del(main)