import unittest
from textnode import text_node_to_html_node

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_types(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_texts(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_urls(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.butwitha.url")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "https://www.boot.dev")

    def test_image(self):
        node = TextNode("", TextType.IMAGE, "https://www.boot.dev.some_image", "some alt text")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.boot.dev.some_image")
        self.assertEqual(html_node.props["alt"], "some alt text")

    def test_invalid_text_type(self):
        node = TextNode("Some text", "invalid_type")
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(node)

    def test_link_empty_url(self):
        node = TextNode("Empty link", TextType.LINK, "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["href"], "")

    def test_image_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "https://image.url", "")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props["alt"], "")



if __name__ == "__main__":
    unittest.main()
