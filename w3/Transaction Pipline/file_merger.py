import os
import json
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

# Iterate through each directory and apply the remove_rows value to the files
for directory in directories:
    directory_formatted = directory.name.replace(' ', '_')
    if directory_formatted in folder_config:
        config = folder_config[directory_formatted]
        remove_rows = config['remove_rows']
        header = config['header']
        files = [f for f in directory.iterdir() if f.is_file()]

        for file in files:
            # Read the file, skipping the specified number of rows
            with file.open('r') as f:
                lines = f.readlines()

            # Remove the specified number of rows
            lines = lines[remove_rows:]

            # Add header if specified
            if header:
                lines.insert(0, ','.join(header) + '\n')

            # Write the modified lines back to the file
            with file.open('w') as f:
                f.writelines(lines)