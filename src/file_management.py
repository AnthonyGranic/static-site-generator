import os
import pathlib
import shutil

from markdowntohtml import extract_title, markdown_to_html_node


def copy_static_to_public():
    if os.path.exists("./public"):
        shutil.rmtree("./public")

    os.mkdir("./public")

    copy_all_files_to_dir("./static/", "./public/")


def copy_all_files_to_dir(source_dir, target_dir, subdir=""):

    current_dir = os.path.join(source_dir, subdir)
    target_subdir = os.path.join(target_dir, subdir)

    os.makedirs(target_subdir, exist_ok=True)

    for item in os.listdir(current_dir):
        source_path = os.path.join(current_dir, item)
        target_path = os.path.join(target_subdir, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)
        elif os.path.isdir(source_path):
            copy_all_files_to_dir(source_dir, target_dir, os.path.join(subdir, item))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_text = ""
    with open(from_path, "r") as fro:
        md_text = fro.read()
        fro.close()

    template_text = ""
    with open(template_path, "r") as template:
        template_text = template.read()
        template.close()

    html_node = markdown_to_html_node(md_text)
    html_text = html_node.to_html()

    title = extract_title(md_text)

    template_with_title = template_text.replace(r"{{ Title }}", title)
    template_with_content = template_with_title.replace(r"{{ Content }}", html_text)

    dirname = os.path.dirname(dest_path)
    os.makedirs(dirname, exist_ok=True)

    with open(dest_path, "w") as dest:
        dest.write(template_with_content)
        dest.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        target_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path) and source_path.endswith(".md"):

            html_target = target_path.replace("md", "html")
            generate_page(source_path, template_path, html_target)

        elif os.path.isdir(source_path):

            generate_pages_recursive(source_path, template_path, target_path)
