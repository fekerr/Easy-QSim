# packio/file_utils.py (simplified)
import sys
import io

def generate_output(input_dir: str, files_to_pack: list[str], output_path: str | None):
    """Reads files and writes formatted content to output."""
    output_stream = None
    try:
        if output_path:
            # Ensure the output directory exists if specified
            output_dir = os.path.dirname(output_path)
            if output_dir:
                 os.makedirs(output_dir, exist_ok=True)
            output_stream = open(output_path, "w", encoding="utf-8")
            logging.info(f"Writing output to file: {output_path}")
        else:
            output_stream = sys.stdout
            logging.info("Writing output to stdout.")

        # --- Optional: Add File Tree Prefix ---
        # tree_str = generate_file_tree(files_to_pack) # Implement this function
        # output_stream.write("--- File Tree ---\n")
        # output_stream.write(tree_str)
        # output_stream.write("\n--- End File Tree ---\n\n")

        for relative_path in files_to_pack:
            full_path = os.path.join(input_dir, relative_path)
            header = f"--- File: {relative_path} ---\n" # Output format [9, 19]
            output_stream.write(header)
            try:
                with open(full_path, "r", encoding="utf-8", errors="replace") as infile:
                    # Read and write content (potentially in chunks for large files)
                    content = infile.read()
                    output_stream.write(content)
                    # Ensure newline after content, even if file doesn't end with one
                    if not content.endswith('\n'):
                        output_stream.write("\n")
                    output_stream.write("\n") # Add extra newline for separation
            except FileNotFoundError:
                logging.warning(f"Skipping file not found: {relative_path}")
            except PermissionError:
                logging.warning(f"Skipping file due to permission error: {relative_path}")
            except UnicodeDecodeError:
                logging.warning(f"Skipping file due to encoding error (not UTF-8?): {relative_path}")
            except Exception as e:
                logging.warning(f"Skipping file {relative_path} due to error: {e}")

    finally:
        if output_stream and output_path: # Close file only if it was opened
            output_stream.close()
            logging.info(f"Finished writing to {output_path}")

# --- Main processing function ---
def process_directory(input_dir: str, output_path: str | None, include: list[str], ignore: list[str]):
    abs_input_dir = os.path.abspath(input_dir)
    if not os.path.isdir(abs_input_dir):
        raise ValueError(f"Input directory not found or not a directory: {input_dir}")

    candidate_files =
    if is_git_repository(abs_input_dir):
        try:
            candidate_files = get_git_tracked_files(abs_input_dir)
        except Exception as e:
            logging.warning(f"Could not get files from git: {e}. Falling back to recursive walk.")
            candidate_files = list_files_recursive(abs_input_dir)
    else:
        logging.info("Not a git repository, performing recursive file walk.")
        candidate_files = list_files_recursive(abs_input_dir)

    files_to_pack = apply_filters(candidate_files, include, ignore)

    if not files_to_pack:
        logging.warning("No files selected after filtering. Output will be empty.")

    generate_output(abs_input_dir, files_to_pack, output_path)
