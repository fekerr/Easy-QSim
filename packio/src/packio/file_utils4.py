# packio/file_utils.py (additions)
import math

def chunk_content(content: str, chunk_size: int, overlap: int) -> list[str]:
    """Splits content into fixed-size chunks with overlap."""
    if chunk_size <= 0:
        return [content] # No chunking if size is invalid

    chunks =
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunks.append(content[start:end])
        start += chunk_size - overlap
        if overlap >= chunk_size: # Prevent infinite loop if overlap is too large
             start = end # Move to next non-overlapping position

    return chunks

# --- Modify generate_output function ---
def generate_output(input_dir: str, files_to_pack: list[str], output_path: str | None, chunk_size: int = 0, chunk_overlap_ratio: float = 0.1):
    #... (output_stream setup)...
    overlap = math.floor(chunk_size * chunk_overlap_ratio) if chunk_size > 0 else 0

    #... (optional file tree)...

    full_content_buffer = io.StringIO() # Buffer to hold all content before chunking

    for relative_path in files_to_pack:
        #... (read file content into 'content' variable, handle errors)...
        header = f"--- File: {relative_path} ---\n"
        full_content_buffer.write(header)
        full_content_buffer.write(content)
        if not content.endswith('\n'):
            full_content_buffer.write("\n")
        full_content_buffer.write("\n")

    final_content = full_content_buffer.getvalue()
    full_content_buffer.close()

    if chunk_size > 0:
        content_chunks = chunk_content(final_content, chunk_size, overlap)
        logging.info(f"Splitting content into {len(content_chunks)} chunks (size={chunk_size}, overlap={overlap}).")
        for i, chunk in enumerate(content_chunks):
             # Optionally add chunk headers
             output_stream.write(f"--- Chunk {i+1}/{len(content_chunks)} ---\n")
             output_stream.write(chunk)
             output_stream.write("\n") # Separator between chunks
    else:
         # Write all content at once if not chunking
         output_stream.write(final_content)

    #... (output_stream cleanup)...

# --- Update process_directory call in main.py ---
# process_directory(..., args.chunk_size,...) # Pass chunk size arg
