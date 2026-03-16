import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from models.cnn_model import build_cnn_model
from utils.preprocessing import load_training_data, load_validation_data, get_class_labels
import tensorflow as tf


def train_model(train_dir, val_dir, epochs=25, batch_size=32, results_dir='results'):
    train_generator = load_training_data(train_dir, batch_size)
    val_generator = load_validation_data(val_dir, batch_size)
    
    num_classes = len(train_generator.class_indices)
    
    model = build_cnn_model(num_classes=num_classes)
    
    model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        verbose=1
    )
    
    model_path = os.path.join(results_dir, 'wheat_disease_model.h5')
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    # Save class indices to JSON file for loading in inference
    class_indices = train_generator.class_indices
    class_indices_path = os.path.join(results_dir, 'class_indices.json')
    with open(class_indices_path, 'w') as f:
        json.dump(class_indices, f)
    print(f"Class indices saved to {class_indices_path}")
    
    return model, class_indices


if __name__ == "__main__":
    train_dir = 'dataset/train'
    val_dir = 'dataset/val'
    results_dir = 'results'
    
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    model, class_indices = train_model(train_dir, val_dir, epochs=25, batch_size=32, results_dir=results_dir)
    print("Training completed successfully!")
