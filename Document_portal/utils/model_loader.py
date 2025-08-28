import os
import sys
import json
from dotenv import load_dotenv
from utils.config_loader import load_config
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from logger.custom_logging import CustomLogger
from exception.custom_exception import DocumentPortalException

log = CustomLogger().get_logger(__name__)

class ModelLoader:
    def __init__(self):
        pass

    def _validate_env(self):
        pass

    def load_embedding(self):
        pass

    def load_model(self):
        pass