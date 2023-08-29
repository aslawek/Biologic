import os
import originpro as op

print('filename: ', os.getcwd())

#folder_path = 'data/'  # Replace with the actual folder path
#folder_path_STDP = 'data/data_STDP_/'  # Replace with the actual folder path
#folder_path_READ= 'data/read_peaks_/'  # Replace with the actual folder path
#folder_path_RESET = 'data/reset_peaks_/'  # Replace with the actual folder path

# Get a list of files in each of the folders
#file_list_STDP = [file for file in os.listdir(folder_path_STDP) if file.endswith(".txt")]  # Adjust the file extension if needed
#file_list_READ = [file for file in os.listdir(folder_path_READ) if file.endswith(".txt")]  # Adjust the file extension if needed
#file_list_RESET = [file for file in os.listdir(folder_path_RESET) if file.endswith(".txt")]  # Adjust the file extension if needed


#mkdir(folder_name)

# Loop through each file and import it into OriginPro

#file_path = os.path.join(folder_path, file_name)
new_sheet()
import_file(file_path)
workbook_name = file_name[:-4]  # Remove the file extension from the workbook name
save(workbook_name, overwrite=True)
