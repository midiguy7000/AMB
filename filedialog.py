import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(
    title='Select any MIDI',
    defaultextension=".mid",
    filetypes=[("MIDI files", "*.mid")]
)

save_path = filedialog.asksaveasfilename(
    title='Save as',
    defaultextension='.mid',
    filetypes=[("MIDI files", "*.mid")]
)