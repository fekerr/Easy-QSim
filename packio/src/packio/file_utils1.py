# packio/file_utils.py (simplified)
def apply_filters(files: list[str], include_patterns: list[str], ignore_patterns: list[str]) -> list[str]:
    """Applies include and ignore glob patterns to a list of files."""
    # Note: This is a basic implementation. More robust handling might
    # convert gitignore-style patterns to glob patterns.
    filtered_files = files

    if include_patterns:
        included_set = set()
        for pattern in include_patterns:
            included_set.update(fnmatch.filter(files, pattern))
        filtered_files = list(included_set)
        logging.debug(f"Files after include patterns: {len(filtered_files)}")

    if ignore_patterns:
        ignored_set = set()
        for pattern in ignore_patterns:
            ignored_set.update(fnmatch.filter(filtered_files, pattern))
        filtered_files = [f for f in filtered_files if f not in ignored_set]
        logging.debug(f"Files after ignore patterns: {len(filtered_files)}")

    # Add logic here to parse and apply.gitignore if not using git ls-files
    # This is complex and omitted for brevity. Recommend using git ls-files.

    logging.info(f"Selected {len(filtered_files)} files after filtering.")
    return sorted(filtered_files) # Sort for consistent output
