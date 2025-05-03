# packio/git_utils.py (simplified)
import os
import subprocess
import logging # Use logging module

def is_git_repository(directory: str) -> bool:
    """Checks if a directory is a Git repository."""
    git_dir = os.path.join(directory, ".git")
    return os.path.exists(git_dir) and os.path.isdir(git_dir)

def get_git_tracked_files(directory: str) -> list[str]:
    """Gets a list of tracked files using 'git ls-files'."""
    if not is_git_repository(directory):
        return
    try:
        # -z: null-terminate filenames
        # -c: show cached files (staged)
        # --exclude-standard: respect.gitignore,.git/info/exclude, core.excludesFile
        # --others: include untracked files (optional, consider adding a flag)
        # Note: Running git commands requires 'git' in PATH
        result = subprocess.run(
            ["git", "ls-files", "-zc", "--exclude-standard"],
            cwd=directory,
            capture_output=True,
            text=True, # Decode stdout/stderr as text
            check=True, # Raise CalledProcessError on non-zero exit
            encoding='utf-8', # Specify encoding for text mode
            errors='ignore' # Handle potential decoding errors in output
        )
        # Split by null character and filter out empty strings
        files = [f for f in result.stdout.split('\0') if f]
        logging.info(f"Found {len(files)} tracked files via git ls-files.")
        return files
    except FileNotFoundError:
        logging.error("'git' command not found. Is Git installed and in PATH?")
        raise # Re-raise the exception
    except subprocess.CalledProcessError as e:
        logging.error(f"Git command failed: {e}")
        logging.error(f"Git stderr: {e.stderr}")
        raise # Re-raise the exception
    except Exception as e:
        logging.error(f"Error running git ls-files: {e}")
        raise
