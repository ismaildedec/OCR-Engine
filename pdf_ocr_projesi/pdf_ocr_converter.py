import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import logging

class PDFToTextConverter:
    def __init__(self, tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe', 
        language='tur'):
    
        # Tesseract yolu
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
        self.language = language
        
        # Logging ayarları
        logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def convert_pdf_to_images(self, pdf_path):
        """
        PDF dosyasını görüntülere dönüştür
        
        Args:
        pdf_path (str): PDF dosya yolu
        
        Returns:
        list: Dönüştürülmüş görüntüler
        """
        try:
            images = convert_from_path(pdf_path)
            self.logger.info(f"{pdf_path} PDF'si görüntülere dönüştürüldü.")
            return images
        except Exception as e:
            self.logger.error(f"PDF dönüştürme hatası: {e}")
            return []

    def extract_text_from_images(self, images):
        """
        Görüntülerden metin çıkar
        
        Args:
        images (list): Görüntü listesi
        
        Returns:
        str: Çıkarılan metinler
        """
        extracted_texts = []
        for index, image in enumerate(images, 1):
            try:
                text = pytesseract.image_to_string(image, lang=self.language)
                extracted_texts.append(text)
                self.logger.info(f"{index}. sayfa metin çıkarma başarılı.")
            except Exception as e:
                self.logger.error(f"{index}. sayfa metin çıkarma hatası: {e}")
            
        return "\n\n".join(extracted_texts)

    def save_text(self, text, output_path):
        """
        Metni dosyaya kaydet
        
        Args:
        text (str): Çıkarılan metin
        output_path (str): Çıktı dosya yolu
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as file:
             file.write(text)
            self.logger.info(f"Metin {output_path}'a kaydedildi.")
        except Exception as e:
            self.logger.error(f"Dosya kaydetme hatası: {e}")

    def process_pdf(self, pdf_path, output_path=None):
        """
        PDF'yi işle ve metne dönüştür
        
        Args:
        pdf_path (str): Giriş PDF dosya yolu
        output_path (str, optional): Çıktı metin dosya yolu
        
        Returns:
        str: Çıkarılan metin
        """
        # PDF'yi görüntülere dönüştürür
        images = self.convert_pdf_to_images(pdf_path)
        
        if not images:
            self.logger.error("Hiç görüntü oluşturulamadı!")
            return ""
        
        # Görüntülerden metin çıkar
        extracted_text = self.extract_text_from_images(images)
        
        #  çıktı yolu verilmişse metni kaydet
        if output_path:
            self.save_text(extracted_text, output_path)
        
        return extracted_text

def main():
   
        converter = PDFToTextConverter(
        # Tesseract executable path
        tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        language='tur'  # Türkçe OCR için
        )   
        
        # PDF dosya yolunu ve çıktı dosya yolu
        pdf_path = 'ornek_dokuman.pdf'
        output_path = 'cikti_metin.txt'
        
        # PDF'yi işle
        extracted_text = converter.process_pdf(pdf_path, output_path)
        
        # Konsola yazdır
        print(extracted_text)

if __name__ == "__main__":
        main()