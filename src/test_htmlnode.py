import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode,ParentNode

class TestHTMLNode(unittest.TestCase):
    
    def test_default_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')
    def test_props_to_html_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None,"Hello, World!")
        self.assertEqual(node.to_html(),"Hello, World!")
        
if __name__ == "__main__":
    unittest.main()
    
    
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_missing_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "x")])
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_to_html_no_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
            
    def test_to_html_incomplete_child(self):
        parent_node = ParentNode("div", [LeafNode("b", "hi"), LeafNode(None, " there")])
        self.assertEqual(parent_node.to_html(), "<div><b>hi</b> there</div>")
        