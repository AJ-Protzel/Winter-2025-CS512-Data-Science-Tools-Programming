import subprocess

if __name__ == "__main__":
    # Csk user to import files and to which folder <Type>_<Bank>_<Card>
    subprocess.run(["python", "file_importer.py"])
    print("File Importing......Done")

    # Cleans headers and merges multiple files in single bank account folder
    subprocess.run(["python", "file_merger.py"])
    print("File Merging......Done")

    # Removes, renames, adds, splits columns

    # remove / fix headers
    # merge like Files 

    # remove unwanted cols
    # rename cols
    # add cols / split cols
    # fix fields using maps
