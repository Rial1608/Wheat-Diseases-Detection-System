import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2
from utils.gradcam import GradCAM
from utils.visualize import save_heatmap_visualization


def predict_disease(image_path, model_path, class_names, results_dir='results'):
    model = load_model(model_path)
    
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    
    predictions = model.predict(img_array, verbose=0)
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = class_names[predicted_class_idx]
    confidence = predictions[0][predicted_class_idx]
    
    # Find the last Conv2D layer for GradCAM
    last_conv_layer_name = None
    for layer in reversed(model.layers):
        if 'conv' in layer.name.lower():
            last_conv_layer_name = layer.name
            break
    
    if last_conv_layer_name is None:
        raise ValueError("No convolutional layer found in the model")
    
    gradcam = GradCAM(model, last_conv_layer_name)
    heatmap = gradcam.generate_heatmap(img_array)
    
    original_image = cv2.imread(image_path)
    
    output_filename = f"prediction_{os.path.basename(image_path).split('.')[0]}_gradcam.png"
    output_path = os.path.join(results_dir, output_filename)
    
    overlayed = save_heatmap_visualization(original_image, heatmap, predicted_class, confidence, output_path)
    
    # Get image name
    image_name = os.path.basename(image_path)
    
    return {
        'image': image_name,
        'predicted_class': predicted_class,
        'confidence': float(confidence),
        'all_predictions': predictions[0].tolist(),
        'heatmap': heatmap,
        'output_path': output_path
    }


def batch_predict(image_dir, model_path, class_names, results_dir='results'):
    results = []
    
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [f for f in os.listdir(image_dir) 
                   if os.path.splitext(f)[1].lower() in image_extensions]
    
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        try:
            result = predict_disease(image_path, model_path, class_names, results_dir)
            result['image'] = image_file
            results.append(result)
            print(f"Predicted {image_file}: {result['predicted_class']} ({result['confidence']:.2%})")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    return results


if __name__ == "__main__":
    model_path = 'results/wheat_disease_model.h5'
    class_names = ['Healthy', 'Disease1', 'Disease2']
    
    test_image = 'path/to/test/image.jpg'
    
    if os.path.exists(model_path):
        result = predict_disease(test_image, model_path, class_names)
        print(f"Predicted: {result['predicted_class']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Output saved: {result['output_path']}")
