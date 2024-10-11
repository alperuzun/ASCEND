import os
import shutil
from os import getcwd
import pandas as pd

def move_txt_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Debugging: Confirm the paths
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")

    for subdir, _, files in os.walk(source_folder):
        # Debugging: Confirm each subdirectory being processed
        print(f"Processing directory: {subdir}")

        for file in files:
            if file.endswith('.tsv'):
                source_path = os.path.join(subdir, file)
                destination_path = os.path.join(destination_folder, file)

                # Debugging: Confirm each file found
                print(f"Found txt file: {source_path}")

                # If a file with the same name already exists in the destination, rename it
                if os.path.exists(destination_path):
                    base, extension = os.path.splitext(file)
                    counter = 1
                    new_destination_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")
                    while os.path.exists(new_destination_path):
                        counter += 1
                        new_destination_path = os.path.join(destination_folder, f"{base}_{counter}{extension}")
                    destination_path = new_destination_path

                shutil.move(source_path, destination_path)
                # Debugging: Confirm each move operation
                print(f"Moved: {source_path} -> {destination_path}")


source_folder = getcwd() + '/data/tcga_ge_data'
destination_folder = getcwd() + '/data/processed/tcga_ge_processed'  # Replace with the desired output folder path

move_txt_files(source_folder, destination_folder)

def convert_txt_to_df(txts_path):
    count = 0
    for name in os.listdir(txts_path):
        temp_file_path = f'{txts_path}/{name}'
        df = pd.read_csv(temp_file_path, names=['site', 'beta_val'], sep='	')
        count += 1
        df.to_csv(f'{getcwd()}/data/processed/ge_dfs/df{count}.csv', index=False)
    return count

txts_path = getcwd() + '/data/processed/tcga_methyl_processed'
count = convert_txt_to_df(txts_path)
print(count)
# Combine the dataframes
def read_dataframes(directory_path):
    # List to hold all dataframes
    dfs = []
    directory_path = dir_path
    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            # Read the CSV file into a dataframe
            file_path = os.path.join(directory_path, filename)
            try:
                df = pd.read_csv(file_path)
                if df.shape == (27578, 2) and df['site'][0] == 'cg00000292':
                    dfs.append(df)
                # Ensure the dataframe has the required columns
                # if 'site' in df.columns and 'beta_val' in df.columns:
                    # Set the 'site' column as index
                    # df = df.set_index('site')
                # else:
                #     print(f"File {file_path} does not have the required columns.")
            except UnicodeDecodeError as e:
                print(f"Encoding error in file {file_path}: {e}")
                continue

    # Debug: print the shapes of all dataframes
    for i, df in enumerate(dfs):
        print(f"DataFrame {i+1} shape: {df.shape}")

    return dfs

def combined_dataframes(directory_path):
    dfs = read_dataframes(directory_path)
    # Ensure all dataframes have the same site values
    site_values = dfs[0]['site']

    # Initialize a list to hold the beta_val columns
    beta_values_list = []

    for df in dfs:
        # Set the 'site' column as index and get the beta_val column
        beta_values = df.set_index('site')['beta_val']
        beta_values_list.append(beta_values)

    # Concatenate the beta_val columns along the columns axis
    combined_df = pd.concat(beta_values_list, axis=1)
    # Set the site column as the index of the final dataframe
    combined_df.index = site_values
    # Rename the columns to differentiate the beta_val columns
    combined_df.columns = [f'patient_beta_{i + 1}' for i in range(len(dfs))]
    return combined_df


dir_path = getcwd() + '/data/processed/methyl_dfs'
combined_df = combined_dataframes(dir_path)
combined_df.to_csv(getcwd() + '/data/processed/methyl_full_df.csv', index=False)
combined_df