from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(markdown):

    if is_valid_heading(markdown):
        return BlockType.HEADING
    if is_valid_code_block(markdown):
        return BlockType.CODE
    if is_valid_quote_block(markdown):
        return BlockType.QUOTE
    if is_valid_unordered_list_block(markdown):
        return BlockType.UNORDERED_LIST
    if is_valid_ordered_list_block(markdown):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def is_valid_heading(s):
    return bool(re.match(r"^(#{1,6})\s.+", s))


def is_valid_ordered_list_block(s):
    lines = [line.strip() for line in s.strip().splitlines() if line.strip()]
    for i, line in enumerate(lines, start=1):
        if not re.match(rf"^{i}\.\s*", line):
            return False
    return True


def is_valid_unordered_list_block(s):
    lines = s.splitlines()
    return all(line.strip().startswith("- ") for line in lines if line.strip())


def is_valid_quote_block(s):
    lines = s.splitlines()
    return all(line.strip().startswith(">") for line in lines if line.strip())


def is_valid_code_block(s):
    lines = s.splitlines()
    if len(lines) < 2:
        return False
    return lines[0].startswith("```") and lines[-1].strip() == "```"
