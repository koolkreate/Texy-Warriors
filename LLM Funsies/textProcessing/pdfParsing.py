#So what i need to do is;
#Parse a pdf, then chunk the text
#As per our meeting, pymupdf will be used,
import os
import re
import requests
import base64
import pymupdf.layout
import pymupdf4llm
import cv2
import concurrent.futures
from chunker import ChunkedDocument
import pymupdf # In the future, we may need to change this; as it's not free for commercial use
import json
# the two ways are .get_textpage_ocr, and get_text
#We need to account for; maths formula, images, tables, and other special characters
#right
#Currently optimising this 
from typing import List, Optional
from pydantic import BaseModel, Field

class ImageAnalysis(BaseModel):
    category: str = Field(..., description="Technical category (e.g., 'Constraint Graph', 'Grid', 'Algebraic Equation').")
    core_concept: str = Field(..., description="The main concept visualized (e.g., 'Sudoku as CSP', 'Domain size calculation').")
    structural_elements: List[str] = Field(..., description="Specific entities (e.g., 'Node WA', 'Variable X1', 'Grid 9x9').")
    relationships_logic: str = Field(..., description="How elements interact or constraints apply.")
    math_formula_present: bool = Field(
        False, 
        description="True if the image contains LaTeX, formal equations, or complex mathematical notation."
    )
    latex_transcription: Optional[str] = Field(
        None, 
        description="A best-effort transcription of math formulas if present. Use standard LaTeX format."
    )
    pedagogical_value: str = Field(..., description="Why this visual is in the lecture.")

class pdfParser:
    def __init__(self, file):
        self.file_path = file
        self.doc_ending = os.path.splitext(os.path.basename(file))[0]
        self.img_dir = f"images/{self.doc_ending}"
        self.currentText = ""
    
    def parse_pdf(self):
        print(f"Opening file: {self.file_path}")
        os.makedirs(self.img_dir, exist_ok=True)
        self.currentText = pymupdf4llm.to_markdown(
            self.file_path, 
            write_images=True, 
            image_path=self.img_dir
        )

        self.currentText = re.sub(r'!\[\]\((.*?)\)', self.replacer, self.currentText)
        
        print("Parsed and Saved")
        with open(f"testLecture/{self.doc_ending}.md", "w", encoding="utf-8") as f:
            f.write(self.currentText)
        
        return self.currentText

    def replacer(self, match):
        original_path = match.group(1)
        basename = os.path.basename(original_path)
        dirname = os.path.dirname(original_path)
        
        m_file = re.search(r'-(\d+)-(\d+)\.(png|jpg|jpeg)$', basename)
        if m_file:
            page_num = int(m_file.group(1))
            img_idx = int(m_file.group(2))
            ext = m_file.group(3)
            
            new_name = f"Slide_{page_num}_Image_{img_idx}.{ext}"
            new_path = os.path.join(dirname, new_name)
            
            old_full_path = os.path.join(dirname, basename)
            if os.path.exists(old_full_path):
                os.rename(old_full_path, new_path)
                return f"![]({new_path})"
        
        return match.group(0)

    def process_image_single(self, filename, api_key, processed_cache, context): #Note; we can do this without the api and that's what we will actually do - this is a job that also our gemini api could do, but we want to avoid spamming gemini with requests.
        api_url = "https://api.moondream.ai/v1/query" 
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        img_path = os.path.join(self.img_dir, filename)
        current_image = cv2.imread(img_path)
        if current_image is None: return None
        
        height, width, _ = current_image.shape
        if height < 100 or width < 100:
            return None


        image_hash = hash(current_image.tobytes()) 

        if image_hash in processed_cache:
            return image_hash, processed_cache[image_hash]

        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        payload = {
            "image_url": f"data:image/png;base64,{encoded_string}",
            "question": f"Analyze this image, review the context: {context} and respond with a valid JSON object strictly adhering to this schema: \n{ImageAnalysis.model_json_schema()}\nDo not include markdown formatting like ```json.",
            "stream": False,
            "settings": {"reasoning": True}
        }

        response = requests.post(api_url, headers=headers, json=payload)
        if response.status_code == 200:
            answer = response.json().get("answer", "")
            with open(f"{os.path.splitext(img_path)[0]}.json", "w") as f:
                f.write(answer)
            print(f"V3 Analyzed: {filename}")
            return image_hash, answer
        return None

    def generate_captions_parallel(self, context):
        api_key_path = "apiKey/captionApi.txt"
        with open(api_key_path, "r") as f:
            api_key = f.read().strip()
        
        processedImages = {} 
        
        # Identify valid files first
        tasks = [f for f in os.listdir(self.img_dir) if f.startswith("Slide_")]
        
        print(f"Starting Parallel Processing for {len(tasks)} images...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            operations = []
            for fileProcessing in tasks:
                toExecute = executor.submit(self.process_image_single, fileProcessing, api_key, processedImages, context)
                operations.append(toExecute)
            for future in concurrent.futures.as_completed(operations):
                try:
                    result = future.result()
                    if result:
                        img_hash, answer = result
                        processedImages[img_hash] = answer
                except Exception as exc:
                    print(f"A task generated an exception: {exc}")

    def find_explanation(self, match):# A function which iterates through the md file and adds the explanation to the markdown. 
        image_path = match.group(1)
        dirname = os.path.dirname(image_path)
        basename = os.path.basename(image_path)
        
        # Extract slide and image numbers from the basename
        match_name = re.match(r'Slide_(\d+)_Image_(\d+)\.(png|jpg|jpeg)', basename)
        if not match_name:
            return match.group(0)
        
        page_num = int(match_name.group(1))
        img_idx = int(match_name.group(2))
        ext = match_name.group(3)
        
        # Build the JSON path based on the canonical naming format
        json_path = os.path.join(dirname, f"Slide_{page_num}_Image_{img_idx}.json")
        
        if not os.path.exists(json_path):
            return match.group(0)
        
        # Load and format the JSON data
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                info = data.get("properties", data)
                
                # Build explanation lines
                field_mapping = {
                    "category": "Category",
                    "core_concept": "Core Concept",
                    "structural_elements": "Structural Elements",
                    "relationships_logic": "Logic",
                    "pedagogical_value": "Pedagogical Value"
                }
                
                lines = []
                for key, label in field_mapping.items():
                    if key in info:
                        value = info[key]
                        if isinstance(value, list):
                            value = ", ".join(str(e) for e in value)
                        lines.append(f"**{label}:** {value}")
                
                # Format as blockquote
                canonical_image_path = os.path.join(dirname, f"Slide_{page_num}_Image_{img_idx}.{ext}")
                filename = os.path.basename(canonical_image_path)
                formatted_block = f"\n> **[Visual Context: {filename}]**\n"
                formatted_block += "\n".join(f"> {line}" for line in lines) + "\n"
                
                return f"![]({canonical_image_path})\n{formatted_block}"
                
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error processing {json_path}: {e}")
            return match.group(0)

    def add_explanation(self):
        # Ensure we have the text loaded if it's empty
        if not self.currentText:
            if os.path.exists(f"{self.doc_ending}.md"):
                with open(f"{self.doc_ending}.md", "r", encoding="utf-8") as f:
                    self.currentText = f.read()
            else:
                print(f"File {self.doc_ending}.md not found.")
                return


        self.currentText = re.sub(r'!\[\]\((.*?)\)(?!\n> \*\*\[Visual Context)', self.find_explanation, self.currentText)
        
        print("Explanations injected. Saving file...")
        with open(f"{self.doc_ending}.md", "w", encoding="utf-8") as f:
            f.write(self.currentText)
                        #print(answer)
                # print(basename)
                # print(dirname)
                # old_full_path = os.path.join(dirname, basename)
                # if os.path.exists(filePath):
                # print(modelFile.group(3))
                
            
            #print(modelFile.group(0))
            

        
        


# url = "https://api.moondream.ai/v1/query" #MoonDream AI API; so this will be used to provide a caption describing what an image has.


# Usage
parser = pdfParser("assembler.pdf")
markdown_output = parser.parse_pdf()
parser.generate_captions_parallel(context = "Assembly Language; a Computer Systems lecture.")
parser.add_explanation()
# # 2. Define your Headers (Authorization, etc.)
# headers = {
#     "Authorization":  f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# # 3. Define your Data (the payload)


# # 4. Make the request
# #  soms was here teeheeee

# parse_pdf("CSP.pdf")
