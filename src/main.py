from textnode import TextNode, TextType
import os, shutil
from gencontent import *
import sys

def copy_destination(src,dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    
    recursive_copy(src,dst)
    
def recursive_copy(src,dst):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            recursive_copy(src_path, dst_path)
    
def main():
    if len(sys.argv)>1:
        basepath = sys.argv
    else:
        basepath = "/"
    copy_destination("static","docs")
    generate_page_recursive(basepath,"content", "template.html", "docs")
    

if __name__ == "__main__":
    main()