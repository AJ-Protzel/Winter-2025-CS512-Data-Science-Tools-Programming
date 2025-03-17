import pandas as pd
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'clean.csv')

# Load the CSV file
df = pd.read_csv(file_path)

# Split the Date field into Day
df['Day'] = df['Date'].str.split('/', expand=True)[1]

# Add a column ID with a unique id for each record
df['ID'] = range(1, len(df) + 1)

# Delete records where Category is 'transfer' or 'expense'
df = df[~df['Category'].isin(['transfer', 'expense'])]

# Reorder columns to place ID at the beginning while keeping the original Date field
df = df[['ID', 'Year', 'Month', 'Day', 'Date', 'Description', 'Category', 'Amount', 'Type', 'Bank', 'Card']]

# Save the modified CSV file
df.to_csv(os.path.join(current_dir, 'clean_modified.csv'), index=False)

print("Complete")