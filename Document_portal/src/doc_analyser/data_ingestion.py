import os
import fitz
import uuid
from datetime import datetime
import sys

from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception

class DocumentHandler:
    def __init__(self,data_dir=None,session_id=None):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = data_dir or os.getenv(
                "DAT_STORAGE_PATH",
                os.path.join(os.getcwd(), "data","document_analysis"),
            )
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4().hex[:8])}"

            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            self.log.info("PDF Handler intialised", session_id = self.session_id, session_path = self.session_path)

        except Exception as e:
            self.log.error(f"Error in initalising PDF Handler: {e}")
            raise Document_Portal_Exception("Error in intialising PDF Handler",sys)

    def save_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in saving PDF: {e}")
            raise Document_Portal_Exception("Error in saving PDF",sys)

    def read_pdf(self):
        try:
            pass
        except Exception as e:
            self.log.error(f"Error in reading PDF: {e}")
            raise Document_Portal_Exception("Error in reading PDF",sys)

if __name__ == "__main__":
    handler = DocumentHandler()
    