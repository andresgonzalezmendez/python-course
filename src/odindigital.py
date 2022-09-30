"""
Program: Odin Digital
Version: 1.0
Author: Andrés González Méndez
Date: 30 Sep 2022
Main script
"""

from tkinter import messagebox
import tkinter as tk
import odinfunctions

dialog = tk.Tk()
dialog.title("Odin Digital 1.1")
dialog.geometry("1280x720")
dialog.resizable(False, False)

button1 = tk.Button(
    dialog,
    text = "Compare images",
    command = odinfunctions.compareimages
    )
button1.pack(pady = 50)

button2 = tk.Button(
    dialog,
    text = "Button2"
    )
button2.pack(pady = 50)

button3 = tk.Button(
    dialog,
    text = "Button3"
    )
button3.pack(pady = 50)

button4 = tk.Button(
    dialog,
    text = "Button4"
    )
button4.pack(pady = 50)

def closedialog():
    """Show confirmation dialog"""
    if messagebox.askyesno(message = "Are you sure you want to close the app?"):
        dialog.destroy()

closebutton = tk.Button(
    dialog,
    text = "Close",
    command = closedialog
    )
closebutton.pack(pady = 50)

dialog.protocol("WM_DELETE_WINDOW", closedialog)

dialog.mainloop()
