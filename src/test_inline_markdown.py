import unittest
from inline_markdown import *
from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_node_no_delimeter(self):
        node = TextNode("just plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result,[TextNode("just plain text", TextType.TEXT)])
    def test_node_delimeter_middle(self):
        node = TextNode("just **plain** text", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertEqual(result,[
    TextNode("just ", TextType.TEXT),
    TextNode("plain", TextType.BOLD),
    TextNode(" text", TextType.TEXT),
    ])
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [boots](https://www.boot.dev)"
        )
        self.assertListEqual ([("boots", "https://www.boot.dev")],matches)
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_links(self):
        node = TextNode("plain text with link [anchor text](https://www.example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
            TextNode("plain text with link ", TextType.TEXT),
            TextNode("anchor text", TextType.LINK, "https://www.example.com")
            ], new_nodes
        )
        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_one_block(self):
        md = "hello"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["hello"],
        )