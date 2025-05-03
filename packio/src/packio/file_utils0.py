# packio/file_utils.py (simplified)
import os
import fnmatch
import logging

def list_files_recursive(directory: str) -> list[str]:
    """Recursively lists all files in a directory."""
    all_files =
    for root, _, files in os.walk(directory):
        for filename in files:
            full_path = os.path.join(root, filename)
            # Store relative path from the input directory
            relative_path = os.path.relpath(full_path, directory)
            all_files.append(relative_path)
    logging.info(f"Found {len(all_files)} files via os.walk.")
    return all_files

# --- In process_directory function ---
# if is_git_repository(input_dir):
#     try:
#         candidate_files = get_git_tracked_files(input_dir)
#     except Exception:
#         logging.warning("Git command failed, falling back to recursive walk.")
#         candidate_files = list_files_recursive(input_dir)
# else:
#     candidate_files = list_files_recursive(input_dir)
