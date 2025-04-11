import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINK, "ad.com")
        node2 = TextNode("This is a text node", TextType.LINK, "ad.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text1 node", TextType.LINK, "ad.com")
        node2 = TextNode("This is a text node", TextType.LINK, "ad.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_when_one_has_link(self):
        node = TextNode("This is a text1 node", TextType.LINK, "ad.com")
        node2 = TextNode("This is a text1 node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_types(self):
        node = TextNode("This is a text node", TextType.IMAGE, "ad.com")
        node2 = TextNode("This is a text node", TextType.LINK, "ad.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold node</b>")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(
            html_node.to_html(), '<a href="google.com">This is a link node</a>'
        )

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.to_html(),
            '<img href="google.com" alt="This is an image node"></img>',
        )


if __name__ == "__main__":
    unittest.main()
