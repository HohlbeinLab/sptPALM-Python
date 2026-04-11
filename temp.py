# %%
import pickle
import tkinter as tk
from tkinter import filedialog

# Open file dialog to select pkl file
root = tk.Tk()
root.withdraw()  # hide the main window
root.lift()
root.focus_force()

filepath = filedialog.askopenfilename(
    title="Select pickle file",
    filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
)
root.destroy()

# Load and display
if filepath:
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    data
else:
    print("No file selected")
# %%
