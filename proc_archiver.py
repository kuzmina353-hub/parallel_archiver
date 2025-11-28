import tkinter as tk
from tkinter import filedialog, messagebox
from multiprocessing import Process, freeze_support
import os
import shutil

def archive(opened_dir_path:str):
    for included_element_name in os.listdir(opened_dir_path):
        included_element_path = os.path.join(opened_dir_path, included_element_name)
        if os.path.isdir(included_element_path):
            shutil.make_archive(
                base_name=included_element_path,
                format="zip",
                root_dir=opened_dir_path,
                base_dir=included_element_name
            )


def archive_a_directory(opened_dir_path:str, dir_name:str):
    dir_path = os.path.join(opened_dir_path, dir_name)
    try:
        shutil.make_archive(
            base_name=dir_path,
            format="zip",
            root_dir=opened_dir_path,
            base_dir=dir_name
        )
        messagebox.showinfo("Success", f"Successfully archived: '{dir_name}'")
    except Exception as e:
        messagebox.showerror("Error", f"Archive Error: '{dir_name}':\n{e}")

def choose_directory(textbox: tk.Text):
    directory = filedialog.askdirectory()
    if directory:
        textbox.delete("1.0", tk.END)
        textbox.insert(tk.END, directory)

def start_archiving(textbox: tk.Text):
    directory_path = textbox.get("1.0", tk.END).strip()
    if not os.path.isdir(directory_path):
        messagebox.showerror("Error", "Directory does not exist")
        return

    processes = []
    for name in os.listdir(directory_path):
        full_path = os.path.join(directory_path, name)
        if os.path.isdir(full_path):
            p = Process(target=archive_a_directory, args=(directory_path, name))
            p.start()
            processes.append(p)

    if not processes:
        messagebox.showinfo("Error", "No folders found")

def create_window():
    root = tk.Tk()
    root.title("Parallel Archiver")
    root.geometry("600x300")
    frame = tk.Frame(root, padx=12, pady=12)
    frame.pack(fill="both", expand=True)
    textbox = tk.Text(frame, height=3, width=60)
    textbox.grid(row=0, column=0)
    btn_choose = tk.Button(frame, text="Choose Folder",command=lambda: choose_directory(textbox))
    btn_choose.grid(row=0, column=1)
    btn_archive = tk.Button(frame, text="Archive", command=lambda: start_archiving(textbox))
    btn_archive.grid(row=1, column=0, pady=10)
    return root


if __name__ == "__main__":
    freeze_support()
    app = create_window()
    app.mainloop()
