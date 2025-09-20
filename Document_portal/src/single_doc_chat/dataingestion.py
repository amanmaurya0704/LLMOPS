import uuid
from pathlib import Path
import sys
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception
from utils.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self):
        try:
            self.log = CustomLogger().get_logger(__name__)
        except Exception as e:
            self.log.error("Failed to initalize Single Doc Ingestor",error = str(e))
            raise Document_Portal_Exception("Failed to initalize Single Doc Ingestor",sys)

    def ingest_files(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to ingest files",error = str(e))
            raise Document_Portal_Exception("Failed to ingest files",sys)

    def _create_retriver(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to create retriver",error = str(e))
            raise Document_Portal_Exception("Failed to create retriver",sys)