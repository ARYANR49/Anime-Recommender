from langchain.text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

class VectorStoreBuilder:
    def __init__(self,csv_path:str,persist_dir:str=os.path.abspath("FAISS_index")):

        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embedding = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2")
    
    def build_and_save_vectorstore(self):
        if not self.csv_path or not os.path.exists(self.csv_path):
         print("Skipping vector store build — no valid CSV path provided.")
         return
        
        loader = CSVLoader(
            file_path=self.csv_path,
            encoding='utf-8',
            metadata_columns=[]
        )

        data = loader.load()

        splitter = CharacterTextSplitter(chunk_size=1000,chunk_overlap=0)
        texts = splitter.split_documents(data)

        # db = FAISS.from_documents(texts,self.embedding,persist_directory=self.persist_dir)
        db = FAISS.from_documents(texts,self.embedding)
        db.save_local(self.persist_dir,self.embedding)
        

    def load_vector_store(self):
        return FAISS.load_local(self.persist_dir,self.embedding, allow_dangerous_deserialization=True)



