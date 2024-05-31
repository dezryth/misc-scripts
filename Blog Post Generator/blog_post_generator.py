import os
import datetime
import random
import string
import json
import re
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, Listbox, SINGLE, END, Toplevel, Text, scrolledtext, Label, Entry, Button
from tkhtmlview import HTMLLabel
import markdown2
import yaml

# Path to the config file
config_file_path = "blog_post_generator_config.json"

# Load configuration from file
def load_config():
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            config = json.load(f)
            # Ensure all required keys are present in the configuration
            if "image_dir" not in config:
                config["image_dir"] = "/Users/YourName/Repos/blog/static/img/"
            return config
    else:
        return {
            "author": "YourName",
            "output_dir": "/Users/YourName/Repos/blog/content/post/",
            "image_dir": "/Users/YourName/Repos/blog/static/img/"
        }

# Save configuration to file
def save_config(config):
    with open(config_file_path, 'w') as f:
        json.dump(config, f, indent=4)

# Global configuration
config = load_config()

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def get_current_time():
    return datetime.datetime.now().isoformat()

def capitalize_categories(categories):
    return [cat.strip().title() for cat in categories.split(',')]

def validate_title(title):
    return re.match("^[A-Za-z0-9 _-]+$", title) is not None

def generate_post(title, author, date, url, categories, tags, thumbnail_image, additional_images, content, output_path):
    categories_str = "\n  - ".join(categories)
    tags_str = "\n  - ".join(tags)
    post_content = f"""---
title: {title}
author: {author}
type: post
date: {date}
url: {url}
categories:
  - {categories_str}
tags:
  - {tags_str}
thumbnailImage: /img/{os.path.basename(thumbnail_image)}
---
{content}
"""
    with open(output_path, 'w') as file:
        file.write(post_content)

    # Copy images to the img directory
    img_dir = config["image_dir"]
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for image_path in [thumbnail_image] + additional_images:
        if image_path:  # Ensure the path is not empty
            target_path = os.path.join(img_dir, os.path.basename(image_path))
            with open(image_path, 'rb') as src_file:
                with open(target_path, 'wb') as dest_file:
                    dest_file.write(src_file.read())

    messagebox.showinfo("Success", f"Post generated at {output_path}")

def select_source_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def select_image_file(entry, image_list, listbox):
    file_path = filedialog.askopenfilename()
    if file_path and file_path not in image_list:
        image_name = os.path.basename(file_path)
        entry.delete(0, tk.END)
        entry.insert(0, file_path)  # Store full path for copying later
        image_list.append(file_path)
        listbox.insert(END, image_name)

def remove_image(image_list, listbox):
    selected_indices = listbox.curselection()
    if selected_indices:
        selected_image = listbox.get(selected_indices[0])
        if messagebox.askyesno("Remove Image", f"Are you sure you want to remove the image {selected_image}?"):
            listbox.delete(selected_indices[0])
            full_image_path = next((img for img in image_list if os.path.basename(img) == selected_image), None)
            if full_image_path:
                image_list.remove(full_image_path)

def insert_image_reference(content_text, image_listbox):
    selected_indices = image_listbox.curselection()
    if selected_indices:
        selected_image = image_listbox.get(selected_indices[0])
        cursor_position = content_text.index(tk.INSERT)
        content_text.insert(cursor_position, f"![Description Here](/img/{selected_image})")

def preview_markdown(content_text):
    content = content_text.get("1.0", tk.END).strip()
    html_content = markdown2.markdown(content)

    preview_window = Toplevel()
    preview_window.title("Markdown Preview")

    html_label = HTMLLabel(preview_window, html=html_content)
    html_label.pack(fill="both", expand=True)

def configure_settings():
    def save_settings():
        config["author"] = author_entry.get().strip()
        config["output_dir"] = post_dir_entry.get().strip()
        config["image_dir"] = image_dir_entry.get().strip()
        save_config(config)
        settings_window.destroy()

    settings_window = Toplevel()
    settings_window.title("Configure Settings")

    Label(settings_window, text="Author:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
    author_entry = Entry(settings_window, width=50)
    author_entry.grid(row=0, column=1, padx=10, pady=5)
    author_entry.insert(0, config["author"])

    Label(settings_window, text="Post Directory:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
    post_dir_entry = Entry(settings_window, width=50)
    post_dir_entry.grid(row=1, column=1, padx=10, pady=5)
    post_dir_entry.insert(0, config["output_dir"])
    Button(settings_window, text="Browse", command=lambda: post_dir_entry.delete(0, tk.END) or post_dir_entry.insert(0, filedialog.askdirectory())).grid(row=1, column=2, padx=10, pady=5)

    Label(settings_window, text="Image Directory:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
    image_dir_entry = Entry(settings_window, width=50)
    image_dir_entry.grid(row=2, column=1, padx=10, pady=5)
    image_dir_entry.insert(0, config["image_dir"])
    Button(settings_window, text="Browse", command=lambda: image_dir_entry.delete(0, tk.END) or image_dir_entry.insert(0, filedialog.askdirectory())).grid(row=2, column=2, padx=10, pady=5)

    Button(settings_window, text="Save", command=save_settings).grid(row=3, column=1, pady=10)

def load_post():
    post_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if post_path:
        with open(post_path, 'r') as file:
            content = file.read()
        
        front_matter, post_content = content.split('---', 2)[1:3]
        front_matter = yaml.safe_load(front_matter)
        
        title_entry.delete(0, tk.END)
        title_entry.insert(0, front_matter.get('title', ''))
        
        categories_entry.delete(0, tk.END)
        categories_entry.insert(0, ', '.join(front_matter.get('categories', [])))
        
        tags_entry.delete(0, tk.END)
        tags_entry.insert(0, ', '.join(front_matter.get('tags', [])))
        
        thumbnail_entry.delete(0, tk.END)
        thumbnail_entry.insert(0, front_matter.get('thumbnailImage', '').replace('/img/', ''))
        
        additional_images.clear()
        image_listbox.delete(0, END)
        
        content_text.delete("1.0", tk.END)
        content_text.insert(tk.END, post_content.strip())

        # Extract additional images from content
        image_references = re.findall(r'!\[.*?\]\(/img/(.*?)\)', post_content)
        for img in image_references:
            img_path = os.path.join(config["image_dir"], img)
            if img_path not in additional_images:
                additional_images.append(img_path)
                image_listbox.insert(END, img)
        
        generate_button.config(text="Update Post")
        generate_button.config(command=lambda: create_post(post_path, date=front_matter.get('date')))

def create_post(output_path=None, date=None):
    title = title_entry.get().strip()
    
    # Validate title
    if not validate_title(title):
        messagebox.showerror("Invalid Title", "Title contains invalid characters. Only alphanumeric characters, spaces, hyphens, and underscores are allowed.")
        return
    
    source_path = source_entry.get().strip()

    if not title and source_path:
        if os.path.exists(source_path):
            with open(source_path, 'r') as file:
                lines = file.readlines()
            title = lines[0].strip('# ').strip()
            content = ''.join(lines)
        else:
            messagebox.showerror("Error", "Source file not found. Using default title and content.")
            title = "no-title-" + random_string()
            content = "This is a placeholder content."
    elif not title:
        title = "no-title-" + random_string()
        content = content_text.get("1.0", tk.END).strip()
    else:
        content


def main():
    global title_entry, source_entry, categories_entry, tags_entry, thumbnail_entry, content_text, image_listbox, generate_button, additional_images

    root = tk.Tk()
    root.title("Blog Post Generator")
    root.geometry("880x655")  # Set fixed size for the window
    root.resizable(False, False)  # Disable resizing

    tk.Label(root, text="Title:").grid(row=0, column=0, sticky=tk.W)
    title_entry = tk.Entry(root, width=50)
    title_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Source Markdown File:").grid(row=1, column=0, sticky=tk.W)
    source_entry = tk.Entry(root, width=50)
    source_entry.grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_source_file(source_entry)).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(root, text="Categories (comma separated):").grid(row=2, column=0, sticky=tk.W)
    categories_entry = tk.Entry(root, width=50)
    categories_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Tags (comma separated):").grid(row=3, column=0, sticky=tk.W)
    tags_entry = tk.Entry(root, width=50)
    tags_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Thumbnail Image File:").grid(row=4, column=0, sticky=tk.W)
    thumbnail_entry = tk.Entry(root, width=50)
    thumbnail_entry.grid(row=4, column=1, padx=10, pady=5)
    tk.Button(root, text="Browse", command=lambda: select_image_file(thumbnail_entry, additional_images, image_listbox)).grid(row=4, column=2, padx=10, pady=5)

    tk.Label(root, text="Content:").grid(row=5, column=0, sticky=tk.W)
    content_text = scrolledtext.ScrolledText(root, width=60, height=10)
    content_text.grid(row=5, column=1, padx=10, pady=5)
    tk.Button(root, text="Preview Markdown", command=lambda: preview_markdown(content_text)).grid(row=5, column=2, padx=10, pady=5)

    additional_images = []
    tk.Button(root, text="Add Additional Image", command=lambda: select_image_file(tk.Entry(root, width=50), additional_images, image_listbox)).grid(row=6, column=1, padx=10, pady=10)
    tk.Button(root, text="Remove Selected Image", command=lambda: remove_image(additional_images, image_listbox)).grid(row=6, column=2, padx=10, pady=10)

    image_listbox = Listbox(root, selectmode=SINGLE, width=50, height=5)
    image_listbox.grid(row=7, column=1, padx=10, pady=5)

    tk.Button(root, text="Insert Image Reference", command=lambda: insert_image_reference(content_text, image_listbox)).grid(row=8, column=1, padx=10, pady=5)
    
    load_button = tk.Button(root, text="Load Post", command=load_post)
    generate_button = tk.Button(root, text="Generate Post", command=create_post)
    load_button.grid(row=9, column=1, padx=10, pady=10, sticky=tk.E)
    generate_button.grid(row=9, column=2, padx=10, pady=10, sticky=tk.E)

    tk.Button(root, text="Configure Settings", command=configure_settings).grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    main()
