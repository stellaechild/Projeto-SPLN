#!/usr/bin/env python3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Tuple
import torch

class DocumentRetriever:
    def __init__(self):
        self.data_dir = Path("data")
        self.model_dir = Path("models")
        
        # Load the trained model
        model_path = self.model_dir / "repositorium_similarity_model"
        if model_path.exists():
            self.model = SentenceTransformer(str(model_path))
        else:
            # Fallback to base model if trained model doesn't exist
            self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("Warning: Using base model as trained model not found")
            
        # Load document collection
        self.documents = self.load_documents()
        
    def load_documents(self) -> List[Dict]:
        """Load the processed document collection."""
        json_file = list(self.data_dir.glob("*_processed.json"))[0]
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def encode_documents(self):
        """Encode all documents in the collection."""
        abstracts = [doc.get('dc.description.abstract', '') for doc in self.documents]
        return self.model.encode(abstracts, convert_to_tensor=True)
        
    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Retrieve the most relevant documents for a query.
        
        Args:
            query (str): The search query
            top_k (int): Number of documents to retrieve
            
        Returns:
            List of tuples containing (document, similarity_score)
        """
        # Encode the query
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        
        # Encode all documents (or load from cache)
        doc_embeddings = self.encode_documents()
        
        # Calculate similarities
        similarities = torch.nn.functional.cosine_similarity(
            query_embedding.unsqueeze(0),
            doc_embeddings
        )
        
        # Get top-k documents
        top_indices = torch.argsort(similarities, descending=True)[:top_k]
        
        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            score = similarities[idx].item()
            results.append((doc, score))
            
        return results
        
    def print_results(self, results: List[Tuple[Dict, float]]):
        """Print the retrieval results in a readable format."""
        print("\nSearch Results:")
        print("-" * 80)
        
        for i, (doc, score) in enumerate(results, 1):
            print(f"\n{i}. Score: {score:.4f}")
            print(f"Title: {doc.get('dc.title', 'No title')}")
            print(f"Authors: {doc.get('dc.contributor.author', 'No authors')}")
            print(f"Abstract: {doc.get('dc.description.abstract', 'No abstract')[:200]}...")
            print("-" * 80)
            
def main():
    retriever = DocumentRetriever()
    
    while True:
        query = input("\nEnter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break
            
        results = retriever.retrieve(query)
        retriever.print_results(results)
        
if __name__ == "__main__":
    main() 