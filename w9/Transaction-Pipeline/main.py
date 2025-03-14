"""
Author: Adrien Protzel

This program sequentially calls other scripts to import, manage, and clean data.
"""

import subprocess
import os

if __name__ == "__main__":
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ask user to import files and to which folder <Type>_<Bank>_<Card>
    subprocess.run(["python", os.path.join(current_dir, "file_importer.py")])
    print("File Importing......Done")

    # Cleans headers and merges multiple files in single bank account file
    subprocess.run(["python", os.path.join(current_dir, "file_merger.py")])
    print("File Merging......Done")

    # Removes, renames, adds, splits columns, merges into single clean file in Clean folder
    subprocess.run(["python", os.path.join(current_dir, "file_cleaner.py")])
    print("File Cleaning......Done")

    # # Convert CSV to JSON
    # subprocess.run(["python", os.path.join(current_dir, "CSV_to_JSON.py")])
    # print("CSV to JSON......Done")

    # # Convert JSON to CSV
    # subprocess.run(["python", os.path.join(current_dir, "JSON_to_CSV.py")])
    # print("JSON to CSV......Done")