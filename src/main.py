from file_management import copy_static_to_public, generate_pages_recursive
import sys


def main():
    if len(sys.argv) != 2 and len(sys.argv) != 1:
        raise Exception("usage is python3 main.py <root path>")

    basepath = sys.argv[1] if len(sys.argv) == 2 else "/"

    copy_static_to_public()
    generate_pages_recursive("./content/", "template.html", "./docs/", basepath)


if __name__ == "__main__":
    main()
