#!/usr/bin/env python3
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader
import torch

class ModelTrainer:
    def __init__(self):
        self.data_dir = Path("data")
        self.model_dir = Path("models")
        self.model_dir.mkdir(exist_ok=True)
        
        # Initialize the base model
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        
    def load_training_data(self):
        """Load the training data created by the DataProcessor."""
        train_file = self.data_dir / "training_data.json"
        if not train_file.exists():
            raise FileNotFoundError(f"Training data not found: {train_file}")
            
        with open(train_file, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def prepare_training_examples(self, training_data):
        """Convert training data into InputExample format."""
        train_examples = []
        
        for item in training_data:
            # Each item is [abstracts1_list, abstracts2_list, similarity]
            if not isinstance(item, list) or len(item) != 3:
                print(f"Skipping invalid item: {item}")
                continue
                
            abstracts1_list, abstracts2_list, similarity = item
            
            # Create training examples using the first abstract from each list
            # (assuming the first one is in the main language)
            if abstracts1_list and abstracts2_list:
                abstract1 = abstracts1_list[0] if isinstance(abstracts1_list, list) else abstracts1_list
                abstract2 = abstracts2_list[0] if isinstance(abstracts2_list, list) else abstracts2_list
                
                train_examples.append(
                    InputExample(
                        texts=[abstract1, abstract2],
                        label=float(similarity)
                    )
                )
            
        if not train_examples:
            raise ValueError("No valid training examples could be created!")
            
        return train_examples
        
    def train(self, train_examples, epochs=3, batch_size=16):
        """Train the model on the provided examples."""
        if not train_examples:
            raise ValueError("No valid training examples found!")
            
        train_dataloader = DataLoader(
            train_examples,
            shuffle=True,
            batch_size=batch_size
        )
        
        # Use cosine similarity loss
        train_loss = losses.CosineSimilarityLoss(self.model)
        
        # Train the model
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=epochs,
            warmup_steps=100,
            show_progress_bar=True
        )
        
        # Save the model
        model_path = self.model_dir / "repositorium_similarity_model"
        self.model.save(str(model_path))
        print(f"Model saved to {model_path}")
        
    def run_training(self, epochs=3, batch_size=16):
        """Run the complete training pipeline."""
        print("Loading training data...")
        training_data = self.load_training_data()
        
        print("Preparing training examples...")
        train_examples = self.prepare_training_examples(training_data)
        
        print(f"Starting training with {len(train_examples)} examples...")
        self.train(train_examples, epochs=epochs, batch_size=batch_size)
        
if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run_training() 