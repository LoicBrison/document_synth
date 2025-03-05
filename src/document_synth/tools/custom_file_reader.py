import fitz   # PyMuPDF
import docx
import pandas as pd
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
# from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, UnstructuredExcelLoader


class CustomFileReaderInput(BaseModel):
    """Input schema for CustomFileReader."""
    argument: str = Field(..., description="Path.")

class CustomFileReader(BaseTool):

    name: str = "Cusotm File Reader"
    description: str = (
        "Clear description for what this tool is useful for, your agent will need this information to use it."
    )
    args_schema: Type[BaseModel] = CustomFileReaderInput

    def _run(self, argument: str) -> str:
        file_path = argument
        if file_path.endswith(".pdf"):
            return self.read_pdf(file_path)
        elif file_path.endswith(".docx"):
            return self.read_docx(file_path)
        elif file_path.endswith(".xlsx"):
            return self.read_excel(file_path)
        else:
            return "Format non supporté"

    def read_pdf(self, file_path):
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def read_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def read_excel(self, file_path):
        df = pd.read_excel(file_path)
        return df.to_string()

    # def read_pdf(self, file_path):
    #     loader = PyPDFLoader(file_path)
    #     docs = loader.load()
    #     return docs[0].page_content
       
    # def read_docx(self, file_path):
    #     loader = UnstructuredWordDocumentLoader(file_path)
    #     docs = loader.load()
    #     return docs[0].page_content

    # def read_excel(self, file_path):
    #     loader = UnstructuredExcelLoader(file_path)
    #     docs = loader.load()
    #     return docs[0].page_content

