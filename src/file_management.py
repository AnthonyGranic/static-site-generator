import os
import pathlib
import shutil

from markdowntohtml import extract_title, markdown_to_html_node


def copy_static_to_public():
    if os.path.exists("./docs"):
        shutil.rmtree("./docs")

    os.mkdir("./docs")

    copy_all_files_to_dir("./static/", "./docs/")


def copy_all_files_to_dir(source_dir, target_dir):

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)
        elif os.path.isdir(source_path):
            os.makedirs(target_path, exist_ok=True)
            copy_all_files_to_dir(source_path, target_path)


def generate_page(from_path, template_path, dest_path, basepath):
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
    template_with_basepath = template_with_content.replace(
        'href="/', f'href="{basepath}'
    ).replace('src="/', f'src="{basepath}')

    dirname = os.path.dirname(dest_path)
    os.makedirs(dirname, exist_ok=True)

    with open(dest_path, "w") as dest:
        dest.write(template_with_basepath)
        dest.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        target_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_path) and source_path.endswith(".md"):

            html_target = target_path.replace("md", "html")
            generate_page(source_path, template_path, html_target, basepath)

        elif os.path.isdir(source_path):

            generate_pages_recursive(source_path, template_path, target_path, basepath)
