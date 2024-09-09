# Code based on https://gitlab.forge.hefr.ch/icoservices/deepmarket/image/text-recognition

import logging

class PDFReader:
    def __init__(self, file):
        self.file = file
        self.logger = logging.getLogger(__name__)

    def read_first_page(self):
        self.logger.info("Reading first page of the PDF")
        with pdfplumber.open(self.file) as pdf:
            self.logger.info("open pdf file")
            if len(pdf.pages) > 0:
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                if text:
                    self.logger.info("Text extracted from the first page")
                    return text
                else:
                    self.logger.warning("No text found on the first page")
                    return "No text found"
            else:
                self.logger.error("PDF has no pages")
                raise ValueError("PDF has no pages")