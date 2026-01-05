# language_agent/chunker.py
#You may be looking and be like wth is all this weird @dataclass nonesense; it's okay i'll try explain 
import json
import os
from typing import List, Optional, Any, Dict
from dataclasses import dataclass, asdict, field
import numpy as np
from numpy.linalg import norm

# --- Tokenizer and Embedding Imports ---
# Using SentenceTransformer tokenizer as a proxy for tokenization
# and SentenceTransformer for embeddings.

from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

# --- Type Alias ---
EmbeddingType = List[float]

#@dataclass, saves us from having to write def  __init__, and initialises our class with the ability to toString and compare instances.

@dataclass
class Chunk:
    """
    Represents a single chunk of text.
    """
    start_pos: int  # Start position in tokens
    end_pos: int    # End position in tokens (exclusive)
    num_tokens: int # Number of tokens in the chunk
    text: str       # The text content of the chunk
    embedding: Optional[EmbeddingType] = field(default=None) # Embedding, set later

    def set_embedding(self, embedding: EmbeddingType):
        """Sets the embedding for the chunk."""
        # Ensure it's a list of floats for consistency
        if embedding is not None:
            self.embedding = [float(x) for x in embedding]
        else:
            self.embedding = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Chunk to a dictionary for serialization."""
        return asdict(self)

    @classmethod #This is a class method, it means it can be called on the class itself, not an instance of the class.
    # So in english, it means that if we have a chunk, it will apply to the entire Class; so all chunks
    def from_dict(cls, data: Dict[str, Any]) -> 'Chunk':
        """
        Creates a Chunk instance from a dictionary.
        Ensures embedding is a list of floats or None.
        """
        embedding_data = data.get('embedding')
        if embedding_data is not None:
            # Ensure it's a list of floats for JSON compatibility and consistency
            data['embedding'] = [float(x) for x in embedding_data]
        # Use .get() with defaults for robustness if keys are missing
        return cls(
            start_pos=data.get('start_pos', 0),
            end_pos=data.get('end_pos', 0),
            num_tokens=data.get('num_tokens', 0),
            text=data.get('text', ''),
            embedding=data.get('embedding') # Will be list or None
        )


@dataclass
class ChunkedDocument:
    """
    Represents a full document that has been split into chunks.
    """
    filepath: str
    chunk_size: int
    filename: str = field(init=False) # Derived from filepath
    chunks: List[Chunk] = field(default_factory=list) # Initialize as empty list
    # _document_text is not stored as a field to avoid serializing large text
    # It will be loaded from filepath when needed

    def __post_init__(self):
        """Initialize derived fields after the main __init__."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Source file not found: {self.filepath}")
        self.filename = os.path.basename(self.filepath)

    def chunk_text(self):
        """
        Runs the chunking process and creates the chunks based on token count,
        respecting semantic boundaries (paragraphs/blocks) where possible.
        """
        print(f"Starting smart chunking for '{self.filename}' (Chunk size: {self.chunk_size} tokens)...")
        
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                document_text = f.read()
        except Exception as e:
            raise IOError(f"Error reading file {self.filepath}: {e}")

        if not document_text.strip():
            print(f"Warning: File '{self.filename}' is empty or contains only whitespace.")
            self.chunks = []
            return

        # Use the tokenizer associated with the embedding model for consistency
        tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        
        self.chunks = []
        
        # Split text into blocks based on double newlines to preserve paragraphs and visual context sections
        # We use a simple split by double newline as a proxy for semantic blocks.
        # This keeps "Visual Context" blocks (which are usually blockquotes) together 
        # as long as they don't have internal double newlines.
        blocks = document_text.split('\n\n')
        
        current_chunk_blocks = []
        current_chunk_tokens = 0
        current_doc_token_pos = 0 # Track global token position if needed (though approximate if we rejoin)

        for block in blocks:
            # Tokenize the block to get its size
            # We strip the block to avoid counting excess whitespace, but we'll rejoin with \n\n later
            block_content = block.strip()
            if not block_content:
                continue
                
            block_tokens = tokenizer.encode(block_content, add_special_tokens=False)
            num_block_tokens = len(block_tokens)
            
            # Check if adding this block would exceed the chunk size
            if current_chunk_tokens + num_block_tokens > self.chunk_size:
                # If we have accumulated blocks, finalize the current chunk
                if current_chunk_blocks:
                    self._create_and_add_chunk(current_chunk_blocks, current_doc_token_pos, tokenizer)
                    current_doc_token_pos += current_chunk_tokens
                    
                    # Reset for new chunk
                    current_chunk_blocks = []
                    current_chunk_tokens = 0
                
                # Now handle the current block
                # If the block itself is larger than chunk_size, we might need to split it
                # or just accept it as a large chunk to preserve integrity.
                # Use a soft limit: if it's massive (> 1.5x chunk size), maybe split? 
                # For now, per user request to "chunk correctly" with context, we prioritize keeping it intact.
                if num_block_tokens > self.chunk_size:
                     # Add it as a single oversize chunk for now to ensure we don't break Visual Context.
                     current_chunk_blocks.append(block_content)
                     current_chunk_tokens += num_block_tokens
                else:
                    current_chunk_blocks.append(block_content)
                    current_chunk_tokens += num_block_tokens
            else:
                # Add block to current chunk
                current_chunk_blocks.append(block_content)
                current_chunk_tokens += num_block_tokens

        # Finalize any remaining blocks
        if current_chunk_blocks:
            self._create_and_add_chunk(current_chunk_blocks, current_doc_token_pos, tokenizer)

        print(f"Chunking complete. Created {len(self.chunks)} chunks.")

    def _create_and_add_chunk(self, blocks: List[str], start_pos: int, tokenizer):
        """Helper to create a Chunk object from a list of text blocks."""
        # Join blocks with double newlines to reconstruct the text
        chunk_text = "\n\n".join(blocks)
        
        # Recalculate exact tokens for the final chunk text (including the joined newlines)
        chunk_tokens = tokenizer.encode(chunk_text, add_special_tokens=False)
        num_tokens = len(chunk_tokens)
        
        end_pos = start_pos + num_tokens
        
        chunk = Chunk(
            start_pos=start_pos,
            end_pos=end_pos,
            num_tokens=num_tokens,
            text=chunk_text
        )
        self.chunks.append(chunk)

    def get_chunk_text(self) -> List[str]:
        """
        Returns a list of the text content of all chunks in order.

        Returns:
            List[str]: List of chunk texts.
        """
        return [chunk.text for chunk in self.chunks]

    def calculate_chunk_embeddings(self):
        """
        Embeds all chunks using SentenceTransformer and stores the results.
        """
        if not self.chunks:
            print("No chunks available for embedding.")
            return

        print(f"Calculating embeddings for {len(self.chunks)} chunks...")
        try:
            # Load the SentenceTransformer model
            # Consider loading this once outside the loop if processing many documents
            model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
            
            # Get all chunk texts
            texts_to_embed = [chunk.text for chunk in self.chunks]
            
            # --- Replace with Cerebras Embedding Call if needed ---
            # Example (conceptual):
            # response = cerebras_client.embeddings.create(model="my-cerebras-embedding-model", input=texts_to_embed)
            # embedding_vectors = [data.embedding for data in response.data]
            # Again with cerebras stuff dw, we will need to talk first :)
            # --- End Replacement ---
            
            # Encode all texts in a batch for efficiency
            embedding_vectors = model.encode(texts_to_embed)
            
            # Assign embeddings back to chunks
            # model.encode returns a numpy array, so we convert to list
            for i, chunk in enumerate(self.chunks):
                chunk.set_embedding(embedding_vectors[i].tolist())
                # Progress indicator for large numbers of chunks
                if (i + 1) % 50 == 0 or i == len(self.chunks) - 1:
                    print(f"  Embedded chunk {i+1}/{len(self.chunks)}")

        except Exception as e:
            print(f"Error during embedding calculation: {e}")
            raise # Re-raise to signal failure
        print("Embedding calculation complete.")

    def get_embeddings(self) -> List[Optional[EmbeddingType]]:
        """
        Returns a list of all chunk embeddings in order.

        Returns:
            List[Optional[EmbeddingType]]: List of embeddings, None if not calculated.
        """
        return [chunk.embedding for chunk in self.chunks]

    def find_by_embedding(self, query_embedding: EmbeddingType) -> Optional[Chunk]:
        """
        Finds the most similar chunk to a given query embedding using cosine similarity.

        Args:
            query_embedding (EmbeddingType): The embedding of the query.

        Returns:
            Optional[Chunk]: The most similar chunk, or None if no chunks or embeddings.
        """
        if not self.chunks:
            print("No chunks available for search.")
            return None

        # Filter chunks that have embeddings
        embedded_chunks = [(chunk, chunk.embedding) for chunk in self.chunks if chunk.embedding is not None]

        if not embedded_chunks:
            print("No chunk embeddings calculated. Please run calculate_chunk_embeddings() first.")
            return None

        # Convert query and chunk embeddings to numpy arrays for calculation
        try:
            query_vec = np.array(query_embedding)
        except Exception as e:
            print(f"Error converting query embedding: {e}")
            return None

        best_chunk: Optional[Chunk] = None
        highest_similarity: float = -1.0 # Cosine similarity ranges from -1 to 1

        for chunk, chunk_embedding in embedded_chunks:
            try:
                chunk_vec = np.array(chunk_embedding)
                # Calculate cosine similarity
                # Cosine similarity = (A . B) / (||A|| * ||B||)
                dot_product = np.dot(query_vec, chunk_vec)
                norms = norm(query_vec) * norm(chunk_vec)
                if norms == 0:
                    similarity = 0.0 # Avoid division by zero
                else:
                    similarity = dot_product / norms

                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_chunk = chunk
            except Exception as e:
                print(f"Error calculating similarity for a chunk: {e}")
                continue # Continue searching other chunks

        if best_chunk:
            print(f"Found most similar chunk (similarity: {highest_similarity:.4f})")
        else:
            print("No similar chunk found (similarity calculation failed for all).")

        return best_chunk

    def save(self, save_path: str):
        """
        Serializes the ChunkedDocument to a JSON file.
        Note: Does not save the full document text.

        Args:
            save_path (str): Path to the file where the document will be saved.
        """
        print(f"Saving ChunkedDocument to '{save_path}'...")
        try:
            data_to_save = {
                "filepath": self.filepath,
                # filename is derived, so not strictly necessary to save, but can be helpful
                "filename": self.filename,
                "chunk_size": self.chunk_size,
                "chunks": [chunk.to_dict() for chunk in self.chunks]
            }
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            print("Save successful.")
        except Exception as e:
            print(f"Error saving ChunkedDocument: {e}")
            raise
    def get_chunks(self):
        return self.chunks

    @classmethod
    def load(cls, load_path: str) -> 'ChunkedDocument':
        """
        Deserializes a ChunkedDocument from a JSON file.

        Args:
            load_path (str): Path to the saved JSON file.

        Returns:
            ChunkedDocument: The loaded ChunkedDocument instance.
        """
        print(f"Loading ChunkedDocument from '{load_path}'...")
        if not os.path.exists(load_path):
            raise FileNotFoundError(f"Save file not found: {load_path}")

        try:
            with open(load_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Create instance using the primary constructor (dataclass __init__)
            # This will also trigger __post_init__
            doc = cls(
                filepath=data["filepath"],
                chunk_size=data["chunk_size"]
            )
            
            # Recreate Chunk objects from dictionaries
            # Use the robust from_dict method
            doc.chunks = [Chunk.from_dict(chunk_data) for chunk_data in data.get("chunks", [])]
            
            print("Load successful.")
            return doc
        except (json.JSONDecodeError, KeyError, TypeError) as e: # Catch more potential errors
            print(f"Error loading ChunkedDocument: {e}")
            raise ValueError(f"Could not load or parse the file '{load_path}': {e}") from e
        except Exception as e:
            print(f"Unexpected error loading ChunkedDocument: {e}")
            raise

    def __repr__(self) -> str:
        return f"ChunkedDocument(filepath='{self.filepath}', chunk_size={self.chunk_size}, num_chunks={len(self.chunks)})"
