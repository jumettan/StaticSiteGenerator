from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    results = []
    for item in old_nodes:
        if item.text_type == TextType.TEXT:
            node_splitted = item.text.split(delimiter)
            if len(node_splitted) % 2 == 1:
                for i,piece in enumerate(node_splitted):
                    if piece =="":
                        continue
                    elif i %2 == 0:
                        results.append(TextNode(piece,TextType.TEXT))
                    else: 
                        results.append(TextNode(piece, text_type))
            else:
                raise Exception("delimeter not valid divider")
        else:
            results.append(item)
    return results

def extract_markdown_images(markdown):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)
def extract_markdown_links(markdown):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", markdown)



def split_nodes_image(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        splitted = extract_markdown_images(node.text)
        if splitted ==[]:
            results.append(node)
            continue
        remaining_text = node.text
        for image in splitted:
            sections = remaining_text.split(f"![{image[0]}]({image[1]})",1)
            if sections[0] != "":
                results.append(TextNode(sections[0], TextType.TEXT))
            results.append(TextNode(image[0],TextType.IMAGE,image[1]))
            remaining_text = sections[1]
        if remaining_text != "":
            results.append(TextNode(remaining_text, TextType.TEXT))
    return results
        
def split_nodes_link(old_nodes):
    results = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            results.append(node)
            continue
        node_splitted = extract_markdown_links(node.text)
        if node_splitted ==[]:
            results.append(node)
            continue
        
        remaining_text = node.text
        
        for link in node_splitted:
            sections = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0] != "":
                results.append(TextNode(sections[0], TextType.TEXT))  # TEXT node inside the if
            results.append(TextNode(link[0], TextType.LINK, link[1]))  # LINK node OUTSIDE the if
            remaining_text = sections[1]
        if remaining_text != "":
            results.append(TextNode(remaining_text, TextType.TEXT))
                
    return results

def text_to_textnodes(text):
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        string = block.strip()
        if string  != "":
            result.append(string)
    return result
    