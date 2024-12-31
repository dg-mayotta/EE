from config import Config

def chunk_text(text):
    """
    Split text into chunks that don't exceed GPT-4's token limit
    """
    # Approximate tokens (rough estimate: 4 chars = 1 token)
    max_chars = Config.MAX_CHUNK_SIZE * 4
    
    # If text is short enough, return as single chunk
    if len(text) <= max_chars:
        return [text]
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        # If a single paragraph is too long, split it by sentences
        if len(paragraph) > max_chars:
            sentences = paragraph.split('. ')
            for sentence in sentences:
                if current_length + len(sentence) > max_chars:
                    # Save current chunk and start new one
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [sentence]
                    current_length = len(sentence)
                else:
                    current_chunk.append(sentence)
                    current_length += len(sentence)
        else:
            if current_length + len(paragraph) > max_chars:
                # Save current chunk and start new one
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = [paragraph]
                current_length = len(paragraph)
            else:
                current_chunk.append(paragraph)
                current_length += len(paragraph)
    
    # Add the last chunk if it exists
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks
