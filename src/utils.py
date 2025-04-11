from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_list.extend(split_single_node(node, delimiter, text_type))
        else:
            new_list.append(node)

    return new_list


def split_single_node(node, delimiter, text_type):
    new_texts = node.text.split(delimiter)

    if len(new_texts) % 2 == 0:
        raise Exception("delimiter missing pair")

    split_nodes = []
    for i in range(len(new_texts)):
        if new_texts[i] == "":
            continue
        if i % 2 == 0:
            split_nodes.append(TextNode(new_texts[i], TextType.TEXT))
        else:
            split_nodes.append(TextNode(new_texts[i], text_type))

    return split_nodes


def extract_markdown_images(text):

    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(regex, text)

    return [(match[0], match[1]) for match in matches]


def extract_markdown_links(text):

    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

    matches = re.findall(regex, text)

    return list(map(lambda x: (x[0], x[1]), matches))


def split_nodes_image(old_nodes):

    new_list = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_list.extend(split_single_node_images(node))
        else:
            new_list.append(node)

    return new_list


def split_nodes_link(old_nodes):
    new_list = []

    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_list.extend(split_single_node_link(node))
        else:
            new_list.append(node)

    return new_list


def split_single_node_images(node):

    images = extract_markdown_images(node.text)
    if len(images) == 0:
        return [node]

    original_text = node.text
    result = []
    for image in images:
        image_alt = image[0]
        image_link = image[1]

        sections = original_text.split(f"![{image_alt}]({image_link})", 1)
        original_text = sections[1]

        if len(sections[0]) != 0:
            result.append(TextNode(sections[0], TextType.TEXT))
        result.append(TextNode(image_alt, TextType.IMAGE, image_link))

    if len(original_text) != 0:
        result.append(TextNode(original_text, TextType.TEXT))

    return result


def split_single_node_link(node):

    links = extract_markdown_links(node.text)
    if len(links) == 0:
        return [node]

    original_text = node.text
    result = []
    for link in links:
        link_alt = link[0]
        link_link = link[1]

        sections = original_text.split(f"[{link_alt}]({link_link})", 1)

        original_text = sections[1]
        if len(sections[0]) != 0:
            result.append(TextNode(sections[0], TextType.TEXT))
        result.append(TextNode(link_alt, TextType.LINK, link_link))

    if len(original_text) != 0:
        result.append(TextNode(original_text, TextType.TEXT))

    return result


def text_to_textnodes(text):
    initial_node = TextNode(text, TextType.TEXT)
    bold = split_nodes_delimiter([initial_node], "**", TextType.BOLD)
    italic = split_nodes_delimiter(bold, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italic, "`", TextType.CODE)
    link = split_nodes_link(code)
    image = split_nodes_image(link)

    return image


def markdown_to_blocks(markdown):

    blocks = markdown.split("\n\n")

    return list(filter(None, (block.strip() for block in blocks)))
