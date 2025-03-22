import sys
import os
import shutil
from textnode import TextNode, TextType
from generate import generate_page, generate_pages_recursive


def copy_static(source_dir, target_dir):
    """
    Recursively copy files from source_dir to target_dir
    """
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    os.mkdir(target_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, target_path)
            print(f"Copied file: {source_path} to {target_path}")
        else:
            os.mkdir(target_path)
            copy_static(source_path, target_path)
            print(f"Copied directory: {source_path} to {target_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "docs")
    content_dir = os.path.join(script_dir, "content")
    template_path = os.path.join(script_dir, "template.html")

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_static(static_dir, public_dir)

    generate_pages_recursive(
        content_dir,
        template_path,
        public_dir,
        basepath
    )

if __name__ == "__main__":
    main()
