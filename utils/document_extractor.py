"""
Document Extraction Module
Handles text extraction from various document formats including PDF, DOCX, and images.
"""

import os
from typing import Optional, List, Dict, Any
import fitz  # PyMuPDF
from docx import Document
from PIL import Image
import io
from .ocr_processor import OCRProcessor, ImagePreprocessor


class DocumentExtractor:
    """
    Extract text from various document formats.
    """
    
    def __init__(self, ocr_processor: Optional[OCRProcessor] = None):
        """
        Initialize document extractor.
        
        Args:
            ocr_processor: Optional OCRProcessor instance for image-based extraction.
        """
        self.ocr_processor = ocr_processor or OCRProcessor()
    
    def extract_text(self, file_path: str, use_ocr: bool = True) -> str:
        """
        Extract text from a document based on its file type.
        
        Args:
            file_path: Path to the document file.
            use_ocr: Whether to use OCR for scanned documents.
            
        Returns:
            Extracted text as string.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        extractors = {
            '.pdf': self.extract_from_pdf,
            '.docx': self.extract_from_docx,
            '.doc': self.extract_from_docx,
            '.png': self.extract_from_image,
            '.jpg': self.extract_from_image,
            '.jpeg': self.extract_from_image,
        }
        
        extractor = extractors.get(file_extension)
        if not extractor:
            raise ValueError(f"Unsupported file format: {file_extension}")
        
        return extractor(file_path, use_ocr=use_ocr)
    
    def extract_from_pdf(self, pdf_path: str, use_ocr: bool = True) -> str:
        """
        Extract text from PDF file.
        
        Args:
            pdf_path: Path to the PDF file.
            use_ocr: Whether to use OCR for scanned pages.
            
        Returns:
            Extracted text from all pages.
        """
        try:
            doc = fitz.open(pdf_path)
            all_text = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Try to extract text directly
                text = page.get_text()
                
                # If text extraction fails or returns very little text, use OCR
                if use_ocr and (not text or len(text.strip()) < 50):
                    # Convert page to image
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    img = Image.open(io.BytesIO(img_data))
                    
                    # Use OCR
                    text = self.ocr_processor.extract_text_from_pil_image(img)
                
                all_text.append(f"--- Page {page_num + 1} ---\n{text}")
            
            doc.close()
            return '\n\n'.join(all_text)
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def extract_from_docx(self, docx_path: str, use_ocr: bool = False) -> str:
        """
        Extract text from DOCX file.
        
        Args:
            docx_path: Path to the DOCX file.
            use_ocr: Whether to use OCR for embedded images (not implemented).
            
        Returns:
            Extracted text from document.
        """
        try:
            doc = Document(docx_path)
            all_text = []
            
            # Extract text from paragraphs
            for paragraph in doc.paragraphs:
                all_text.append(paragraph.text)
            
            # Extract text from tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        all_text.append(cell.text)
            
            return '\n'.join(all_text)
            
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
    
    def extract_from_image(self, image_path: str, use_ocr: bool = True) -> str:
        """
        Extract text from image file using OCR.
        
        Args:
            image_path: Path to the image file.
            use_ocr: Whether to use OCR.
            
        Returns:
            Extracted text.
        """
        if not use_ocr:
            raise ValueError("OCR must be enabled for image files")
        
        return self.ocr_processor.extract_text_from_image(image_path)
    
    def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from document.
        
        Args:
            file_path: Path to the document file.
            
        Returns:
            Dictionary containing metadata.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_extension = os.path.splitext(file_path)[1].lower()
        metadata = {
            'file_name': os.path.basename(file_path),
            'file_size': os.path.getsize(file_path),
            'file_type': file_extension,
        }
        
        if file_extension == '.pdf':
            try:
                doc = fitz.open(file_path)
                metadata.update({
                    'page_count': len(doc),
                    'title': doc.metadata.get('title', ''),
                    'author': doc.metadata.get('author', ''),
                    'subject': doc.metadata.get('subject', ''),
                    'creator': doc.metadata.get('creator', ''),
                })
                doc.close()
            except Exception as e:
                metadata['error'] = str(e)
        
        elif file_extension in ['.docx', '.doc']:
            try:
                doc = Document(file_path)
                metadata.update({
                    'paragraph_count': len(doc.paragraphs),
                    'table_count': len(doc.tables),
                })
            except Exception as e:
                metadata['error'] = str(e)
        
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            try:
                with Image.open(file_path) as img:
                    metadata.update({
                        'width': img.width,
                        'height': img.height,
                        'format': img.format,
                        'mode': img.mode,
                    })
            except Exception as e:
                metadata['error'] = str(e)
        
        return metadata
    
    def is_scanned_pdf(self, pdf_path: str, threshold: float = 0.5) -> bool:
        """
        Determine if a PDF is scanned (image-based) or text-based.
        
        Args:
            pdf_path: Path to the PDF file.
            threshold: Threshold for determining if scanned.
            
        Returns:
            True if PDF appears to be scanned.
        """
        try:
            doc = fitz.open(pdf_path)
            
            # Check first few pages
            pages_to_check = min(3, len(doc))
            total_text_length = 0
            
            for page_num in range(pages_to_check):
                page = doc[page_num]
                text = page.get_text()
                total_text_length += len(text.strip())
            
            doc.close()
            
            # If average text per page is very low, likely scanned
            avg_text_per_page = total_text_length / pages_to_check
            return avg_text_per_page < threshold
            
        except Exception as e:
            raise Exception(f"Error determining if PDF is scanned: {str(e)}")
    
    def extract_images_from_pdf(self, pdf_path: str, output_dir: str) -> List[str]:
        """
        Extract all images from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file.
            output_dir: Directory to save extracted images.
            
        Returns:
            List of paths to extracted images.
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            doc = fitz.open(pdf_path)
            image_paths = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_data = base_image["image"]
                    
                    # Save image
                    image_path = os.path.join(
                        output_dir,
                        f"page_{page_num + 1}_img_{img_index + 1}.png"
                    )
                    with open(image_path, "wb") as f:
                        f.write(image_data)
                    
                    image_paths.append(image_path)
            
            doc.close()
            return image_paths
            
        except Exception as e:
            raise Exception(f"Error extracting images from PDF: {str(e)}")


class TextCleaner:
    """
    Utility class for cleaning and normalizing extracted text.
    """
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize extracted text.
        
        Args:
            text: Raw extracted text.
            
        Returns:
            Cleaned text.
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove page markers
        text = text.replace('--- Page', '\n--- Page')
        
        # Remove common artifacts
        artifacts = [
            '\x0c',  # Form feed
            '\x00',  # Null character
        ]
        
        for artifact in artifacts:
            text = text.replace(artifact, '')
        
        return text.strip()
    
    @staticmethod
    def extract_sections(text: str) -> Dict[str, str]:
        """
        Extract common resume sections from text.
        
        Args:
            text: Resume text.
            
        Returns:
            Dictionary mapping section names to content.
        """
        sections = {}
        section_keywords = {
            'experience': ['experience', 'work history', 'employment', 'professional experience'],
            'education': ['education', 'academic', 'qualifications', 'learning'],
            'skills': ['skills', 'technical skills', 'competencies', 'technologies'],
            'projects': ['projects', 'portfolio', 'work'],
            'certificates': ['certificates', 'certifications', 'credentials'],
            'summary': ['summary', 'profile', 'about', 'objective'],
        }
        
        lines = text.split('\n')
        current_section = 'other'
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Check if this line starts a new section
            found_section = None
            for section, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    found_section = section
                    break
            
            if found_section:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                
                # Start new section
                current_section = found_section
                current_content = [line]
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """
        Extract contact information from text.
        
        Args:
            text: Resume text.
            
        Returns:
            Dictionary with contact information.
        """
        import re
        
        contact_info = {
            'email': '',
            'phone': '',
            'linkedin': '',
            'github': '',
        }
        
        # Extract email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Extract phone number
        phone_pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
        phone_match = re.search(phone_pattern, text)
        if phone_match:
            contact_info['phone'] = phone_match.group()
        
        # Extract LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[a-zA-Z0-9-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        if linkedin_match:
            contact_info['linkedin'] = f"https://{linkedin_match.group()}"
        
        # Extract GitHub
        github_pattern = r'github\.com/[a-zA-Z0-9-]+'
        github_match = re.search(github_pattern, text)
        if github_match:
            contact_info['github'] = f"https://{github_match.group()}"
        
        return contact_info


class FileValidator:
    """
    Validate uploaded files.
    """
    
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    
    @classmethod
    def validate_file(cls, file_path: str) -> tuple[bool, str]:
        """
        Validate a file.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            Tuple of (is_valid, error_message).
        """
        if not os.path.exists(file_path):
            return False, "File does not exist"
        
        # Check file extension
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension not in cls.ALLOWED_EXTENSIONS:
            return False, f"Unsupported file type: {file_extension}"
        
        # Check file size
        file_size = os.path.getsize(file_path)
        if file_size > cls.MAX_FILE_SIZE:
            return False, f"File too large: {file_size / (1024*1024):.2f} MB (max: {cls.MAX_FILE_SIZE / (1024*1024)} MB)"
        
        return True, ""
    
    @classmethod
    def get_file_info(cls, file_path: str) -> Dict[str, Any]:
        """
        Get information about a file.
        
        Args:
            file_path: Path to the file.
            
        Returns:
            Dictionary with file information.
        """
        return {
            'name': os.path.basename(file_path),
            'size': os.path.getsize(file_path),
            'extension': os.path.splitext(file_path)[1].lower(),
            'is_valid': cls.validate_file(file_path)[0],
        }
