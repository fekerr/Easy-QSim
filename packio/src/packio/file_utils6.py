# packio/file_utils.py (new function)
def generate_file_tree(file_list: list[str], indent: str = "  ") -> str:
    """Generates a simple text-based file tree string."""
    tree = {}
    for path_str in sorted(file_list):
        parts = path_str.split(os.sep)
        node = tree
        for part in parts:
            node = node.setdefault(part, {})

    tree_lines =
    def build_tree_lines(node, prefix=""):
        items = sorted(node.keys())
        for i, key in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            tree_lines.append(f"{prefix}{connector}{key}")
            if node[key]: # If it's a directory (has children)
                extension = "│   " if i < len(items) - 1 else "    "
                build_tree_lines(node[key], prefix + extension)

    build_tree_lines(tree)
    return "\n".join(tree_lines)

# --- Called from generate_output ---
# if files_to_pack: # Only generate tree if there are files
#     tree_str = generate_file_tree(files_to_pack)
#     output_stream.write("--- File Tree ---\n")
#     output_stream.write(tree_str)
#     output_stream.write("\n--- End File Tree ---\n\n")
