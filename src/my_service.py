from common_code.config import get_settings
from common_code.logger.logger import get_logger, Logger
from common_code.service.models import Service
from common_code.service.enums import ServiceStatus
from common_code.common.enums import FieldDescriptionType, ExecutionUnitTagName, ExecutionUnitTagAcronym
from common_code.common.models import FieldDescription, ExecutionUnitTag
from common_code.tasks.models import TaskData
# Imports required by the service's model
from text_recognition.text_recognition import PDFReader
import io
import json

api_description = """This service extracts text for a PDF file.
"""
api_summary = """Returns a JSON file containing the text in the input PDF
"""

api_title = "PDF extraction API."
version = "0.0.1"

settings = get_settings()


class MyService(Service):
    """
    PDF Extractor service model
    """

    _model: object
    _logger: Logger

    def __init__(self):
        super().__init__(
            name="PDF Extractor",
            slug="pdf-extractor",
            url=settings.service_url,
            summary=api_summary,
            description=api_description,
            status=ServiceStatus.AVAILABLE,

            data_in_fields=[
                FieldDescription(name="file", type=[FieldDescriptionType.APPLICATION_PDF]),
            ],
            data_out_fields=[
                FieldDescription(
                    name="result", type=[FieldDescriptionType.APPLICATION_JSON]
                ),
            ],
            tags=[
                ExecutionUnitTag(
                    name=ExecutionUnitTagName.NATURAL_LANGUAGE_PROCESSING,
                    acronym=ExecutionUnitTagAcronym.NATURAL_LANGUAGE_PROCESSING,
                ),
            ],
            has_ai=True,
            docs_url="https://docs.swiss-ai-center.ch/reference/services/pdf-extractor/",
        )
        self._logger = get_logger(settings)

    def process(self, data):
        # The 'file' is the PDF file input, assumed to be a file-like object or bytes
        pdf_file = data["file"].data  # PDF file in bytes
        # Wrap the bytes object in a BytesIO file-like object
        pdf_file_obj = io.BytesIO(pdf_file)

        # Create a PDFReader instance and pass the file-like object
        pdf_reader = PDFReader(pdf_file_obj)

        # Read all pages of the PDF and extract the text
        text_data = pdf_reader.read_first_page()  # Use read_first_page() if only the first page is needed

        # Format the extracted data as a dictionary
        json_data = {'text': text_data}

        # Encode the dictionary to JSON
        json_bytes = json.dumps(json_data).encode('utf-8')

        # Return the result with the required field name
        return {
            "result": TaskData(data=json_bytes, type=FieldDescriptionType.APPLICATION_JSON),
        }
