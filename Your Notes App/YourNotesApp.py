import os
import json
from tkinter import Tk, filedialog, Frame, Button, Listbox, Text, END, Label, Toplevel, Entry
from tkinter.scrolledtext import ScrolledText
from tkhtmlview import HTMLLabel
import markdown
from tkinter import messagebox

# Save directory path
CONFIG_FILE = "your_notes_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file).get("directory", None)
    return None

def save_config(directory):
    with open(CONFIG_FILE, "w") as file:
        json.dump({"directory": directory}, file)

class YourNotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Notes")

        # Directory and files
        self.directory = load_config()
        self.current_folder = None
        self.current_file = None

        # GUI Layout
        self.setup_ui()

        # Initial directory setup
        if not self.directory:
            self.prompt_directory_selection()
        else:
            self.load_folders()

    def setup_ui(self):
        # Frames
        self.folder_frame = Frame(self.root, width=200)
        self.folder_frame.pack(side="right", fill="y")
        
        self.note_frame = Frame(self.root)
        self.note_frame.pack(side="left", expand=True, fill="both")

        self.preview_label = Label(self.note_frame, text="Preview Mode", anchor="w")
        self.preview_label.pack(fill="x")

        self.note_display = ScrolledText(self.note_frame, state="disabled", wrap="word")
        self.note_display.pack(expand=True, fill="both")

        self.save_button = Button(self.note_frame, text="Save", command=self.save_note, state="disabled")
        self.save_button.pack(side="left")

        self.edit_button = Button(self.note_frame, text="Edit", command=self.edit_mode)
        self.edit_button.pack(side="left")

        self.preview_button = Button(self.note_frame, text="Preview", command=self.preview_mode)
        self.preview_button.pack(side="left")

        self.folder_list = Listbox(self.folder_frame)
        self.folder_list.pack(expand=True, fill="both")
        self.folder_list.bind("<<ListboxSelect>>", self.on_folder_select)

        self.file_list = Listbox(self.folder_frame)
        self.file_list.pack(expand=True, fill="both")
        self.file_list.bind("<<ListboxSelect>>", self.on_file_select)

        self.new_folder_button = Button(self.folder_frame, text="New Folder", command=self.create_new_folder)
        self.new_folder_button.pack(fill="x")

        self.new_note_button = Button(self.folder_frame, text="New Note", command=self.create_new_note)
        self.new_note_button.pack(fill="x")

        self.change_directory_button = Button(self.folder_frame, text="Change Directory", command=self.change_directory)
        self.change_directory_button.pack(fill="x")

    def prompt_directory_selection(self):
        directory = filedialog.askdirectory(title="Select Notes Directory")
        if directory:
            self.directory = directory
            save_config(directory)
            self.load_folders()

    def load_folders(self):
        if not self.directory or not os.path.exists(self.directory):
            messagebox.showerror("Error", "Invalid directory.")
            self.prompt_directory_selection()
            return

        self.folder_list.delete(0, END)
        self.file_list.delete(0, END)
        self.current_folder = None
        self.current_file = None
        
        for folder in sorted(os.listdir(self.directory)):
            folder_path = os.path.join(self.directory, folder)
            if os.path.isdir(folder_path):
                self.folder_list.insert(END, folder)

    def on_folder_select(self, event):
        selected = self.folder_list.curselection()
        if selected:
            self.current_folder = self.folder_list.get(selected[0])
            self.load_files()

    def load_files(self):
        self.file_list.delete(0, END)
        folder_path = os.path.join(self.directory, self.current_folder)
        
        for file in sorted(os.listdir(folder_path)):
            if file.endswith(".md"):
                self.file_list.insert(END, file)

    def on_file_select(self, event):
        selected = self.file_list.curselection()
        if selected:
            self.current_file = self.file_list.get(selected[0])
            self.display_file()

    def display_file(self):
        if self.current_folder and self.current_file:
            file_path = os.path.join(self.directory, self.current_folder, self.current_file)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            self.note_display.config(state="normal")
            self.note_display.delete("1.0", END)
            rendered_content = markdown.markdown(content)

            for widget in self.note_frame.winfo_children():
                if isinstance(widget, HTMLLabel):
                    widget.destroy()

            self.note_display_html = HTMLLabel(self.note_frame, html=rendered_content)
            self.note_display_html.pack(expand=True, fill="both")
            self.note_display.pack_forget()
            self.preview_label.config(text="Preview Mode")
            self.save_button.config(state="disabled")

    def edit_mode(self):
        if self.current_folder and self.current_file:
            file_path = os.path.join(self.directory, self.current_folder, self.current_file)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            for widget in self.note_frame.winfo_children():
                if isinstance(widget, HTMLLabel):
                    widget.destroy()

            self.note_display_html.pack_forget()
            self.note_display.pack(expand=True, fill="both")
            self.note_display.config(state="normal")
            self.note_display.delete("1.0", END)
            self.note_display.insert("1.0", content)
            self.preview_label.config(text="Edit Mode")
            self.save_button.config(state="normal")

    def save_note(self):
        if self.current_folder and self.current_file:
            content = self.note_display.get("1.0", END).strip()
            file_path = os.path.join(self.directory, self.current_folder, self.current_file)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            messagebox.showinfo("Success", "Note saved successfully!")

    def preview_mode(self):
        if self.current_folder and self.current_file:
            content = self.note_display.get("1.0", END).strip()
            rendered_content = markdown.markdown(content)

            for widget in self.note_frame.winfo_children():
                if isinstance(widget, HTMLLabel):
                    widget.destroy()

            self.note_display_html = HTMLLabel(self.note_frame, html=rendered_content)
            self.note_display_html.pack(expand=True, fill="both")
            self.note_display.pack_forget()
            self.preview_label.config(text="Preview Mode")
            self.save_button.config(state="disabled")

    def create_new_folder(self):
        new_folder_window = Toplevel(self.root)
        new_folder_window.title("New Folder")
        
        Label(new_folder_window, text="Folder Name:").pack(pady=5)
        folder_name_entry = Entry(new_folder_window)
        folder_name_entry.pack(pady=5)
        
        def create_folder():
            folder_name = folder_name_entry.get().strip()
            if folder_name:
                folder_path = os.path.join(self.directory, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                self.load_folders()
                new_folder_window.destroy()

        Button(new_folder_window, text="Create", command=create_folder).pack(pady=5)

    def create_new_note(self):
        if not self.current_folder:
            messagebox.showerror("Error", "Select a folder to create a new note.")
            return

        new_note_window = Toplevel(self.root)
        new_note_window.title("New Note")

        Label(new_note_window, text="Note Name (without .md):").pack(pady=5)
        note_name_entry = Entry(new_note_window)
        note_name_entry.pack(pady=5)

        def create_note():
            note_name = note_name_entry.get().strip()
            if note_name:
                note_path = os.path.join(self.directory, self.current_folder, f"{note_name}.md")
                with open(note_path, "w", encoding="utf-8") as file:
                    file.write("# New Note\n")
                self.load_files()
                new_note_window.destroy()

        Button(new_note_window, text="Create", command=create_note).pack(pady=5)

    def change_directory(self):
        new_directory = filedialog.askdirectory(title="Select New Notes Directory")
        if new_directory:
            self.directory = new_directory
            save_config(new_directory)
            self.load_folders()

if __name__ == "__main__":
    root = Tk()
    app = YourNotesApp(root)
    root.mainloop()
