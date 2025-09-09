import os
import sys
sys.path.insert(0, 'C:\\Users\\amanm\\Downloads\\Machine Learning\\LLMOPS\\Document_portal')
from utils.model_loader import ModelLoader
from logger.custom_logging import CustomLogger
from exception.custom_exception import Document_Portal_Exception
from model.models import *
from langchain.output_parsers import JsonOutputToolsParser
from langchain.output_parsers import OutputFixingParser
import sys
from prompt import *

class DocumentAnalyser:
    def __init__(self):
        self.log = CustomLogger().get_logger(__name__)
        try:
            self.loader = ModelLoader()
            self.llm = self.loader.load_llm()

            self.parser = JsonOutputToolsParser(pydantic_object = MetaData)
            self.fixing_parser = OutputFixingParser.from_llm(parser=self.parser, llm=self.llm)

            self.prompt = prompt

            self.log.info("Document Analyser Initialised")


        except:
            self.log.error(f"Error in initalising Document Analyzer: {e}")
            raise Document_Portal_Exception("Error in intialising Analyser",sys)

    def analyse_metadata(self, document_text:str)->dict:
        """
        Analyse the document's text and extract structured meta data and summary.
        """

        try:
            chain = self.prompt | self.llm | self.fixing_parser
            self.log.info("Meta data analysis chain initalised")

            response = chain.invoke({
                "format_instructions": self.parser.get_format_instructions(),
                "document_text": document_text
            })

            self.log.info("meta data extraction successful", keys = list(response.keys))

            return response

        except:
            self.log.error(f"Error in analysing metadata: {e}")
            raise Document_Portal_Exception("Error in analysing metadata",sys)

