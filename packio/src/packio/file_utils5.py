# packio/file_utils.py (additions)

# Rough estimate based on llm-context [4]
CHARS_PER_TOKEN_ESTIMATE = 3.62

def estimate_tokens(text: str) -> int:
    """Provides a rough estimate of token count based on character length."""
    if not text:
        return 0
    return math.ceil(len(text) / CHARS_PER_TOKEN_ESTIMATE)

# --- Can be called within generate_output ---
# total_estimated_tokens = estimate_tokens(final_content)
# logging.info(f"Estimated token count (approx): {total_estimated_tokens}")
# if chunk_size > 0:
#     for i, chunk in enumerate(content_chunks):
#         chunk_tokens = estimate_tokens(chunk)
#         logging.debug(f"Chunk {i+1} estimated tokens: {chunk_tokens}")
