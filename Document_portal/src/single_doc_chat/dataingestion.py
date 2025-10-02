import uuid
from pathlib import Path
import sys
from datetime import datetime,timezone
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception
from utils.model_loader import ModelLoader

class SingleDocIngestor:
    def __init__(self,data_dir : str = "data/single_document_chat",faiss_dir:str = "faiss_index"):
        try:
            self.log = CustomLogger().get_logger(__name__)
            self.data_dir = Path(data_dir)
            self.data_dir.mkdir(parents=True, exist_ok=True)
            self.faiss_dir = Path(faiss_dir)
            self.faiss_dir.mkdir(parents=True, exist_ok=True)
            self.model_loader = ModelLoader()
            self.log.info("Single Doc Ingestor initalized")
        except Exception as e:
            self.log.error("Failed to initalize Single Doc Ingestor",error = str(e))
            raise Document_Portal_Exception("Failed to initalize Single Doc Ingestor",sys)

    def ingest_files(self,uploaded_files):
        try:
            documents = []
            for uploaded_file in uploaded_files:
                unique_filename = f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4().hex[:8])}"
                temp_path = self.data_dir/ unique_filename

                with open(temp_path,"wb") as f_out:
                    f_out.write(uploaded_file.read())
                self.log.info("PDF saved for ingestion", filename = uploaded_file.name)
                loader = PyPDFLoader(str(temp_path))
                docs = loader.load()
                documents.extend(docs)
            self.log.info("PDF files Loaded", count = len(documents))
            return self._create_retriver(documents)

        except Exception as e:
            self.log.error("Failed to ingest files",error = str(e))
            raise Document_Portal_Exception("Failed to ingest files",sys)

    def _create_retriver(self,documents):
        try:
            splitter =  RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 300)
            chunks = splitter.split_documents(documents)
            self.log.info("PDF files splitted", count = len(chunks))

            embeddings = self.model_loader.load_embedding()
            vectorstore = FAISS.from_documents(documents = chunks,embedding = embeddings)
            vectorstore.save_local(str(self.faiss_dir))
            self.log.info("FAISS Index is created", faiss_path = str(self.faiss_dir))
            retriever = vectorstore.as_retriever(search_type = "similarity",search_kwargs = {"k":5})
            self.log.info("Retriever created successfully", retriever_type = str(type(retriever)))
            return retriever

            
        except Exception as e:
            self.log.error("Failed to create retriver",error = str(e))
            raise Document_Portal_Exception("Failed to create retriver",sys)