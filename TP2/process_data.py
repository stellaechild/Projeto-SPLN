#!/usr/bin/env python3
import json
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import Counter
from typing import List, Dict, Tuple
import numpy as np

class DataProcessor:
    def __init__(self):
        self.data_dir = Path("data")
        self.ns = {
            'oai': 'http://www.openarchives.org/OAI/2.0/',
            'dim': 'http://www.dspace.org/xmlns/dspace/dim'
        }
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        # Removing extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text).strip()
        # Converting to lowercase
        return text.lower()
    
    def extract_metadata(self, record: ET.Element) -> Dict:
        """Extract relevant metadata from a record."""
        metadata = {}
        
        # Finding all fields in DSpace Intermediate Metadata format
        fields = record.findall('.//dim:field', self.ns)
        
        for field in fields:
            mdschema = field.get('mdschema', '')
            element = field.get('element', '')
            qualifier = field.get('qualifier', '')
            
            key = f"{mdschema}.{element}"
            if qualifier:
                key += f".{qualifier}"
                
            value = self.clean_text(field.text)
            
            if key in metadata:
                if isinstance(metadata[key], list):
                    metadata[key].append(value)
                else:
                    metadata[key] = [metadata[key], value]
            else:
                metadata[key] = value
                
        return metadata
    
    def xml_to_json(self, collection: str = "col_1822_21316") -> List[Dict]:
        """Convert XML data to JSON format."""
        xml_file = self.data_dir / f"{collection}_data.xml"
        if not xml_file.exists():
            raise FileNotFoundError(f"XML file not found: {xml_file}")
            
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        documents = []
        for record in root.findall('.//oai:record', self.ns):
            metadata = self.extract_metadata(record)
            if metadata:  
                documents.append(metadata)
                
        # Saving to JSON
        json_file = self.data_dir / f"{collection}_processed.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=2)
            
        return documents
    
    def guess_similarity(self, doc1: Dict, doc2: Dict) -> float:
        """
        Calculate similarity between two documents using various heuristics.
        Returns a similarity score between 0 and 1.
        """
        score = 0.0
        weights = {
            'keywords': 0.4,
            'subject': 0.3,
            'collection': 0.3
        }
        
        # Comparing keywords
        keywords1 = set(doc1.get('dc.subject', '').split()) if isinstance(doc1.get('dc.subject', ''), str) else set()
        keywords2 = set(doc2.get('dc.subject', '').split()) if isinstance(doc2.get('dc.subject', ''), str) else set()
        
        if keywords1 and keywords2:
            keyword_sim = len(keywords1 & keywords2) / max(len(keywords1 | keywords2), 1)
            score += weights['keywords'] * keyword_sim
            
        # Comparing subjects (UDC and FOS)
        subjects1 = set(str(doc1.get('dc.subject.udc', '')).split() + str(doc1.get('dc.subject.fos', '')).split())
        subjects2 = set(str(doc2.get('dc.subject.udc', '')).split() + str(doc2.get('dc.subject.fos', '')).split())
        
        if subjects1 and subjects2:
            subject_sim = len(subjects1 & subjects2) / max(len(subjects1 | subjects2), 1)
            score += weights['subject'] * subject_sim
            
        # Comparing collections
        col1 = set(str(doc1.get('dc.relation.ispartof', '')).split())
        col2 = set(str(doc2.get('dc.relation.ispartof', '')).split())
        
        if col1 and col2:
            col_sim = len(col1 & col2) / max(len(col1 | col2), 1)
            score += weights['collection'] * col_sim
            
        return score
    
    def create_training_collection(self, documents: List[Dict], sample_size: int = 1000) -> List[List]:
        """Create training collection of document pairs with similarity scores."""
        training_data = []
        
        # Random pairs
        indices = np.random.choice(len(documents), min(sample_size * 2, len(documents)), replace=False)
        
        for i in range(0, len(indices) - 1, 2):
            doc1 = documents[indices[i]]
            doc2 = documents[indices[i + 1]]
            
            abstract1 = doc1.get('dc.description.abstract', '')
            abstract2 = doc2.get('dc.description.abstract', '')
            
            if abstract1 and abstract2: 
                sim_score = self.guess_similarity(doc1, doc2)
                # Ensure consistent data structure: always use a list with two elements and a score
                training_data.append([abstract1, abstract2, sim_score])
                
        # Saving training data
        train_file = self.data_dir / "training_data.json"
        with open(train_file, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, ensure_ascii=False, indent=2)
            
        return training_data

if __name__ == "__main__":
    processor = DataProcessor()
    documents = processor.xml_to_json()
    training_data = processor.create_training_collection(documents)
    print(f"Created training collection with {len(training_data)} document pairs")
