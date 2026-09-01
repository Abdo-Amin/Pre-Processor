from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


class PDFToChromaETL:
    def __init__(self, persist_dir="./files/chroma_db/"):
        self.persist_dir = persist_dir
        self.embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    def extract(self, pdf_path):                  # E
        return PyPDFLoader(pdf_path).load()

    def transform(self, docs):                   # T
        splitter = RecursiveCharacterTextSplitter(chunk_size = 150, chunk_overlap = 100)
        return splitter.split_documents(docs)

    def load(self, chunks):                      # L
        return Chroma.from_documents(
            chunks, self.embeddings,
            persist_directory=self.persist_dir
        )

    def run(self, pdf_path):
        docs = self.extract(pdf_path)
        chunks = self.transform(docs)
        db = self.load(chunks)
        return db
