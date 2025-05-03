# packio/main.py (simplified)
import argparse
import sys
from.file_utils import process_directory # Assuming processing logic is here

def main():
    parser = argparse.ArgumentParser(
        description="Pack project files into a single context file for LLMs."
    )
    parser.add_argument(
        "input_dir",
        metavar="INPUT_DIRECTORY",
        type=str,
        help="The root directory of the project to pack.",
    )
    parser.add_argument(
        "-o",
        "--output",
        metavar="OUTPUT_FILE",
        type=str,
        default=None, # Default to stdout
        help="Path to the output file. If omitted, output goes to stdout.",
    )
    parser.add_argument(
        "--include",
        action="append", # Allows multiple --include flags
        default=,
        metavar="PATTERN",
        help="Glob pattern for files/directories to explicitly include.",
    )
    parser.add_argument(
        "--ignore",
        action="append", # Allows multiple --ignore flags
        default=,
        metavar="PATTERN",
        help="Glob pattern for files/directories to exclude (overrides includes).",
    )
    # Add arguments for chunking, token counting, verbosity etc.
    # parser.add_argument("--chunk-size", type=int, default=0, help="...")
    # parser.add_argument("-v", "--verbose", action="store_true", help="...")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    try:
        # Basic logging setup (can be more sophisticated)
        # if args.verbose: logging.basicConfig(level=logging.DEBUG)
        # else: logging.basicConfig(level=logging.INFO)

        process_directory(
            args.input_dir,
            args.output,
            args.include,
            args.ignore,
            # Pass other args like chunk_size, etc.
        )
    except Exception as e:
        # logging.error(f"An error occurred: {e}", exc_info=True) # More detailed logging
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
