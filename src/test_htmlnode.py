from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, TextType
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")
    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://www.google.com"')
    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
            "class": "link-button",
            "id": "main-link"
        })
        result = node.props_to_html()
        self.assertEqual(
            result,
            ' href="https://www.google.com" target="_blank" class="link-button" id="main-link"'
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_node_no_tag(self):
        node = LeafNode(value="Just some simple text")
        self.assertEqual(node.to_html(), "Just some simple text")
    def test_leaf_node_with_tag(self):
        node = LeafNode("p", "text with tag")
        self.assertEqual(node.to_html(), "<p>text with tag</p>")
    def test_leaf_node_with_props(self):
        node = LeafNode("a", "text with prop", {"target": "_blank"})
        self.assertEqual(node.to_html(), '<a target="_blank">text with prop</a>')
    def test_leaf_node_none_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(value=None)
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_one_child(self):
        child = LeafNode("b", "Bold text")
        node = ParentNode("p", [child])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b></p>")
    def test_more_children(self):
        child1 = LeafNode("b", "thing1")
        child2 = LeafNode("b", "thing2")
        node = ParentNode("p", [child1, child2])
        self.assertEqual(node.to_html(), "<p><b>thing1</b><b>thing2</b></p>")
    def test_with_another_parent(self):
        inner_child1 = LeafNode("b", "bold text")
        inner_child2 = LeafNode("i", "italic text")
        inner_parent = ParentNode("div", [inner_child1, inner_child2])
        outer_node = ParentNode("p", [inner_parent])
        self.assertEqual(outer_node.to_html(), "<p><div><b>bold text</b><i>italic text</i></div></p>")
    def test_with_both(self):
        inner_child1 = LeafNode("b", "bold text")
        inner_child2 = LeafNode("i", "italic text")
        inner_parent = ParentNode("div", [inner_child1, inner_child2])
        outer_child = LeafNode("b", "more bold text")
        big_node = ParentNode("p", [inner_parent, outer_child])
        self.assertEqual(big_node.to_html(),
            "<p><div><b>bold text</b><i>italic text</i></div><b>more bold text</b></p>"
        )
    def test_parent_node_tag_none(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=[LeafNode("b", "some text")])
            node.to_html()
    def test_parent_node_children_none(self):
        with self.assertRaises(ValueError):
            node = ParentNode(tag="p", children=None)
            node.to_html()



if __name__ == "__main__":
    unittest.main()
