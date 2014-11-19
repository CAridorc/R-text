# -*- coding: utf-8 -*-
try:
    import tkinter as tk
except:
    import Tkinter as tk

try:
    import tkMessageBox as pop_up
except:
    import tkinter.tkMessageBox as pop_up

import datetime

import glob

import os


TXT_EXTENSION = ".txt"
ALL_CHARS = "abcdefghijklmnopqrstuvwxyz12345690"

EMPTY_TITLE_ERROR_MESSAGE_SAVE = "Please write the name of the file you want to save in the given field."
EMPTY_TITLE_ERROR_MESSAGE_OPEN = "Please write the name of the file you want to open in the given field."
FILE_NOT_FOUND_ERROR_MESSAGE = "No file with the given title was found, remember that this text editor can only read files in its directory."
INVALID_CHRACTERS_MESSAGE = "Unicode does not allow accented letters, please replace them in the following way: è -> e', à -> a'."
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please be sure that the file you want to open exists and that it is in the same folder of this editor."
SAVING_SUCCESS_MESSAGE = "Your text is now stored in the {filename} file"


def _open():
    filename = tkFileDialog.askopenfilename()
    file_title.delete(0, tk.END)
    file_title.insert(tk.INSERT, filename)
    with open(filename) as f:
        main_text.delete("1.0", tk.END)
        main_text.insert(tk.INSERT, f.read(), "a")

def list_files():
    files = '\n'.join([file for file in glob.glob("*.txt")])
    pop_up.showinfo("All the files","Down here you can see all the files you can open with this text editor:\n\n"+files)


def save():
    if not file_title.get():
        pop_up.showerror("No title.", EMPTY_TITLE_ERROR_MESSAGE_SAVE)
        return 1
    
    try:
        title = file_title.get()
    except UnicodeEncodeError:
        pop_up.showerror("Invalid characters",INVALID_CHRACTERS_MESSAGE)
        return 1
        
    if not TXT_EXTENSION in file_title.get():
        filename = title + TXT_EXTENSION
    
    with open(filename, "w+") as f:
        try:
            f.write(main_text.get(1.0, tk.END))
        except UnicodeEncodeError:
            pop_up.showerror("Invalid characters",INVALID_CHRACTERS_MESSAGE)
            return 1
        
        try:
            pop_up.showinfo("File saved succesfully.",
SAVING_SUCCESS_MESSAGE.format(filename=filename))
        except UnicodeEncodeError:
            pop_up.showerror("Invalid characters",INVALID_CHRACTERS_MESSAGE)


def add_date():
    date = "\n" + str(datetime.date.today())
    main_text.insert(tk.INSERT, date, "a")


def add_signature():
    try:
        with open("signature.txt") as f:
            data = f.read()
            print(data)
            if not any([i in data for i in ALL_CHARS]): # is empty
                pop_up.showerror("\"signature.txt\" is empty.","Please write your signature to that file.")
                return 1
            main_text.insert(tk.INSERT, "\n" + data, "a")
    except IOError:
        MESSAGE = SIGNATURE_TXT_NOT_FOUND_MESSAGE
        pop_up.showerror("\"signature.txt\" not found.", MESSAGE)


root = tk.Tk()
root.wm_title("R Text")

menubar = tk.Menu(root)
menubar.add_command(label="Open", command=_open)
menubar.add_command(label="List files", command=list_files)
menubar.add_command(label="Save", command=save)
menubar.add_command(label="Add signature", command=add_signature)
menubar.add_command(label="Add date", command=add_date)

root.config(menu=menubar)

top = tk.Frame(root)
temp = tk.Label(root, text="Title:")
temp.pack(in_=top, side=tk.LEFT)

file_title = tk.Entry(root)
file_title.pack(in_=top, side=tk.RIGHT)

top.pack()

main_text = tk.Text(root)
main_text.pack()

tk.mainloop()

