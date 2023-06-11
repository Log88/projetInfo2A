import os
import shutil
import tkinter as tk
from tkinter import filedialog

def zip_folder(src_folder):
    # create a zip file (overwrites existing one if it exists)
    shutil.make_archive(src_folder, 'zip', src_folder)

def download(src_folder):
    # Zip the folder
    zip_folder(src_folder)
    
    # Create a save dialog to choose where to save the zipped folder
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.asksaveasfilename(defaultextension='.zip',
                                             initialfile=os.path.basename(src_folder),
                                             filetypes=[('Zip Files', '*.zip')])
    if file_path:  # If a file path was chosen
        shutil.move(f'{src_folder}.zip', file_path)
        print('Folder zipped and saved successfully.')
    else:
        print('Folder zipping was cancelled.')
    root.destroy()  # Destroy the tkinter instance
    
    # Delete the local zip file if it exists
    if os.path.exists(f'{src_folder}.zip'):
        os.remove(f'{src_folder}.zip')

if __name__ == "__main__":
    folder = r"C:\Users\logan\Desktop\DOCZZ\ECOLE\2A\PROJET INFO FINAL\data\Database_bg\ScrapedData_bg"
    download(folder)
