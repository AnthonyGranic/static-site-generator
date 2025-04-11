import unittest
from blocktype import BlockType, block_to_block_type


class TestBlockDetection(unittest.TestCase):

    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Final Level"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("####### Too many"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"), BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```python\nprint(123)\n```"), BlockType.CODE
        )
        self.assertNotEqual(block_to_block_type("``` Missing closing"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type("> A quote\n> Another line"), BlockType.QUOTE
        )
        self.assertNotEqual(block_to_block_type("> Good\nNope"), BlockType.QUOTE)

    def test_unordered_list_block(self):
        self.assertEqual(
            block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST
        )
        self.assertNotEqual(
            block_to_block_type("- Okay\n* Not okay"), BlockType.UNORDERED_LIST
        )

    def test_ordered_list_block(self):
        self.assertEqual(
            block_to_block_type("1. One\n2. Two\n3. Three"), BlockType.ORDERED_LIST
        )
        self.assertNotEqual(
            block_to_block_type("1. Start\n3. Skipped"), BlockType.ORDERED_LIST
        )
        self.assertEqual(block_to_block_type("1. One\n2. Two"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just some random text."), BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("No list, no quote, no heading."), BlockType.PARAGRAPH
        )


if __name__ == "__main__":
    unittest.main()
