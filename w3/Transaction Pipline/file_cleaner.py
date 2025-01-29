import json
import csv
from pathlib import Path
from datetime import datetime
import shutil
import subprocess

# Define constants for folder and configuration paths
FOLDER_PATH = Path('Data')
CONFIG_PATH = Path('Configs/config.json')
MERGED_FILE_PATH = Path('Data/dirty.csv')

# Define the desired column order and default values
DESIRED_COLUMNS = ["Year", "Month", "Date", "Description", "Category", "Amount", "Type", "Bank", "Card"]
DEFAULT_VALUES = {
    "Year": 0,
    "Month": "",
    "Date": "01/25/2025",
    "Description": "",
    "Category": "",
    "Amount": 0.00,
    "Type": "",
    "Bank": "",
    "Card": ""
}

def load_config(config_path):
    """Load the configuration file."""
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def map_folder_config(config_data):
    """Create a dictionary to map folder names to their configurations."""
    return {f"{entry['type']}_{entry['bank']}_{entry['card']}": entry for entry in config_data}

def list_directories(folder_path):
    """List all directories in the specified folder path."""
    return [d for d in folder_path.iterdir() if d.is_dir()]

def clean_amount(amount):
    """Clean the Amount column by removing commas and converting to float."""
    try:
        return float(amount.replace(',', ''))
    except ValueError:
        return 0.0

def format_amount(amount):
    """Format the Amount to two decimal places."""
    return f"{amount:.2f}"

def normalize_headers(header, header_mapping):
    """Normalize headers based on the configuration mapping."""
    return [header_mapping.get(col, col) for col in header]

def remove_unwanted_columns(lines, columns_to_remove):
    """Remove columns labeled with '*' from the data."""
    return [[cell for i, cell in enumerate(row) if i not in columns_to_remove] for row in lines]

def create_new_header(normalized_header):
    """Create a new header in the desired order."""
    new_header = []
    for col in DESIRED_COLUMNS:
        if col in normalized_header:
            new_header.append(col)
        else:
            new_header.append(col)
    return new_header

def reorder_rows(lines, new_header, normalized_header):
    """Reorder the rows to match the new header order."""
    col_indices = {col: idx for idx, col in enumerate(normalized_header)}
    reordered_lines = [new_header]
    for row in lines[1:]:
        new_row = [row[col_indices[col]] if col in col_indices else DEFAULT_VALUES[col] for col in new_header]
        reordered_lines.append(new_row)
    return reordered_lines

def fill_additional_columns(reordered_lines, config, new_header):
    """Fill in additional columns with values from the configuration."""
    type_index = new_header.index("Type")
    bank_index = new_header.index("Bank")
    card_index = new_header.index("Card")
    amount_index = new_header.index("Amount")
    date_index = new_header.index("Date")
    year_index = new_header.index("Year")
    month_index = new_header.index("Month")
    
    for row in reordered_lines[1:]:
        row[type_index] = config['type']
        row[bank_index] = config['bank']
        row[card_index] = config['card']
        row[amount_index] = format_amount(clean_amount(row[amount_index]))
        try:
            date_obj = datetime.strptime(row[date_index], "%m/%d/%Y")
            row[year_index] = date_obj.year
            row[month_index] = date_obj.strftime("%B")
        except ValueError:
            row[year_index] = 0
            row[month_index] = ""
    return reordered_lines

def process_files(directory, config, header_mapping):
    """Process each file in the directory, normalize headers, and fill additional columns."""
    files = [f for f in directory.iterdir() if f.is_file() and f.suffix == '.csv']
    
    for file in files:
        try:
            with file.open('r') as f:
                reader = csv.reader(f)
                lines = list(reader)

            header = lines[0]
            normalized_header = normalize_headers(header, header_mapping)
            columns_to_remove = [i for i, col in enumerate(normalized_header) if col == "*"]
            normalized_header = [col for i, col in enumerate(normalized_header) if i not in columns_to_remove]
            lines = remove_unwanted_columns(lines, columns_to_remove)
            new_header = create_new_header(normalized_header)
            reordered_lines = reorder_rows(lines, new_header, normalized_header)
            reordered_lines = fill_additional_columns(reordered_lines, config, new_header)

            # Write the cleaned data to a new file in the same directory
            clean_file_path = directory / file.name
            with clean_file_path.open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(reordered_lines)

        except Exception as e:
            print(f"Error processing file {file}: {e}")

def merge_files():
    """Merge all files in the Data folder and its subfolders into one CSV file called dirty.csv without duplicating headers."""
    files_to_merge = [f for f in FOLDER_PATH.rglob('*.csv') if f.is_file()]
    
    with MERGED_FILE_PATH.open('w', newline='') as merged_file:
        writer = csv.writer(merged_file)
        
        # Write header only once
        header_written = False
        
        for file in files_to_merge:
            with file.open('r') as f:
                reader = csv.reader(f)
                header = next(reader)
                
                if not header_written:
                    writer.writerow(header)
                    header_written = True
                
                for row in reader:
                    writer.writerow(row)

def remove_old_files():
    """Remove all old CSV files and folders from the Data folder after merging them."""
    files_to_remove = [f for f in FOLDER_PATH.rglob('*.csv') if f.is_file() and f != MERGED_FILE_PATH]
    folders_to_remove = [d for d in FOLDER_PATH.iterdir() if d.is_dir()]
    
    for file in files_to_remove:
        file.unlink()
    
    for folder in folders_to_remove:
        shutil.rmtree(folder)

def main():
    """Main function to load configuration, list directories, process files, merge them, remove old files, and call subprocesses."""
    config_data = load_config(CONFIG_PATH)
    folder_config = map_folder_config(config_data)
    directories = list_directories(FOLDER_PATH)

    for directory in directories:
        directory_formatted = directory.name.replace(' ', '_')
        if directory_formatted in folder_config:
            config = folder_config[directory_formatted]
            header_mapping = config.get('header_mapping', {})
            process_files(directory, config, header_mapping)

    # Merge all cleaned files into one CSV file called dirty.csv
    merge_files()

    # Remove old CSV files and folders from the Data folder
    remove_old_files()

    # Call the bad_lines_cleaner.py subprocess
    subprocess.run(["python", "bad_lines_cleaner.py"])

    # Find the year and month from the date after merging and deleting old files
    with MERGED_FILE_PATH.open('r') as merged_file:
        reader = csv.DictReader(merged_file)
        for row in reader:
            try:
                date_obj = datetime.strptime(row["Date"], "%m/%d/%Y")
                year = date_obj.year
                month = date_obj.strftime("%B")
                print(f"Year: {year}, Month: {month}")
            except ValueError:
                print("Invalid date format")

    # Call the desc_cleaner.py subprocess
    subprocess.run(["python", "desc_cleaner.py"])

if __name__ == "__main__":
    main()