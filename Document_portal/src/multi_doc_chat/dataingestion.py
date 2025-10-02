import uuid
from pathlib import Path
import sys
from datetime import datetime,timezone
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader, UnstructuredMarkdownLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception
from utils.model_loader import ModelLoader

class DocumentIngestor:
    SUPPORTED_FILE_TYPES = {'.pdf','.docx','.txt','.md'}
    def __init__(self, temp_dir:str = "data/multi_doc_chat", faiss_dir:str = "faiss_index", session_id: str | None = None):
        try:
            self.log = CustomLogger().get_logger(__name__)

            self.temp_dir = Path(temp_dir)
            self.faiss_dir = Path(faiss_dir)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)

            self.session_id = session_id or f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4().hex[:8])}"
            self.session_temp_dir = self.temp_dir / self.session_id
            self.session_faiss_dir = self.faiss_dir / self.session_id
            self.session_temp_dir.mkdir(parents=True, exist_ok=True)
            self.session_faiss_dir.mkdir(parents=True, exist_ok=True)

            self.model_loader = ModelLoader()


            self.log.info("Multi Doc Ingestor initalized", 
            temp_base = str(self.temp_dir),
            faiss_base = str(self.faiss_dir),
            session_id = self.session_id,
            temp_path = str(self.session_temp_dir),
            faiss_path = str(self.session_faiss_dir))
        except Exception as e:
            self.log.error("Failed to initalize Multi Doc Ingestor",error = str(e))
            raise Document_Portal_Exception("Failed to initalize Multi Doc Ingestor",sys)
    def ingest_files(self,uploaded_files):
        try:
            documents = []

            for uploaded_file in uploaded_files:
                ext = Path(uploaded_file.name).suffix.lower()
                if ext not in self.SUPPORTED_FILE_TYPES:
                    self.log.warning("Unsupported file skipped", filename = uploaded_file.name)
                    continue

                unique_filename = f"{uuid.uuid4().hex[:8]}{ext}"
                temp_path = self.session_temp_dir / unique_filename

                with open(temp_path,"wb") as f_out:
                    f_out.write(uploaded_file.read())

                self.log.info("File saved for ingestion", filename=uploaded_file.name, saved_as=str(temp_path), session_id=self.session_id)
                
                if ext == '.pdf':
                    loader = PyPDFLoader(str(temp_path))
                elif ext == '.docx':
                    loader = Docx2txtLoader(str(temp_path))
                elif ext == ".txt":
                    loader = TextLoader(str(temp_path))
                elif ext == ".md":
                    loader = UnstructuredMarkdownLoader(str(temp_path))
                else:
                    self.log.warning("Unsupported file type encountered", filename = uploaded_file.name)
                    continue

                docs = loader.load()
                documents.extend(docs)

            if not documents:
                raise Document_Portal_Exception("No documents loaded",sys)
                self.log.warning("No documents loaded", session_id = self.session_id)

            self.log.info("All Files Loaded", total_docs = len(documents),session_id = self.session_id)
            return self._create_retriever(documents)

        except Exception as e:
            self.log.error("Failed to Ingest files",error = str(e))
            raise Document_Portal_Exception("Failed to Ingest files",sys)


    def _create_retriever(self,documents):
        try:
            splitter =  RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)

            chunks = splitter.split_documents(documents)
            self.log.info("PDF files splitted", count = len(chunks))

            embeddings = self.model_loader.load_embedding()
            vectorstore = FAISS.from_documents(documents = chunks,embedding = embeddings)
            vectorstore.save_local(str(self.session_faiss_dir))
            self.log.info("FAISS Index is created", faiss_path = str(self.session_faiss_dir))

            retriever = vectorstore.as_retriever(search_type = "similarity",search_kwargs = {"k":5})
            self.log.info("Retriever created successfully", retriever_type = str(type(retriever)))
            return retriever
            
        except Exception as e:
            self.log.error("Failed to create retriever",error = str(e))
            raise Document_Portal_Exception("Failed to create retriever",sys)