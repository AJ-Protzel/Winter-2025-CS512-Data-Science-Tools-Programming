# Adrien Protzel
"""
This program processes files in specified directories created by file_importer.py and formats based on configurations provided in a config.json file. 

It removes or adds headers as needed, records bad lines, and merges like files.
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

# Iterate through each directory and apply the remove_rows value to the files
for directory in directories:
    directory_formatted = directory.name.replace(' ', '_')
    if directory_formatted in folder_config:
        config = folder_config[directory_formatted]
        remove_rows = config['remove_rows']
        add_header = config.get('add_header', None)
        files = [f for f in directory.iterdir() if f.is_file()]

        all_lines = []

        for file in files:
            try:
                # Read the file, skipping the specified number of rows
                with file.open('r') as f:
                    lines = f.readlines()

                # Remove the specified number of rows
                lines = lines[remove_rows:]

                # Add header if specified
                if add_header:
                    lines.insert(0, ','.join(add_header) + '\n')

                # Write the modified lines back to the file
                with file.open('w') as f:
                    f.writelines(lines)

                # Check for bad lines and write them to bad_lines.txt
                with file.open('r') as f:
                    reader = csv.reader(f)
                    lines = list(reader)

                cleaned_lines = []
                bad_lines_path = folder_path / 'bad_lines.txt'
                with open(bad_lines_path, 'a') as bad_lines_log:
                    for row in lines:
                        try:
                            if len(row) != len(lines[0]):  # Check if the row length matches the header length
                                raise ValueError("Bad line")
                            cleaned_lines.append(row)  # Add valid rows to the cleaned_lines list
                        except Exception:
                            bad_lines_log.write(f"{file}: {row}\n")  # Log bad lines

                # Add cleaned lines to all_lines
                all_lines.extend(cleaned_lines)

                # Remove the old file
                file.unlink()

            except Exception as e:
                print(f"Error processing file {file}: {e}")

        # Write all cleaned lines to a new merged file
        merged_file_path = directory / f"{config['type']}_{config['bank']}_{config['card']}.csv"
        with merged_file_path.open('w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(all_lines)