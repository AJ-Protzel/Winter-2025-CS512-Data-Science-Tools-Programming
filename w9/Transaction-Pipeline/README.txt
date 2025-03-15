# Transaction-pipeline

## Description
This project processes various stages of data, including raw data, to achieve [briefly describe the goal or output of your project].

## Prerequisites
- Python 3.x
- Any additional libraries or dependencies (list them here)

## Usage
1. Run the main script:
    ```bash
    python main.py
    ```

2. Follow the window prompt instructions.

3. Drag and drop the raw data from the `Backup Data` folder into the window to continue the program.

4. In the **Bad Lines** window:
    - Read the bad line text at the top of the window.
    - Manually enter the following details:
        - **Date**
        - **Amount**
        - **Type**: credit/debit
        - **Account**: BofA
        - **Card**: Savings
    - The category and description mappings should be complete, but if prompted:
        - Enter the keyword in the description.
        - Provide the true description of the transaction.
        - Enter the category type of the transaction (e.g., dining, groceries, gas, etc.).

## Data
- **Backup Data**: Contains various stages of data, including raw data.

## Main Files

### Main Script
Author: Adrien Protzel

This program sequentially calls other scripts to import, manage, and clean data.

### JSON to CSV Converter
Author: Adrien Protzel

This script converts a JSON file to a CSV file and then removes the original JSON file.

Modules used:
- csv: For writing the CSV file.
- json: For reading the JSON file.
- os: For interacting with the operating system.

Functions:
- json_to_csv(json_file_path, csv_file_path): Converts a JSON file to a CSV file and removes the original JSON file.

### File Processor
Author: Adrien Protzel

This program processes files in specified directories created by file_importer.py and formats based on configurations provided in a config.json file. 

It removes or adds headers as needed, records bad lines, and merges like files.

### GUI Application for File Organization
Author: Adrien Protzel

This script creates a GUI application using Tkinter to organize files based on user selections. Users can drag and drop files into the application, which then copies the files to appropriate folders based on the selected type, bank, and card.

Modules used:
- tkinter: For creating the GUI.
- tkinterdnd2: For drag-and-drop functionality in Tkinter.
- os: For interacting with the operating system.
- shutil: For file operations.
- json: For reading configuration files.

Functions:
- drop(event): Handles file drop events and copies files to appropriate folders.
- copy_file(file): Copies a file to the appropriate folder based on user selections.
- update_bank_options(*args): Updates bank options based on the selected type.
- update_card_options(*args): Updates card options based on the selected type and bank.
- cancel(): Closes the application.
- create_dropdown(label_text, variable, options, parent, default_value): Creates a dropdown menu with a label.
- center_window(window, width, height): Centers the window on the screen with specified width and height.

### CSV File Processor
Author: Adrien Protzel

This script processes CSV files in a directory by performing various cleaning and transformation tasks. It merges the cleaned data into a single CSV file and then runs additional cleaning scripts.

Modules used:
- os: For interacting with the operating system.
- pandas: For data manipulation and analysis.
- json: For reading configuration files.
- shutil: For file operations.
- subprocess: For running external scripts.
- datetime: For date and time operations.

Functions:
- list_files_in_directory(directory): Lists all files in a directory and its subdirectories.
- remove_star_columns_from_csv(file_path): Removes columns labeled "*" from a CSV file.
- update_csv_header(file_path, new_header): Updates the header of a CSV file and adds empty fields for new columns if necessary.
- fill_in_type_bank_card(file_path, config): Fills in Type, Bank, and Card columns based on a configuration.
- clean_amount_column(file_path): Cleans the Amount column by converting it to a float with two decimal places.
- fill_year_month_columns(file_path): Extracts Year and Month from the Date column.
- remove_empty_amount_rows(file_path): Removes rows where the Amount column is empty or NaN.

### Description Replacement
Author: Adrien Protzel

This script processes a CSV file to replace transaction descriptions based on a predefined mapping. If a description does not match any keyphrase, a manual input window is displayed to allow the user to enter the correct description.

Modules used:
- pandas: For data manipulation and analysis.
- tkinter: For creating the GUI.

Functions:
- load_description_map(): Loads the description map from a file.
- replace_description(row): Replaces descriptions based on the mapping and displays a manual input window if no match is found.

### CSV to JSON Converter
Author: Adrien Protzel

This script converts a CSV file to a JSON file and then removes the original CSV file.

Modules used:
- csv: For reading the CSV file.
- json: For writing the JSON file.
- os: For interacting with the operating system.

Functions:
- csv_to_json(csv_file_path, json_file_path): Converts a CSV file to a JSON file and removes the original CSV file.

### Transaction Categorizer
Author: Adrien Protzel

This script processes a CSV file to categorize transaction descriptions. It uses a predefined category map to automatically categorize descriptions. If a description does not match any category, a manual input window is displayed to allow the user to categorize the transaction.

Modules used:
- pandas: For data manipulation and analysis.
- tkinter: For creating the GUI.
- os: For interacting with the operating system.

Functions:
- load_category_map(): Loads the category map from a file.
- check_description(row): Checks the description against the category map and displays a manual input window if no match is found.

### Bad Lines Cleaner
Author: Adrien Protzel

This script creates a GUI application using Tkinter to manually clean up bad lines from a file. It reads bad lines from a specified file, displays them in a pop-up window, and allows the user to manually enter the correct information. The corrected data is then written to a CSV file.

Modules used:
- tkinter: For creating the GUI.
- tkinterdnd2: For drag-and-drop functionality in Tkinter.
- pathlib: For handling file paths.
- csv: For reading and writing CSV files.
- os: For interacting with the operating system.
