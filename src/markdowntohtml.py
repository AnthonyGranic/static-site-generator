import os
from parentnode import ParentNode
from textnode import text_node_to_html_node
from utils import markdown_to_blocks, text_to_textnodes
from blocktype import block_to_block_type, BlockType
from leafnode import LeafNode
import re


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(create_parent_node(block_type, block))

    return ParentNode("div", children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = text_nodes_to_html_nodes(text_nodes)
    return html_nodes


def text_nodes_to_html_nodes(text_nodes):
    return list(map(lambda x: text_node_to_html_node(x), text_nodes))


def create_parent_node(block_type, block_text):
    match (block_type):
        case BlockType.PARAGRAPH:
            return create_paragraph_node(block_text)
        case BlockType.HEADING:
            return create_heading_node(block_text)
        case BlockType.CODE:
            return create_code_node(block_text)
        case BlockType.QUOTE:
            return create_quote_node(block_text)
        case BlockType.UNORDERED_LIST:
            return create_unordered_list_node(block_text)
        case BlockType.ORDERED_LIST:
            return create_ordered_list_node(block_text)
        case _:
            raise Exception("unsupported block type")


def create_ordered_list_node(block_text):
    lines = block_text.split("\n")
    strip_list_char = map(lambda x: re.sub(r"^\d+\.\s*", "", x), lines)
    list_of_nodes = [
        ParentNode("li", text_to_children(item)) for item in strip_list_char
    ]
    return ParentNode("ol", list_of_nodes)


def create_unordered_list_node(block_text):
    lines = block_text.split("\n")
    strip_list_char = map(lambda x: x.lstrip("- "), lines)
    list_of_nodes = [
        ParentNode("li", text_to_children(item)) for item in strip_list_char
    ]
    return ParentNode("ul", list_of_nodes)


def create_quote_node(block_text):
    lines = block_text.split("\n")
    strip_quote_char = map(lambda x: x.lstrip("> "), lines)
    new_text = " ".join(strip_quote_char)
    children = text_to_children(new_text)
    return ParentNode("blockquote", children)


def create_code_node(block_text):
    text = "\n".join(block_text.split("\n")[1:-1]) + "\n"
    return ParentNode("pre", [LeafNode("code", text)])


def create_paragraph_node(block_text):
    split_new_lines = block_text.split("\n")
    text = " ".join(split_new_lines)
    children = text_to_children(text)
    return ParentNode("p", children)


def create_heading_node(block_text):
    children = text_to_children(block_text)
    header_level = __get_header_level(children[0].value)
    new_children = [
        LeafNode(
            children[0].tag, children[0].value[header_level + 1 :], children[0].props
        ),
        *children[1:],
    ]
    return ParentNode(f"h{header_level}", new_children)


def __get_header_level(string):
    return len(re.match(r"^(#{1,6})\s", string).group(1))


def extract_title(markdown):

    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and __get_header_level(
            block
        ):
            return block[1:].lstrip()

    raise Exception("no title")
