import io
from pypdf import PdfReader
from fastapi import UploadFile

async def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extract text content from an uploaded PDF file.
    """
    content = await file.read()
    pdf_file = io.BytesIO(content)
    reader = PdfReader(pdf_file)
    
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
        
    # Reset file cursor for further usage if needed
    await file.seek(0)
    
    return text
