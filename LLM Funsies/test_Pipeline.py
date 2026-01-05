import os 
from textProcessing.rag_processor import RAGProcessor
from textProcessing.pdfParsing import pdfParser

#Right the entire pipeline is sorted! So we can:
test_FileName = ""#Input the lecture slide file name you want here!
parser = pdfParser(test_FileName + ".pdf")
markdown_output = parser.parse_pdf() # Saves the pdf as a markdown file in testLecture/
parser.generate_captions_parallel(context = "Assembly Language; a Computer Systems lecture.") #Generates captions for the images in the pdf
parser.add_explanation() # Adds explanation to the markdown file
currentProcessor = RAGProcessor("","all-MiniLM-L6-v2")
currentProcessor.build("textProcessing/testLecture/**/*.md")
print(currentProcessor.search("What is a stack pointer? ",2))

# #class RAGProcessor(documents: List[ChunkedDocument], index: Optional[faiss.Index]=None, embedding_model: str, chunks: List[Chunk]=field(default_factory=list), embeddings: Optional[np.ndarray]=None)