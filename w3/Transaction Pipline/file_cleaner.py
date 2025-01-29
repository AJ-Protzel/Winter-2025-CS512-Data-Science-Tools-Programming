import os
import pandas as pd
import json
import shutil
import subprocess

def list_files_in_directory(directory):
    # List to store all file paths
    file_paths = []

    # Walk through directory and its subdirectories
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Append the full file path
            file_paths.append(os.path.join(root, file))

    return file_paths

def remove_star_columns_from_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Drop columns labeled "*"
    df = df.loc[:, ~df.columns.str.contains('\\*')]
    
    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

def update_csv_header(file_path, new_header):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Update the header and add empty fields for new columns if necessary
    for column in new_header:
        if column not in df.columns:
            df[column] = ""
    
    # Reorder columns to match the new header
    df = df[new_header]
    
    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

def fill_in_type_bank_card(file_path, config):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Fill in Type, Bank, Card based on config
    df['Type'] = config['type']
    df['Bank'] = config['bank']
    df['Card'] = config['card']
    
    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

def clean_amount_column(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Clean the Amount column by converting it to a float with two decimal places
    df['Amount'] = df['Amount'].replace(r'[\$,]', '', regex=True).astype(float)
    
    # Format the Amount column to show two decimal places like money
    df['Amount'] = df['Amount'].map('{:.2f}'.format)
    
    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)

# Directory to search
directory = 'Data'

# Load config.json from Configs folder
with open('Configs/config.json', 'r') as f:
    configs = json.load(f)

# New header to be applied to all CSV files
new_header = ["Year", "Month", "Date", "Description", "Category", "Amount", "Type", "Bank", "Card"]

# Get list of all files in the directory and its subdirectories
all_files = list_files_in_directory(directory)

# List to store all dataframes for merging later
dataframes = []

# Process each CSV file to remove columns labeled "*", update the header, fill in Type, Bank, Card, and clean Amount column
for file in all_files:
    if file.endswith('.csv'):
        remove_star_columns_from_csv(file)
        update_csv_header(file, new_header)
        
        # Determine the folder name and match it with config
        folder_name = os.path.basename(os.path.dirname(file))
        for config in configs:
            if folder_name == f"{config['type']}_{config['bank']}_{config['card']}":
                fill_in_type_bank_card(file, config)
                break
        
        clean_amount_column(file)
        
        # Read the cleaned CSV into a dataframe and add it to the list of dataframes
        dataframes.append(pd.read_csv(file))

# Merge all dataframes into a single dataframe
merged_df = pd.concat(dataframes)

# Save the merged dataframe to dirty.csv in the Data folder
merged_df.to_csv(os.path.join(directory, 'dirty.csv'), index=False)

# Remove old CSV files and their respective folders
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.csv') and file != 'dirty.csv':
            os.remove(os.path.join(root, file))
            
for root, dirs, files in os.walk(directory):
    for dir in dirs:
        shutil.rmtree(os.path.join(root, dir))

# Call bad_lines_cleaner.py as a subprocess
subprocess.run(['python', 'bad_lines_cleaner.py'])
