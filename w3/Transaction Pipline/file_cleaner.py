# Adrien Protzel
"""
This program processes files in specified directories created by file_importer.py and formats based on configurations provided in a config.json file. 

It normalizes headers based on the configuration file, adds new columns if they aren't present, and fills in specific columns with values from the configuration file.
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

# Define the desired column order and default values
desired_columns = ["Year", "Month", "Date", "Description", "Category", "Amount", "Type", "Bank", "Card"]
default_values = {
    "Year": "",
    "Month": "",
    "Date": "01/25/2025",
    "Description": "",
    "Category": "",
    "Amount": "0.00",
    "Type": "",
    "Bank": "",
    "Card": ""
}

# Iterate through each directory and normalize headers
for directory in directories:
    directory_formatted = directory.name.replace(' ', '_')
    if directory_formatted in folder_config:
        config = folder_config[directory_formatted]
        header_mapping = config.get('header_mapping', {})
        files = [f for f in directory.iterdir() if f.is_file() and f.suffix == '.csv']

        for file in files:
            try:
                # Read the file
                with file.open('r') as f:
                    reader = csv.reader(f)
                    lines = list(reader)

                # Normalize headers
                header = lines[0]
                normalized_header = [header_mapping.get(col, col) for col in header]

                # Create a new header in the desired order
                new_header = []
                for col in desired_columns:
                    if col in normalized_header:
                        new_header.append(col)
                    else:
                        new_header.append(col)
                        for row in lines[1:]:
                            row.append(default_values[col])

                # Reorder the rows to match the new header order
                col_indices = {col: idx for idx, col in enumerate(normalized_header)}
                reordered_lines = [new_header]
                for row in lines[1:]:
                    new_row = [row[col_indices[col]] if col in col_indices else default_values[col] for col in new_header]
                    reordered_lines.append(new_row)

                # Fill in the "Type", "Bank", and "Card" columns with values from the config
                type_index = new_header.index("Type")
                bank_index = new_header.index("Bank")
                card_index = new_header.index("Card")
                for row in reordered_lines[1:]:
                    row[type_index] = config['type']
                    row[bank_index] = config['bank']
                    row[card_index] = config['card']

                # Write the modified lines back to the file
                with file.open('w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(reordered_lines)

            except Exception as e:
                print(f"Error processing file {file}: {e}")