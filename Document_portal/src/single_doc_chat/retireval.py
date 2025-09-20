import sys
import os
from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.vectorstores import FAISS
from langchain_core.runnables.history import RunnablewithMessageHistory
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_document_chain
from utils.model_loader import ModelLoader
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception
from prompt.prompt_library import PROMPT_REGISTRY


class ConversationalRAG:
    def __init__(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to initalize Conversational RAG",error = str(e))
            raise Document_Portal_Exception("Failed to initalize Conversational RAG",sys)

    def _load_llm(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load LLM",error = str(e))
            raise Document_Portal_Exception("Failed to load LLM",sys)

    def _get_session_history(self, session_id:str):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to get session history",error = str(e))
            raise Document_Portal_Exception("Failed to get session history",sys)

    def load_retriever_from_faiss(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to load retriever from FAISS",error = str(e))
            raise Document_Portal_Exception("Failed to load retriever from FAISS",sys)

    def invoke(self):
        try:
            pass
        except Exception as e:
            self.log.error("Failed to invoke RAG",error = str(e))
            raise Document_Portal_Exception("Failed to invoke RAG",sys)

 