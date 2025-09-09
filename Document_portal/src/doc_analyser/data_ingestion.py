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
                os.path.join(os.getcwd(),"data","document_analysis"),
            )
            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4().hex[:8])}"

            self.session_path = os.path.join(self.data_dir, self.session_id)
            os.makedirs(self.session_path, exist_ok=True)

            self.log.info("PDF Handler intialised", session_id = self.session_id, session_path = self.session_path)

        except Exception as e:
            self.log.error(f"Error in initalising PDF Handler: {e}")
            raise Document_Portal_Exception("Error in intialising PDF Handler",sys)

    def save_pdf(self,uploaded_file):
        try:
            file_name = os.path.basename(uploaded_file.name)
            if not file_name.lower().endswith(".pdf"):
                raise Document_Portal_Exception("Invalid file type. Only PDF files are allowed.")

            save_path = os.path.join(self.session_path, file_name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            self.log.info("PDF saved successfully",pdf_path = save_path,session_id = self.session_id)
            return save_path
            
        except Exception as e:
            self.log.error(f"Error in saving PDF: {e}")
            raise Document_Portal_Exception("Error in saving PDF",sys)

    def read_pdf(self,pdf_path:str)->str:
        try:
            text_chunk = []
            with fitz.open(pdf_path) as doc:
                for page_num, page in enumerate(doc,start = 1):
                    text_chunk.append(f"\n ----Page {page_num} ----\n {page.get_text()}")
            text = "\n".join(text_chunk)
            
            self.log.info("PDF read successfully",pdf_path = pdf_path,session_id = self.session_id,pages = len(text_chunk))
            return " ".join(text_chunk)
        except Exception as e:
            self.log.error(f"Error in reading PDF: {e}")
            raise Document_Portal_Exception("Error in reading PDF",sys)

if __name__ == "__main__":
    from pathlib import Path
    from io import BytesIO
    handler = DocumentHandler()

    pdf_path = "/home/user/LLMOPS/Document_portal/data/document_alanysis/1706.03762v7.pdf"

    class DummyFile:
        def __init__(self, file_path):
            self.name = Path(file_path).name
            self._file_path = file_path

        def get_buffer(self):
            return open(self._file_path,"rb").read()

    dummy_pdf = DummyFile(pdf_path)

    handler = DocumentHandler(session_id = "test session")

    try:
        saved_path = handler.save_pdf(dummy_pdf)
        print(saved_path)
    except Exception as e:
        print("Error : {e}",e)

    