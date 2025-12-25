# src/chunk_processor.py
import tiktoken

class ChunkProcessor:
    def __init__(self, max_tokens=12000):
        self.max_tokens = max_tokens
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoding.encode(text))
    
    def split_text(self, text: str, chunk_size: int = None) -> list:
        """
        Split long text into AI-processable chunks
        """
        if chunk_size is None:
            chunk_size = self.max_tokens
        
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = []
        current_size = 0
        
        for paragraph in paragraphs:
            paragraph_tokens = self.count_tokens(paragraph)
            
            if paragraph_tokens > chunk_size:
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    sentence_tokens = self.count_tokens(sentence)
                    if current_size + sentence_tokens > chunk_size:
                        if current_chunk:
                            chunks.append('\n\n'.join(current_chunk))
                            current_chunk = []
                            current_size = 0
                        if sentence_tokens > chunk_size:
                            sub_chunks = self.split_by_characters(sentence, chunk_size)
                            chunks.extend(sub_chunks)
                        else:
                            current_chunk.append(sentence)
                            current_size = sentence_tokens
                    else:
                        current_chunk.append(sentence)
                        current_size += sentence_tokens
            else:
                if current_size + paragraph_tokens > chunk_size:
                    if current_chunk:
                        chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [paragraph]
                    current_size = paragraph_tokens
                else:
                    current_chunk.append(paragraph)
                    current_size += paragraph_tokens
        
        if current_chunk:
            chunks.append('\n\n'.join(current_chunk))
        
        return chunks
    
    def split_by_characters(self, text: str, max_chars: int) -> list:
        """Split text by character count"""
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]
    
    def create_chunk_summary_prompt(self, chunk: str, chunk_index: int, total_chunks: int) -> str:
        """
        Create summary prompt for each text chunk
        """
        return f"""
This is chunk {chunk_index}/{total_chunks} from a section of "The History of the Decline and Fall of the Roman Empire".

Please extract key information from this text chunk, focusing on:
- Important historical events and figures
- Political, military, and economic changes
- Key descriptions of imperial conditions

Summarize the main content of this chunk in concise bullet points:

{chunk}
"""