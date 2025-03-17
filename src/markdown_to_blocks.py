def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block:
            cleaned_blocks.append(stripped_block)
    return cleaned_blocks
