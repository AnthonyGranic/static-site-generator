from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("tag required")
        if self.children == None:
            raise ValueError("children required")

        value = ""
        for child in self.children:
            value += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{value}</{self.tag}>"
