# Inside generate_output loop
try:
    with open(full_path, "r", encoding="utf-8", errors="strict") as infile: # Use 'strict' initially
        content = infile.read()
        #... write content...
except UnicodeDecodeError:
    logging.warning(f"Encoding error in {relative_path}. Trying latin-1.")
    try:
        # Try a fallback encoding
        with open(full_path, "r", encoding="latin-1") as infile:
             content = infile.read()
             #... write content...
    except Exception as e:
         logging.error(f"Could not read {relative_path} even with fallback: {e}")
         # Skip the file or handle error differently
except Exception as e:
    logging.warning(f"Skipping file {relative_path} due to error: {e}")
