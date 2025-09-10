import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

# Set path to Tesseract if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_with_ocr(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page_num in range(len(doc)):
        pix = doc[page_num].get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img, lang="eng")
        full_text += text + "\n"
    doc.close()
    return full_text
def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += chunk_size - overlap
    return chunks
# Step 1: Extract text from PDF
pdf_text = extract_text_with_ocr("dummyresume.pdf")

# Step 2: Chunk the text
chunks = chunk_text(pdf_text)

# Step 3: Print the chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---\n{chunk}")
def highlight_keywords_in_pdf(pdf_path, keywords, output_path):
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        for keyword in keywords:
            text_instances = page.search_for(keyword)
            for inst in text_instances:
                page.add_highlight_annot(inst)
    doc.save(output_path)
    doc.close()
    print(f"✅ Keywords {keywords} highlighted and saved to: {output_path}")

# Step 3: Search and highlight a keyword
keywords_to_search = ["Python","data","9398092166"] # You can change this to any word
highlight_keywords_in_pdf("dummyresume.pdf", keywords_to_search, "highlighted_resume.pdf")

