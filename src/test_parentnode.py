import unittest

from parentnode import ParentNode
from leafnode import LeafNode


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

    def test_to_html_with_grandchildren2(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = ParentNode("asdf", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span><asdf><b>grandchild</b><b>grandchild</b></asdf></div>",
        )


if __name__ == "__main__":
    unittest.main()
