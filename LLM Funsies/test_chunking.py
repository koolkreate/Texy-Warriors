# toy_chunking.py

import os
from language_agent.chunker import ChunkedDocument

def main():
    """
    Demonstrates chunking, embedding, saving, loading, and retrieval.
    """
    print("--- Toy Chunking and Retrieval Demo ---")

    # --- 1. Setup ---
    # Ensure the json_files directory exists for saving
    output_dir = "json_files"
    os.makedirs(output_dir, exist_ok=True)

    # Path to the IPIP questions file (or any text file you want to use)
    # Make sure this file exists in your project directory
    source_file_path = "CSP.txt" 

    if not os.path.exists(source_file_path):
        print(f"Error: Source file '{source_file_path}' not found. Please ensure it exists.")
        # Optionally, create a small sample file for testing
        sample_text = "This is a sample document.\nIt has multiple lines.\nWe will chunk and embed it.\nChunking is useful for large texts.\nEmbeddings help find similar pieces of text."
        with open(source_file_path, 'w') as f:
            f.write(sample_text)
        print(f"Created a sample file '{source_file_path}' for demonstration.")

    # Define chunk size (in tokens)
    chunk_size_tokens = 15 # Adjust as needed

    # Define save path for the chunked document
    saved_doc_path = os.path.join(output_dir, "chunked_document_demo.json")

    # --- 2. Create and Chunk Document ---
    print(f"\n1. Loading and chunking '{source_file_path}'...")
    try:
        # Create a ChunkedDocument instance
        doc = ChunkedDocument(filepath=source_file_path, chunk_size=chunk_size_tokens)
        
        # Perform the chunking
        doc.chunk_text()
        
        if not doc.chunks:
            print("No chunks were created. Exiting.")
            return

        print(f"   Created {len(doc.chunks)} chunks.")
        print("   Sample Chunk Texts:")
        # Show first couple of chunks
        for i, chunk_text in enumerate(doc.get_chunk_text()[:2]):
            print(f"     Chunk {i+1}: {repr(chunk_text[:100])}...") # repr to show newlines etc.

    except FileNotFoundError as e:
        print(f"   Error: {e}")
        return
    except IOError as e:
        print(f"   Error reading or processing file: {e}")
        return
    except Exception as e:
        print(f"   Unexpected error during chunking: {e}")
        return

    # --- 3. Embed Chunks ---
    print("\n2. Calculating embeddings for chunks...")
    try:
        # Calculate embeddings for all chunks using Sentence Transformers
        # (This will load the model and process the text)
        doc.calculate_chunk_embeddings()
        print("   Embeddings calculated successfully.")
        
        # Verify embeddings were set
        embeddings = doc.get_embeddings()
        if embeddings and embeddings[0] is not None:
            print(f"   Sample Embedding (Chunk 1, first 5 dims): {embeddings[0][:5]}")
        else:
            print("   Warning: Embeddings list is empty or first embedding is None.")

    except Exception as e:
        print(f"   Error calculating embeddings: {e}")
        return

    # --- 4. Save Chunked Document ---
    print(f"\n3. Saving chunked document to '{saved_doc_path}'...")
    try:
        doc.save(saved_doc_path)
        print("   Document saved successfully.")
    except Exception as e:
        print(f"   Error saving document: {e}")
        # Don't return here, as we can still try retrieval with the in-memory doc

    # --- 5. Reload Chunked Document ---
    print(f"\n4. Reloading chunked document from '{saved_doc_path}'...")
    try:
        # Load the ChunkedDocument from the saved file
        reloaded_doc = ChunkedDocument.load(saved_doc_path)
        print("   Document reloaded successfully.")
        print(f"   Reloaded doc has {len(reloaded_doc.chunks)} chunks.")
        
        # Verify embeddings were loaded (they should be lists of floats or None)
        reloaded_embeddings = reloaded_doc.get_embeddings()
        if reloaded_embeddings and reloaded_embeddings[0] is not None:
             print(f"   Reloaded Embedding (Chunk 1, first 5 dims): {reloaded_embeddings[0][:5]}")
        else:
             print("   Warning: Reloaded embeddings list is empty or first embedding is None.")

    except FileNotFoundError as e:
        print(f"   Error: {e}")
        return
    except ValueError as e: # Catch errors from the load method's internal parsing
        print(f"   Error loading or parsing the saved file: {e}")
        return
    except Exception as e:
        print(f"   Unexpected error reloading document: {e}")
        return

    # --- 6. Perform Retrieval ---
    print("\n5. Performing retrieval with a query...")
    
    # Define a query (hardcoded for demo)
    # Try to make it related to the content of ipip_questions.txt or your sample text
    query_text = "What is a constraint satisfaction problem? " # Example query
    
    print(f"   Query: '{query_text}'")

    # --- Embed the Query ---
    try:
        from sentence_transformers import SentenceTransformer
        # Load the same model used for chunk embeddings
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        # Get the embedding for the query
        query_embedding = model.encode(query_text).tolist() # Convert numpy array to list
        print("   Query embedded successfully.")
    except Exception as e:
        print(f"   Error embedding query: {e}")
        return

    # --- Find the Most Similar Chunk ---
    # Use the reloaded document for retrieval to prove loading worked
    try:
        # Find the chunk most similar to the query embedding
        # find_by_embedding returns the Chunk object itself
        most_similar_chunk = reloaded_doc.find_by_embedding(query_embedding)

        if most_similar_chunk:
            print("\n--- Retrieval Result ---")
            print("Most similar chunk found:")
            print(f"  Text: {repr(most_similar_chunk.text)}")
            print(f"  Start Token: {most_similar_chunk.start_pos}")
            print(f"  End Token: {most_similar_chunk.end_pos}")
            print(f"  Number of Tokens: {most_similar_chunk.num_tokens}")
            # Note: The embedding is stored but not printed here for brevity
        else:
            print("   No similar chunk was found.")
            
    except Exception as e:
        print(f"   Error during retrieval: {e}")
        return

    print("\n--- Demo Complete ---")

if __name__ == "__main__":
    main()