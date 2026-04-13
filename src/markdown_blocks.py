from enum import Enum
from inline_markdown import *
from htmlnode import *
from textnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE

    if lines[0].startswith("#"):
        count = len(lines[0]) - len(lines[0].lstrip("#"))
        if 1 <= count <= 6 and lines[0][count] == " ":
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # 🔹 DEFAULT
    return BlockType.PARAGRAPH

def text_to_children(text):
    new_list = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        new_list.append(text_node_to_html_node(node))
    return new_list

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    children = []
    for block in md_blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.PARAGRAPH:
            lines = block.split("\n")
            stripped_lines = [line.strip() for line in lines]
            paragraph = " ".join(stripped_lines)
            children.append(ParentNode("p", text_to_children(paragraph)))
        if blocktype == BlockType.HEADING:
            heading_lvl=block.split(" ",1)
            level = len(heading_lvl[0])
            children.append(ParentNode(f"h{level}", text_to_children(heading_lvl[1])))     
        if blocktype == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            final = " ".join(new_lines)    
            children.append(ParentNode("blockquote", text_to_children(final)))
        if blocktype == BlockType.UNORDERED_LIST:
            items = block.split("\n")
            li_list = []
            for item in items:
                it = item[2:]
                li_list.append(ParentNode("li",text_to_children(it)))
            children.append(ParentNode("ul",li_list))
        if blocktype == BlockType.ORDERED_LIST:
            items = block.split("\n")
            li_list = []
            for item in items:
                itt = item.find(". ")
                it = item[itt + 2:]
                li_list.append(ParentNode("li",text_to_children(it)))
            children.append(ParentNode("ol",li_list))
        if blocktype == BlockType.CODE:
            text = block[4:-3]
            children.append(ParentNode("pre",[ParentNode("code",[text_node_to_html_node(TextNode(text,TextType.TEXT))])]))
    return ParentNode("div", children)