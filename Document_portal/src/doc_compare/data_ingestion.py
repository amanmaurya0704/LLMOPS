import sys
from pathlib import Path
import fitz
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception

class DocumentIngestion:
    def __init__(self,base_dir:str = "Document_portal/data/data_comparison" ):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
    def delete_existing_files(self):
        try:
            if self.base_dir.exists() and self.base_dir.is_dir():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File Deleted.", path = str(file))
                self.log.info("Directory cleaned", directory = str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error in deleting existing files: {e}")
            raise Document_Portal_Exception("Error in deleting existing files",sys)


    def save_uploaded_files(self,reference_file, actual_file):
        try:
            self.delete_existing_files()
            self.log.info("Existing file deleted successfully.")

            self.base_dir.mkdir(parents=True, exist_ok=True)

            ref_path = self.base_dir/reference_file.name
            act_path = self.base_dir/actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Invalid file type. Only PDF files are allowed.")

            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())

            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files Saved", reference = str(ref_path), actual = str(act_path))
            return ref_path, act_path


        except Exception as e:
            self.log.error(f"Error in saving uploaded files: {e}")
            raise Document_Portal_Exception("Error in saving uploaded files",sys)


    def combine_documents(self) -> str:
        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)

            for filename, content in content_dict.items():
                doc_parts.append(f"Document : {filename} \n {content}")

            combined_text = "\n\n".join(doc_parts)
            self.log.info("Documents combined successfully", count=len(doc_parts))
            return combined_text
        except Exception as e:
            self.log.error(f"Error in combining documents: {e}")
            raise Document_Portal_Exception("Error in combining documents",sys)

            
    def clean_old_sessions(self):
        try:
            session_folder = sorted(
                [f for f in self.base_dir.iterdir() if f.is_dir()],
                reverse = True
            )
            for folder in session_folder[keep_latest:]:
                for file in folder.iterdir():
                    file.unlink()
                folder.rmkdir()
                self.log.info("Old sessions cleaned successfully", path = str(folder)
                )
        except Exception as e:
            self.log.error(f"Error in cleaning old sessions: {e}")
            raise Document_Portal_Exception("Error in cleaning old sessions",sys)

    def read_pdf(self,pdf_path: Path)->str:
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page = doc.load_page(page_num)
                    text = page.get_text()
                    if text.strip():
                        all_text.append(f"\n---- Page {page_num +1 }-----\n {text}")
                self.log.info("PDF read successfully", file = str(pdf_path), pages = len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error(f"Error in reading pdf: {e}")
            raise Document_Portal_Exception("Error in reading pdf",sys)
