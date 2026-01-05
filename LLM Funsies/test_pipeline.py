import os 
from textProcessing.rag_processor import RAGProcessor

currentProcessor = RAGProcessor("chunked_document_demo.json","all-MiniLM-L6-v2")
currentProcessor.build("textProcessing/testLecture/**/*.md")
print(currentProcessor.search("What is a stack pointer? ",2))

# #class RAGProcessor(documents: List[ChunkedDocument], index: Optional[faiss.Index]=None, embedding_model: str, chunks: List[Chunk]=field(default_factory=list), embeddings: Optional[np.ndarray]=None)