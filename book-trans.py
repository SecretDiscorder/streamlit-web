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
            translated_chunks.append(translated_chunk)
        else:
            st.warning(f"Skipped chunk of length {len(chunk)} due to invalid length.")
    return ''.join(translated_chunks)

def extract_images_from_pdf(pdf_file):
    images = []
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            images.append(io.BytesIO(image_bytes))
    return images

def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def create_pdf_with_images_and_text(translated_text, images, output_file):
    c = canvas.Canvas(output_file, pagesize=letter)
    width, height = letter

    # Add images to the PDF
    for img in images:
        img_path = tempfile.mktemp(suffix=".png")
        with open(img_path, 'wb') as f:
            f.write(img.read())
        c.drawImage(img_path, 0, 0, width, height)
        os.remove(img_path)

    # Add translated text
    c.setFont("Helvetica", 12)
    text_object = c.beginText(40, height - 40)
    text_object.setTextOrigin(40, height - 40)
    text_object.setFont("Helvetica", 12)
    text_object.textLines(translated_text)
    c.drawText(text_object)

    c.showPage()
    c.save()

def main():
    st.title("PDF Translator with Formatting Preservation")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    # Input languages
    source_language = st.text_input("Enter source language code (e.g., 'en' for English)")
    target_language = st.text_input("Enter target language code (e.g., 'fr' for French)")

    if uploaded_file and source_language and target_language:
        st.write("Extracting text from the PDF...")
        pdf_text = extract_text_from_pdf(uploaded_file)

        if pdf_text:
            st.write("Translating text...")
            translated_text = translate_large_text(pdf_text, target_language, max_chunk_size=4000)
            
            # Extract images
            uploaded_file.seek(0)  # Reset file pointer to the beginning
            images = extract_images_from_pdf(uploaded_file)

            # Create a new PDF with the translated text and original images
            output_pdf_path = tempfile.mktemp(suffix=".pdf")
            create_pdf_with_images_and_text(translated_text, images, output_pdf_path)
            
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

