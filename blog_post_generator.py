import os
import datetime
import random
import string
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# Path to the config file
config_file_path = "blog_post_generator_config.json"

# Load configuration from file
def load_config():
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as f:
            return json.load(f)
    else:
        return {
            "author": "YourName",
            "output_dir": "/Users/YourName/Repos/blog/content/post/"
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

def generate_post(title, author, date, url, categories, thumbnail_image, content, output_path):
    categories_str = "\n  - ".join(categories)
    post_content = f"""---
title: {title}
author: {author}
type: post
date: {date}
url: {url}
categories:
  - {categories_str}
thumbnailImage: /img/{thumbnail_image}
---
{content}
"""
    with open(output_path, 'w') as file:
        file.write(post_content)
    messagebox.showinfo("Success", f"Post generated at {output_path}")

def select_source_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def configure_settings():
    global config
    author = simpledialog.askstring("Input", "Enter the author name:", initialvalue=config["author"])
    if author:
        config["author"] = author
    output_dir = filedialog.askdirectory(initialdir=config["output_dir"], title="Select Output Directory")
    if output_dir:
        config["output_dir"] = output_dir
    save_config(config)

def main():
    def create_post():
        title = title_entry.get().strip()
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
            content = content_text.get("1.0", tk.END).strip()

        author = config["author"]
        date = get_current_time()
        url = f"/{datetime.datetime.now().strftime('%Y/%m/%d')}/{title.lower().replace(' ', '-')}/"
        
        categories_input = categories_entry.get().strip()
        categories = capitalize_categories(categories_input)

        thumbnail_image = thumbnail_entry.get().strip()
        if not thumbnail_image:
            thumbnail_image = "default-thumbnail.png"

        output_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{title.lower().replace(' ', '-')}.md"
        output_path = os.path.join(config["output_dir"], output_filename)

        generate_post(title, author, date, url, categories, thumbnail_image, content, output_path)

    root = tk.Tk()
    root.title("Blog Post Generator")

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

    tk.Label(root, text="Thumbnail Image File Name:").grid(row=3, column=0, sticky=tk.W)
    thumbnail_entry = tk.Entry(root, width=50)
    thumbnail_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Content:").grid(row=4, column=0, sticky=tk.W)
    content_text = tk.Text(root, width=60, height=10)
    content_text.grid(row=4, column=1, padx=10, pady=5)

    tk.Button(root, text="Generate Post", command=create_post).grid(row=5, column=1, padx=10, pady=10)
    tk.Button(root, text="Configure Settings", command=configure_settings).grid(row=5, column=0, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
