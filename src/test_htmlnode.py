import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        internal_node = HTMLNode("tag", "value", None, {"asdf": "Asdf", "a": "b"})
        node = HTMLNode("tag", "value", [internal_node], {"b": "b", "c": "casdfasdf"})
        self.assertEqual(' b="b" c="casdfasdf"', node.props_to_html())

    def test_to_string(self):
        internal_node = HTMLNode("tag", "value", None, {"asdf": "Asdf", "a": "b"})
        node = HTMLNode("tag", "value", [internal_node], {"b": "b", "c": "casdfasdf"})
        self.assertEqual(
            "HTMLNode(tag, value, [HTMLNode(tag, value, None, {'asdf': 'Asdf', 'a': 'b'})], {'b': 'b', 'c': 'casdfasdf'})",
            str(node),
        )

    def test_to_string(self):
        node = HTMLNode()
        self.assertEqual("HTMLNode(None, None, None, None)", str(node))


if __name__ == "__main__":
    unittest.main()
