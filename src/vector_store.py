import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from embeddings import get_embedding_function

FAISS_PATH = "faiss_index"

class VectorStore:
    def __init__(self):
        self.faiss_path = FAISS_PATH
        self.embedding_function = get_embedding_function()
        self._db = None
        
    def get_db(self):
        """Get or create the FAISS database."""
        if self._db is not None:
            return self._db
            
        if os.path.exists(self.faiss_path):
            # Load existing index
            self._db = FAISS.load_local(
                self.faiss_path,
                self.embedding_function,
                allow_dangerous_deserialization=True
            )
        return self._db

    def add_documents(self, documents: list[Document]):
        """Add documents to the vector store."""
        if not documents:
            return 0
            
        if self._db is None and os.path.exists(self.faiss_path):
            # Load existing database
            self._db = FAISS.load_local(
                self.faiss_path,
                self.embedding_function,
                allow_dangerous_deserialization=True
            )
            # Add new documents
            self._db.add_documents(documents)
        else:
            # Create new database from documents
            self._db = FAISS.from_documents(documents, self.embedding_function)
        
        # Save the index
        self._db.save_local(self.faiss_path)
        print(f"Added {len(documents)} chunks to {self.faiss_path}")
        return len(documents)
    
    def clear(self):
        """Clear the existing database."""
        if os.path.exists(self.faiss_path):
            import shutil
            shutil.rmtree(self.faiss_path)
            print(f"Cleared database at {self.faiss_path}")
        self._db = None

    def query(self, query_text: str, k=3):
        """Query the database for relevant documents."""
        db = self.get_db()
        if db is None:
            return []
        results = db.similarity_search_with_relevance_scores(query_text, k=k)
        return results
