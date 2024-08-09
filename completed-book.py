import io
import tempfile
import fitz  # PyMuPDF
from deep_translator import GoogleTranslator
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image
import streamlit as st
import os

def translate_text(text, target_language):
    translator = GoogleTranslator(source='auto', target=target_language)
    try:
        return translator.translate(text)
    except Exception as e:
        st.error(f"Error during translation: {e}")
        return ""

def split_text(text, max_chunk_size):
    chunks = []
    while len(text) > max_chunk_size:
        split_point = text.rfind(' ', 0, max_chunk_size)
        if split_point == -1:
            split_point = max_chunk_size
        chunks.append(text[:split_point])
        text = text[split_point:].strip()
    chunks.append(text)
    return chunks
def translate_large_text(text, target_language, max_chunk_size=4000):
    chunks = split_text(text, max_chunk_size)
    translated_chunks = []

    for chunk in chunks:
        if 0 < len(chunk) <= max_chunk_size:
            translated_chunk = translate_text(chunk, target_language)
            if translated_chunk is not None:  # Check if translation is not None
                translated_chunks.append(translated_chunk)
            else:
                st.warning(f"Translation returned None for chunk of length {len(chunk)}")
        else:
            st.warning(f"Skipped chunk of length {len(chunk)} due to invalid length.")

    # Join chunks and handle empty list case
    return ''.join(translated_chunks) if translated_chunks else ""


def extract_text_and_images_from_pdf(pdf_file):
    text_blocks = []
    images = []
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text blocks
        for block in page.get_text("blocks"):
            text_blocks.append({
                'text': block[4],  # Extracted text
                'rect': block[:4], # Position: x0, y0, x1, y1
                'page_num': page_num
            })
        
        # Extract images
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append({
                'image': io.BytesIO(image_bytes),
                'rect': img[1]  # Bounding box for the image
            })
    
    return text_blocks, images

def create_pdf_with_layout_and_translations(text_blocks, images, translated_text_blocks, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Map of page number to their text blocks and images
    page_text_blocks = {}
    page_images = {}

    for block in text_blocks:
        page = block['page_num']
        if page not in page_text_blocks:
            page_text_blocks[page] = []
        page_text_blocks[page].append(block)
    
    for img in images:
        page = img['rect'][1] // height
        if page not in page_images:
            page_images[page] = []
        page_images[page].append(img)

    # Create PDF pages
    for page_num, blocks in page_text_blocks.items():
        c.showPage()
        c.setPageSize(letter)
        # Draw images for the current page
        if page_num in page_images:
            for img in page_images[page_num]:
                img_path = tempfile.mktemp(suffix=".png")
                with open(img_path, 'wb') as f:
                    f.write(img['image'].read())
                c.drawImage(img_path, img['rect'][0], img['rect'][1], img['rect'][2] - img['rect'][0], img['rect'][3] - img['rect'][1])
                os.remove(img_path)
        
        # Draw translated text blocks for the current page
        if page_num in translated_text_blocks:
            for block in translated_text_blocks[page_num]:
                c.setFont("Helvetica", 12)
                c.drawString(block['rect'][0], height - block['rect'][1], block['text'])

    c.save()

def main():
    st.title("PDF Translator with Layout Preservation")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Input languages
    source_language = st.text_input("Enter source language code (e.g., 'en' for English)")
    target_language = st.text_input("Enter target language code (e.g., 'fr' for French)")

    if uploaded_file and source_language and target_language:
        st.write("Extracting text and images from the PDF...")
        text_blocks, images = extract_text_and_images_from_pdf(uploaded_file)

        if text_blocks:
            st.write("Translating text...")
            translated_text_blocks = []
            for block in text_blocks:
                translated_text = translate_large_text(block['text'], target_language, max_chunk_size=4000)
                translated_text_blocks.append({
                    'text': translated_text,
                    'rect': block['rect'],
                    'page_num': block['page_num']
                })
            
            # Create a new PDF with the translated text and original images
            output_pdf_path = tempfile.mktemp(suffix=".pdf")
            create_pdf_with_layout_and_translations(text_blocks, images, translated_text_blocks, output_pdf_path)
            
            # Provide a download link for the PDF
            with open(output_pdf_path, "rb") as file:
                st.download_button(
                    label="Download Translated PDF",
                    data=file,
                    file_name="translated_text.pdf",
                    mime="application/pdf"
                )
            
            # Clean up the temporary file
            os.remove(output_pdf_path)
        else:
            st.error("No text found in the PDF.")
    elif uploaded_file is None:
        st.warning("Please upload a PDF file.")
    elif not source_language:
        st.warning("Please enter the source language code.")
    elif not target_language:
        st.warning("Please enter the target language code.")

if __name__ == "__main__":
    main()

