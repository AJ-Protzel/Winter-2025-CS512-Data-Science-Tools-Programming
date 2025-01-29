# Adrien Protzel
"""
This program processes files in specified directories created by file_importer.py and formats based on configurations provided in a config.json file. 

It removes columns as specified in the configuration file.
"""

import json
import csv
from pathlib import Path

# Define the folder path
folder_path = Path('Data/Dirty')

# Load the configuration file
config_path = Path('Configs/config.json')
with open(config_path, 'r') as config_file:
    config_data = json.load(config_file)

# Create a dictionary to map folder names to their configurations
folder_config = {f"{entry['type']}_{entry['bank']}_{entry['card']}": entry for entry in config_data}

# List all directories in the specified folder path
directories = [d for d in folder_path.iterdir() if d.is_dir()]

# Iterate through each directory and apply the remove_cols value to the files
for directory in directories:
    directory_formatted = directory.name.replace(' ', '_')
    if directory_formatted in folder_config:
        config = folder_config[directory_formatted]
        remove_cols = config.get('remove_cols', [])
        files = [f for f in directory.iterdir() if f.is_file() and f.suffix == '.csv']

        for file in files:
            try:
                # Read the file
                with file.open('r') as f:
                    reader = csv.reader(f)
                    lines = list(reader)

                # Map column names to indices
                header = lines[0]
                col_indices_to_remove = [header.index(col) for col in remove_cols if col in header]

                # Remove specified columns
                cleaned_lines = []
                for row in lines:
                    cleaned_row = [col for idx, col in enumerate(row) if idx not in col_indices_to_remove]
                    cleaned_lines.append(cleaned_row)

                # Write the modified lines back to the file
                with file.open('w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(cleaned_lines)

            except Exception as e:
                print(f"Error processing file {file}: {e}")