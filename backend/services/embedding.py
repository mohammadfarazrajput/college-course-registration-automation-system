"""
Embedding Service using Google Gemini
Handles text embeddings for vector store
"""

import os
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings


class EmbeddingService:
    """Singleton embedding service"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Gemini embeddings"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=api_key
        )
        print("✅ Gemini Embeddings initialized")
    
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text"""
        return self.embeddings.embed_query(text)
    
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed multiple texts"""
        return self.embeddings.embed_documents(texts)


# Singleton instance
embedding_service = EmbeddingService()