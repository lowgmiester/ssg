import os
from xtr_markdown import extract_title
from block_type import markdown_to_html_node

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    with open(template_path, 'r') as file:
        template_content = file.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    try:
        entries = os.listdir(dir_path_content)
    except OSError as e:
        print(f"Error reading directory {dir_path_content}: {e}")
        return

    for entry in entries:
        entry_path = os.path.join(dir_path_content, entry)

        if os.path.isfile(entry_path):
            print(f"Finished generating: {dest_dir_path}")
            if not entry.endswith('.md'):
                continue

            rel_path = os.path.relpath(entry_path, dir_path_content)
            dest_file_path = os.path.join(dest_dir_path, rel_path)
            dest_file_path = dest_file_path.replace('.md', '.html')

            try:
                os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                generate_page(entry_path, template_path, dest_file_path, basepath)
                print(f"Finished generating: {dest_file_path}")
            except Exception as e:
                print(f"Error generating page for {entry_path}: {e}")

        else:
            rel_path = os.path.relpath(entry_path, dir_path_content)
            new_dest_dir = os.path.join(dest_dir_path, rel_path)

            try:
                generate_pages_recursive(entry_path, template_path, new_dest_dir, basepath)
            except Exception as e:
                print(f"Error processing directory {entry_path}: {e}")

