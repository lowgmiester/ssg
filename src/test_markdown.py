import unittest
from text_splitter import *
from xtr_markdown import *
from textnode import TextNode, TextType

class MarkdownExtractorTests(unittest.TestCase):
    def test_empty_text(self):
        text = ""
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        text = "Images: ![first](https://example.com/1.jpg) and ![second](https://example.com/2.jpg)"
        expected = [("first", "https://example.com/1.jpg"), ("second", "https://example.com/2.jpg")]
        self.assertListEqual(expected, extract_markdown_images(text))

    def test_extract_no_markdown_images(self):
        text = "No images here, just [a link](https://example.com)"
        self.assertListEqual([], extract_markdown_images(text))



    def test_extract_markdown_links(self):
        text = "Check out [this link](https://example.com)"
        expected = [("this link", "https://example.com")]
        self.assertListEqual(expected, extract_markdown_links(text))

    def test_extract_multiple_markdown_links(self):
        text = "Links: [first](https://example.com) and [second](https://another.com)"
        expected = [("first", "https://example.com"), ("second", "https://another.com")]
        self.assertListEqual(expected, extract_markdown_links(text))



    def test_mixed_content(self):
        text = "This contains a ![cute cat](https://example.com/cat.jpg) image and [a link](https://example.com)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("cute cat", "https://example.com/cat.jpg")], image_matches)
        self.assertListEqual([("a link", "https://example.com")], link_matches)

    def test_special_characters(self):
        text = "Special chars in ![alt-text with (parens)](https://example.com/image?param=value&another=true) and [link text with [brackets]](https://example.com/page?q=test)"
        image_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("alt-text with (parens)", "https://example.com/image?param=value&another=true")], image_matches)
        self.assertListEqual([("link text with [brackets]", "https://example.com/page?q=test")], link_matches)


    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

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
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )



    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_simple(self):
        text = "Just plain text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, text)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)

    def test_text_to_textnodes_bold(self):
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_text_to_textnodes_complex(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[4].text_type, TextType.TEXT)
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[6].text_type, TextType.TEXT)
        self.assertEqual(nodes[7].text, "obi wan image")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[8].text_type, TextType.TEXT)
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")



    def test_extract_title_basic(self):
        markdown = "# Hello World\nThis is some content."
        expected = "Hello World"
        self.assertEqual(extract_title(markdown), expected)

    def test_extract_title_with_extra_whitespace(self):
        markdown = "#    Lots of spaces    \nContent here."
        expected = "Lots of spaces"
        self.assertEqual(extract_title(markdown), expected)

    def test_extract_title_no_title(self):
        markdown = "No title here\nJust content."
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
