"""
OCR Processing Module
Handles text extraction from images and scanned documents using EasyOCR.
"""

import os
from typing import Optional, List, Tuple
import cv2
import numpy as np
from PIL import Image
import easyocr
from dotenv import load_dotenv

load_dotenv()


class OCRProcessor:
    """
    Processor for extracting text from images and scanned documents using EasyOCR.
    """
    
    def __init__(self, use_gpu: bool = False, language: str = 'en'):
        """
        Initialize OCR processor.
        
        Args:
            use_gpu: Whether to use GPU for processing.
            language: Language code for OCR (default: 'en').
        """
        self.use_gpu = use_gpu
        self.language = language
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """Initialize EasyOCR reader."""
        try:
            self.reader = easyocr.Reader(
                [self.language],
                gpu=self.use_gpu,
                verbose=False
            )
        except Exception as e:
            raise Exception(f"Failed to initialize EasyOCR reader: {str(e)}")
    
    def extract_text_from_image(
        self,
        image_path: str,
        detail_level: int = 0
    ) -> str:
        """
        Extract text from an image file.
        
        Args:
            image_path: Path to the image file.
            detail_level: Detail level for OCR (0 = text only, 1 = with coordinates).
            
        Returns:
            Extracted text as string.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            # Read image
            result = self.reader.readtext(image_path, detail=detail_level)
            
            # Extract text from results
            if detail_level == 0:
                text = ' '.join(result)
            else:
                text = ' '.join([detection[1] for detection in result])
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    def extract_text_from_pil_image(
        self,
        pil_image: Image.Image,
        detail_level: int = 0
    ) -> str:
        """
        Extract text from a PIL Image object.
        
        Args:
            pil_image: PIL Image object.
            detail_level: Detail level for OCR.
            
        Returns:
            Extracted text as string.
        """
        try:
            # Convert PIL image to numpy array
            image_array = np.array(pil_image)
            
            # Perform OCR
            result = self.reader.readtext(image_array, detail=detail_level)
            
            # Extract text
            if detail_level == 0:
                text = ' '.join(result)
            else:
                text = ' '.join([detection[1] for detection in result])
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Error extracting text from PIL image: {str(e)}")
    
    def extract_text_with_coordinates(
        self,
        image_path: str
    ) -> List[Tuple[Tuple[int, int, int, int], str, float]]:
        """
        Extract text with bounding box coordinates.
        
        Args:
            image_path: Path to the image file.
            
        Returns:
            List of tuples containing (bbox, text, confidence).
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        try:
            result = self.reader.readtext(image_path, detail=1)
            return result
            
        except Exception as e:
            raise Exception(f"Error extracting text with coordinates: {str(e)}")
    
    def preprocess_image(
        self,
        image_path: str,
        output_path: Optional[str] = None
    ) -> str:
        """
        Preprocess image to improve OCR accuracy.
        
        Args:
            image_path: Path to the input image.
            output_path: Path to save preprocessed image. If None, overwrites original.
            
        Returns:
            Path to the preprocessed image.
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Denoise
            denoised = cv2.fastNlMeansDenoising(binary, h=10)
            
            # Save preprocessed image
            output = output_path or image_path
            cv2.imwrite(output, denoised)
            
            return output
            
        except Exception as e:
            raise Exception(f"Error preprocessing image: {str(e)}")
    
    def extract_text_from_scanned_pdf(
        self,
        pdf_path: str,
        page_range: Optional[Tuple[int, int]] = None
    ) -> str:
        """
        Extract text from a scanned PDF by converting pages to images first.
        
        Args:
            pdf_path: Path to the PDF file.
            page_range: Optional tuple (start_page, end_page) for specific pages.
            
        Returns:
            Extracted text from all pages.
        """
        try:
            from pdf2image import convert_from_path
            
            # Convert PDF to images
            if page_range:
                images = convert_from_path(
                    pdf_path,
                    first_page=page_range[0],
                    last_page=page_range[1]
                )
            else:
                images = convert_from_path(pdf_path)
            
            # Extract text from each image
            all_text = []
            for i, image in enumerate(images):
                text = self.extract_text_from_pil_image(image)
                all_text.append(f"--- Page {i + 1} ---\n{text}")
            
            return '\n\n'.join(all_text)
            
        except ImportError:
            raise Exception(
                "pdf2image is required for PDF processing. "
                "Install it with: pip install pdf2image"
            )
        except Exception as e:
            raise Exception(f"Error extracting text from scanned PDF: {str(e)}")
    
    def is_image_scanned(self, image_path: str, threshold: float = 0.1) -> bool:
        """
        Determine if an image is a scanned document.
        
        Args:
            image_path: Path to the image.
            threshold: Threshold for determining if scanned.
            
        Returns:
            True if image appears to be a scanned document.
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Calculate edge density
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            
            # High edge density suggests scanned document
            return edge_density > threshold
            
        except Exception as e:
            raise Exception(f"Error determining if image is scanned: {str(e)}")
    
    def get_text_confidence_scores(self, image_path: str) -> List[float]:
        """
        Get confidence scores for extracted text.
        
        Args:
            image_path: Path to the image.
            
        Returns:
            List of confidence scores.
        """
        try:
            result = self.extract_text_with_coordinates(image_path)
            return [detection[2] for detection in result]
            
        except Exception as e:
            raise Exception(f"Error getting confidence scores: {str(e)}")
    
    def extract_structured_text(
        self,
        image_path: str
    ) -> dict:
        """
        Extract text with structure information.
        
        Args:
            image_path: Path to the image.
            
        Returns:
            Dictionary with structured text data.
        """
        try:
            result = self.extract_text_with_coordinates(image_path)
            
            structured_data = {
                'text_blocks': [],
                'average_confidence': 0.0,
                'total_blocks': len(result)
            }
            
            total_confidence = 0.0
            for bbox, text, confidence in result:
                structured_data['text_blocks'].append({
                    'text': text,
                    'bbox': bbox,
                    'confidence': confidence
                })
                total_confidence += confidence
            
            if result:
                structured_data['average_confidence'] = total_confidence / len(result)
            
            return structured_data
            
        except Exception as e:
            raise Exception(f"Error extracting structured text: {str(e)}")


class ImagePreprocessor:
    """
    Utility class for image preprocessing operations.
    """
    
    @staticmethod
    def resize_image(
        image_path: str,
        output_path: str,
        max_width: int = 2000,
        max_height: int = 2000
    ) -> str:
        """
        Resize image while maintaining aspect ratio.
        
        Args:
            image_path: Path to input image.
            output_path: Path to save resized image.
            max_width: Maximum width.
            max_height: Maximum height.
            
        Returns:
            Path to resized image.
        """
        try:
            image = Image.open(image_path)
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            image.save(output_path)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error resizing image: {str(e)}")
    
    @staticmethod
    def enhance_contrast(image_path: str, output_path: str) -> str:
        """
        Enhance image contrast for better OCR.
        
        Args:
            image_path: Path to input image.
            output_path: Path to save enhanced image.
            
        Returns:
            Path to enhanced image.
        """
        try:
            from PIL import ImageEnhance
            
            image = Image.open(image_path)
            enhancer = ImageEnhance.Contrast(image)
            enhanced = enhancer.enhance(2.0)
            enhanced.save(output_path)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error enhancing contrast: {str(e)}")
    
    @staticmethod
    def remove_noise(image_path: str, output_path: str) -> str:
        """
        Remove noise from image.
        
        Args:
            image_path: Path to input image.
            output_path: Path to save cleaned image.
            
        Returns:
            Path to cleaned image.
        """
        try:
            image = cv2.imread(image_path)
            denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
            cv2.imwrite(output_path, denoised)
            return output_path
            
        except Exception as e:
            raise Exception(f"Error removing noise: {str(e)}")
