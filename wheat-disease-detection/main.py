import os
import sys
import json
from training.train import train_model
from evaluation.evaluate import evaluate_model
from inference.predict import predict_disease, batch_predict
from utils.output_formatter import format_prediction_output, format_batch_output


def load_class_names_from_indices(results_dir='results'):
    """
    Load class names from the saved class indices JSON file.
    The file is created during training and contains the mapping from class names to indices.
    
    Args:
        results_dir (str): Directory where class_indices.json is saved
        
    Returns:
        list: Ordered list of class names matching the model's training classes
    """
    class_indices_path = os.path.join(results_dir, 'class_indices.json')
    
    if not os.path.exists(class_indices_path):
        print(f"Warning: class_indices.json not found at {class_indices_path}")
        print("Using default class names. Please train the model to save correct mappings.")
        return ['Healthy', 'Leaf Rust', 'Black Rust']
    
    try:
        with open(class_indices_path, 'r') as f:
            class_indices = json.load(f)
        
        # Create ordered list of class names by sorting by index value
        # class_indices is {class_name: index}, we need to reverse it to [class_names by index]
        class_names = [''] * len(class_indices)
        for class_name, index in class_indices.items():
            class_names[index] = class_name
        
        print(f"Loaded {len(class_names)} classes from training: {class_names}")
        return class_names
    
    except Exception as e:
        print(f"Error loading class_indices.json: {e}")
        print("Using default class names.")
        return ['Healthy', 'Leaf Rust', 'Black Rust']


def setup_directories():
    if not os.path.exists('results'):
        os.makedirs('results')
    if not os.path.exists('dataset/train'):
        os.makedirs('dataset/train')
    if not os.path.exists('dataset/val'):
        os.makedirs('dataset/val')
    if not os.path.exists('dataset/test'):
        os.makedirs('dataset/test')


def run_training():
    print("=" * 50)
    print("Starting Model Training...")
    print("=" * 50)
    
    train_dir = 'dataset/train'
    val_dir = 'dataset/val'
    results_dir = 'results'
    
    if not os.path.exists(train_dir) or not os.listdir(train_dir):
        print(f"Training directory {train_dir} is empty or does not exist.")
        print("Please add training data in subdirectories organized by disease class.")
        return None
    
    model, class_indices = train_model(train_dir, val_dir, epochs=25, batch_size=32, results_dir=results_dir)
    print("Training completed successfully!")
    
    return class_indices


def run_evaluation():
    print("\n" + "=" * 50)
    print("Starting Model Evaluation...")
    print("=" * 50)
    
    model_path = 'results/wheat_disease_model.h5'
    test_dir = 'dataset/test'
    results_dir = 'results'
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        print("Please train the model first.")
        return None
    
    if not os.path.exists(test_dir) or not os.listdir(test_dir):
        print(f"Test directory {test_dir} is empty or does not exist.")
        print("Please add test data in subdirectories organized by disease class.")
        return None
    
    results = evaluate_model(model_path, test_dir, results_dir)
    print("Evaluation completed successfully!")
    
    return results


def run_prediction(image_path=None, batch_dir=None):
    print("\n" + "=" * 50)
    print("Starting Prediction...")
    print("=" * 50)
    
    model_path = 'results/wheat_disease_model.h5'
    results_dir = 'results'
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        print("Please train the model first.")
        return None
    
    # Load class names from the trained model's class indices
    class_names = load_class_names_from_indices(results_dir)
    
    if image_path and os.path.exists(image_path):
        print(f"\nPredicting for image: {image_path}")
        result = predict_disease(image_path, model_path, class_names, results_dir)
        
        # Display structured output
        formatted_output = format_prediction_output(result, class_names)
        print(formatted_output)
        
        return result
    
    elif batch_dir and os.path.exists(batch_dir):
        print(f"\nBatch predicting from directory: {batch_dir}")
        results = batch_predict(batch_dir, model_path, class_names, results_dir)
        
        # Display structured batch output
        formatted_output = format_batch_output(results, class_names)
        print(formatted_output)
        
        return results
    
    else:
        print("Please provide a valid image path or batch directory for prediction.")
        return None


def main():
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 10 + "Wheat Disease Detection System" + " " * 8 + "║")
    print("║" + " " * 14 + "CNN + Grad-CAM Analysis" + " " * 12 + "║")
    print("╚" + "=" * 48 + "╝")
    
    setup_directories()
    
    print("\nAvailable Options:")
    print("1. Train Model")
    print("2. Evaluate Model")
    print("3. Predict Disease")
    print("4. Run Full Pipeline (Train -> Evaluate -> Predict)")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == '1':
        run_training()
    
    elif choice == '2':
        run_evaluation()
    
    elif choice == '3':
        image_path = input("Enter image path for prediction: ").strip()
        if image_path:
            run_prediction(image_path=image_path)
        else:
            batch_dir = input("Or enter batch directory path: ").strip()
            if batch_dir:
                run_prediction(batch_dir=batch_dir)
    
    elif choice == '4':
        class_indices = run_training()
        if class_indices:
            run_evaluation()
            print("\nFor prediction, use option 3 or run predict.py directly")
    
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
    
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
