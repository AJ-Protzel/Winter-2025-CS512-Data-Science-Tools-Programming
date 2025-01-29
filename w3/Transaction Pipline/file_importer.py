# Adrien Protzel
"""
This program is a file organizer that allows users to drag and drop files into the application. 

The files are then copied to specific folders based on the user's selections for type, bank, and card.
"""

import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import shutil

# Function to handle file drop
def drop(event):
    files = root.tk.splitlist(event.data)
    for file in files:
        # Copy the file to the appropriate folder based on the selections
        copy_file(file)
    
    # Clear the fields after input of files
    type_var.set("")
    bank_var.set("")
    card_var.set("")
    
    # Ask the user if they want to continue or not
    if not messagebox.askyesno("Continue", "Do you want to continue?"):
        root.destroy()

# Function to copy the file to the appropriate folder
def copy_file(file):
    type_selection = type_var.get()
    bank_selection = bank_var.get()
    card_selection = card_var.get()
    
    # Construct the folder path relative to the current program location
    base_path = os.path.join(os.path.dirname(__file__), "Data", "Dirty")
    folder_path = os.path.join(base_path, f"{type_selection}_{bank_selection}_{card_selection}")
    
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    
    # Copy the file to the folder
    shutil.copy(file, folder_path)

# Function to update bank options based on type selection
def update_bank_options(*args):
    type_selection = type_var.get()
    
    bank_options = []
    
    if type_selection == "Debit":
        bank_options = ["BofA"]
    elif type_selection == "Credit":
        bank_options = ["BofA", "Chase", "Bilt"]
    
    bank_var.set("")
    bank_menu['menu'].delete(0, 'end')
    
    for option in bank_options:
        bank_menu['menu'].add_command(label=option, command=tk._setit(bank_var, option))
    
    update_card_options()

# Function to update card options based on type and bank selections
def update_card_options(*args):
    type_selection = type_var.get()
    bank_selection = bank_var.get()
    
    card_options = []
    
    if type_selection == "Debit" and bank_selection == "BofA":
        card_options = ["Savings"]
    elif type_selection == "Credit":
        if bank_selection == "BofA":
            card_options = ["Custom"]
        elif bank_selection == "Chase":
            card_options = ["Reserve", "Freedom", "Prime"]
        elif bank_selection == "Bilt":
            card_options = ["Bilt"]
    
    card_var.set("")
    card_menu['menu'].delete(0, 'end')
    
    for option in card_options:
        card_menu['menu'].add_command(label=option, command=tk._setit(card_var, option))

# Function to handle cancel button click
def cancel():
    root.destroy()

# Initialize main window
root = TkinterDnD.Tk()
root.title("File Organizer")

# Type dropdown
type_var = tk.StringVar()
type_label = tk.Label(root, text="Type:")
type_label.pack()
type_menu = tk.OptionMenu(root, type_var, "Credit", "Debit")
type_menu.pack()

# Bank dropdown
bank_var = tk.StringVar()
bank_label = tk.Label(root, text="Bank:")
bank_label.pack()
bank_menu = tk.OptionMenu(root, bank_var, "")
bank_menu.pack()

# Card dropdown
card_var = tk.StringVar()
card_label = tk.Label(root, text="Card:")
card_label.pack()
card_menu = tk.OptionMenu(root, card_var, "")
card_menu.pack()

# Bind update functions to type and bank dropdown changes
type_var.trace('w', update_bank_options)
bank_var.trace('w', update_card_options)

# Drag and drop area
drop_area = tk.Label(root, text="Drag and drop files here", width=40, height=10, bg="lightgray")
drop_area.pack(pady=20)
drop_area.drop_target_register(DND_FILES)
drop_area.dnd_bind('<<Drop>>', drop)

# Cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel)
cancel_button.pack(pady=10)

# Run the main loop
root.mainloop()