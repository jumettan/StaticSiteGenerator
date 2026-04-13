from htmlnode import *
from markdown_blocks import *
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line = line[2:]
            return line.strip()
        else:
            continue
    raise Exception("no header found")

def generate_page(basepath,from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_page_recursive(basepath,content_dir,template_path,public_dir):
    for item in os.listdir(content_dir):
        content_path = os.path.join(content_dir, item)
        public_path = os.path.join(public_dir, item)
        
        if os.path.isfile(content_path):
            if item == "index.md":
                dest_file = os.path.join(public_dir, "index.html")
                generate_page(basepath,content_path,template_path,dest_file)
        else:
            os.makedirs(public_path, exist_ok=True)
            generate_page_recursive(basepath,content_path, template_path, public_path)