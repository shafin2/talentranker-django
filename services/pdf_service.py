"""
PDF Processing Service
Handles PDF text extraction and validation
"""
import PyPDF2
from io import BytesIO


def extract_text_from_pdf(pdf_buffer):
    """
    Extract text content from PDF buffer.
    
    Args:
        pdf_buffer: File buffer or bytes object containing PDF data
    
    Returns:
        str: Extracted text content
    
    Raises:
        Exception: If PDF parsing fails
    """
    try:
        if isinstance(pdf_buffer, bytes):
            pdf_buffer = BytesIO(pdf_buffer)
        
        pdf_reader = PyPDF2.PdfReader(pdf_buffer)
        text = ''
        
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        return text.strip()
    
    except Exception as e:
        raise Exception(f'Failed to extract text from PDF: {str(e)}')


def validate_pdf(file):
    """
    Validate PDF file.
    
    Args:
        file: Uploaded file object
    
    Returns:
        bool: True if valid
    
    Raises:
        Exception: If validation fails
    """
    # Check file type
    if not file.content_type == 'application/pdf':
        raise Exception('Only PDF files are allowed')
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if file.size > max_size:
        raise Exception('File size exceeds 10MB limit')
    
    return True
