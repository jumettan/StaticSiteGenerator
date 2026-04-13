import unittest
from gencontent import *

class TestGenContent(unittest.TestCase):
    def test_extract_title_basic(self):
        md = "# Hello World"
        assert extract_title(md) == "Hello World"
    def multiple_lines(self):
        md = """Text
        #Title
        Hello"""
        assert extract_title(md) == "Title"
    def test_extract_title_strips_whitespace(self):
        md = "#    Hello World   "
        assert extract_title(md) == "Hello World"