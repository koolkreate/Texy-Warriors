import json
import os
from typing import List, Optional, Any, Dict
from dataclasses import dataclass, asdict, field
import numpy as np
from numpy.linalg import norm
import faiss
from textProcessing.chunker import ChunkedDocument, Chunk
import glob
from sentence_transformers import SentenceTransformer

#This code is lowkk important; what it does is chunk our files, and then create embeddings for them as vectors.
# Luckily i don't think this changes regardless of what model we choose, so no rewriting needed :)


@dataclass
class RAGProcessor:
    documents: List[ChunkedDocument]
    index: Optional[faiss.Index] = None
    embedding_model: str
    chunks: List[Chunk] = field(default_factory=list)
    embeddings: Optional[np.ndarray] = None
   

    def __post_init__(self):
        self.model = SentenceTransformer(self.embedding_model)
        print(f"Chunking complete. Created {len(self.chunks)} chunks.")

    def build(self,directory):
        chunk_texts = []
        for file in glob.iglob(directory,recursive=True):
            current_document = ChunkedDocument(file,512,os.path.basename(file))
            current_document.chunk_text()
            self.chunks.extend(current_document.get_chunks())
            chunk_texts.extend(current_document.get_chunk_text())
        #model = SentenceTransformer(self.embedding_model)
        self.embeddings = self.model.encode(chunk_texts)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])#When dealing with bigger projects, we may use IndexFlatIP instead, we may use IndexPQ or IndexIVFFlat if we have a massive dataset. L2 means euclidean distance squared.
        self.index.add(self.embeddings)# To add more info, the above IndexFlatL2 computes the distance from your vector to any other vector in the dataset; it uses ANN [so it's like KNN and therefore requires all the vectors to be in memory.]
    def search(self,query,k_nearest_neighbours):
        to_return = []
        #ideally we tokenise first to see if we need to chunk our query or not.
        # if total_tokens < 512: May not be needed for the scope of the project; but if we are doing actual RAG stuff then yea, we would chunk our query. <- Well ish, like we could just not type in essays when testing.
        query_vector = self.model.encode([query])
        distances,indices = self.index.search(query_vector,k_nearest_neighbours)
        for row in indices:
            for index in row:
                to_return.append(self.chunks[index])
        return to_return
    def save(self,path):
        faiss.write_index(self.index,f"{path}/index.faiss")

        chunk_dict = [chunk.todict() for chunk in self.chunks]
        with open("RagChunks.json","w") as file:
            file.write(json.dumps(chunk_dict))
    def load(self,path):
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open("RagChunks.json","r") as file:
            chunk_dict = json.load(file)
        for chunk in chunk_dict:
            self.chunks.append(chunk.from_dict(chunk))


#To get all the text files in a directory via glob,
# /**/*.txt 
