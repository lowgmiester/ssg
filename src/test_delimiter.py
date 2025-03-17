import unittest
from textnode import TextNode, TextType
from text_splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from xtr_markdown import *

class TestDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_mult_delims(self):
        node = TextNode("This has **bold** and another **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 5
        assert new_nodes[0].text == "This has "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "bold"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " and another "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "bold"
        assert new_nodes[3].text_type == TextType.BOLD
        assert new_nodes[4].text == " text"
        assert new_nodes[4].text_type == TextType.TEXT

    def test_two_different_delims(self):
        node = TextNode("This has **bold** and _italic_ text", TextType.TEXT)
        nodes_after_bold = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)
        assert len(new_nodes) == 5
        assert new_nodes[0].text == "This has "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "bold"
        assert new_nodes[1].text_type == TextType.BOLD
        assert new_nodes[2].text == " and "
        assert new_nodes[2].text_type == TextType.TEXT
        assert new_nodes[3].text == "italic"
        assert new_nodes[3].text_type == TextType.ITALIC
        assert new_nodes[4].text == " text"
        assert new_nodes[4].text_type == TextType.TEXT

    def test_no_delims(self):
        node = TextNode("Just some text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Just some text"
        assert new_nodes[0].text_type == TextType.TEXT

    def test_non_text(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 1
        assert new_nodes[0].text == "Already bold"
        assert new_nodes[0].text_type == TextType.BOLD

    def test_empty_text(self):
        node = TextNode("This is __ probably a mistake", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == ""
        assert new_nodes[1].text_type == TextType.ITALIC
        assert new_nodes[2].text == " probably a mistake"
        assert new_nodes[2].text_type == TextType.TEXT

    def test_unpaired_delimiter(self):
        node = TextNode("This has an unclosed _delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "_", TextType.ITALIC)



if __name__ == "__main__":
    unittest.main()
