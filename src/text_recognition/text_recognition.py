# Code based on https://gitlab.forge.hefr.ch/icoservices/deepmarket/image/text-recognition

import pdfplumber

class PDFReader:
    def __init__(self, file):
        self.file = file
    
    def read_first_page(self):
        with pdfplumber.open(self.file) as pdf:
            first_page = pdf.pages[0]
            return first_page.extract_text()