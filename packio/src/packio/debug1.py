# Inside get_git_tracked_files
try:
    result = subprocess.run(...) # As before
    logging.debug(f"git ls-files stdout:\n{result.stdout[:500]}...") # Log partial output
except subprocess.CalledProcessError as e:
    logging.error(f"Git command failed with exit code {e.returncode}")
    logging.error(f"Git stderr:\n{e.stderr}") # Crucial for diagnosing git errors
    raise
