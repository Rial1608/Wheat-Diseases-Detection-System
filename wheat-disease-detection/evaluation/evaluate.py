import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tensorflow as tf
from tensorflow.keras.models import load_model
from utils.preprocessing import load_test_data
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def evaluate_model(model_path, test_dir, results_dir='results'):
    model = load_model(model_path)
    
    test_generator = load_test_data(test_dir, batch_size=32)
    
    predictions = model.predict(test_generator)
    predicted_classes = np.argmax(predictions, axis=1)
    true_classes = test_generator.classes
    
    accuracy = accuracy_score(true_classes, predicted_classes)
    print(f"Accuracy: {accuracy:.4f}")
    
    class_names = list(test_generator.class_indices.keys())
    
    print("\nClassification Report:")
    print(classification_report(true_classes, predicted_classes, target_names=class_names))
    
    cm = confusion_matrix(true_classes, predicted_classes)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    cm_path = os.path.join(results_dir, 'confusion_matrix.png')
    plt.savefig(cm_path)
    plt.close()
    
    print(f"\nConfusion Matrix saved to {cm_path}")
    
    return {
        'accuracy': accuracy,
        'confusion_matrix': cm,
        'class_names': class_names,
        'predictions': predictions,
        'true_classes': true_classes,
        'predicted_classes': predicted_classes
    }


if __name__ == "__main__":
    model_path = 'results/wheat_disease_model.h5'
    test_dir = 'dataset/test'
    results_dir = 'results'
    
    if os.path.exists(model_path):
        results = evaluate_model(model_path, test_dir, results_dir)
        print("Evaluation completed successfully!")
    else:
        print(f"Model not found at {model_path}")
