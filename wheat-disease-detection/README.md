# Wheat Disease Detection System

A robust deep learning project for classifying wheat leaf diseases using Convolutional Neural Networks (CNN) with Explainable AI (Grad-CAM) visualization.

## Features

✓ **CNN-based Image Classification** - 5-layer convolutional neural network for disease detection  
✓ **Grad-CAM Explainability** - Visualize which parts of the image influence predictions  
✓ **Data Augmentation** - Rotation, shifts, flips, and zoom for improved model robustness  
✓ **Complete Pipeline** - Training, evaluation, and inference modules  
✓ **Production-Ready** - Modular, professional ML project structure  

## Project Structure

```
wheat-disease-detection/
├── models/
│   └── cnn_model.py                 # CNN architecture
├── utils/
│   ├── preprocessing.py             # Data loading and augmentation
│   ├── gradcam.py                   # Grad-CAM implementation
│   └── visualize.py                 # Heatmap visualization
├── training/
│   └── train.py                     # Model training pipeline
├── evaluation/
│   └── evaluate.py                  # Model evaluation and metrics
├── inference/
│   └── predict.py                   # Inference and predictions
├── dataset/
│   ├── train/                       # Training images by disease class
│   ├── val/                         # Validation images
│   └── test/                        # Test images
├── results/                         # Output models and visualizations
├── main.py                          # Interactive main pipeline
├── requirements.txt                 # Dependencies
└── README.md                        # This file
```

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rial1608/Wheat-Diseases-Detection-System.git
   cd wheat-disease-detection
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Prepare Your Data

Organize images in `dataset/` folder by disease class:

```
dataset/
├── train/
│   ├── Healthy/
│   ├── Disease1/
│   └── Disease2/
├── val/
│   ├── Healthy/
│   ├── Disease1/
│   └── Disease2/
└── test/
    ├── Healthy/
    ├── Disease1/
    └── Disease2/
```

### 2. Train the Model

```bash
python main.py
# Or run directly:
python training/train.py
```

The trained model will be saved to `results/wheat_disease_model.h5`

### 3. Evaluate the Model

```bash
python evaluation/evaluate.py
```

Generates:
- Confusion matrix visualization
- Classification report
- Accuracy metrics

### 4. Make Predictions

Single image:
```bash
python inference/predict.py path/to/image.jpg
```

Batch predictions:
```bash
python inference/predict.py --batch path/to/images/
```

## Model Architecture

- **Input:** 224×224 RGB images
- **Conv Layers:** 5 convolutional blocks with ReLU activation
- **Pooling:** MaxPooling (2×2) after each conv layer
- **Dense Layers:** 512 → 256 neurons with 0.5 Dropout
- **Output:** Softmax activation for multi-class classification

## Grad-CAM Explainability

Grad-CAM (Gradient-weighted Class Activation Mapping) highlights regions that influenced the model's prediction:

```python
from utils.gradcam import GradCAM
from inference.predict import predict_disease

result = predict_disease('image.jpg', 'results/wheat_disease_model.h5', 
                        ['Healthy', 'Disease1', 'Disease2'])
# Outputs visualization with Grad-CAM heatmap
```

## Model Training Details

- **Optimizer:** Adam
- **Loss:** Categorical Crossentropy
- **Metrics:** Accuracy
- **Image Size:** 224×224
- **Augmentation:** Rotation 40°, Width/Height shift 0.2, Horizontal flip, Zoom 0.2

## Results

- Saved model: `results/wheat_disease_model.h5`
- Confusion matrix: `results/confusion_matrix.png`
- Predictions: `results/prediction_*_gradcam.png`

## Dependencies

- TensorFlow 2.12+
- OpenCV 4.8+
- NumPy 1.24+
- Matplotlib 3.7+
- Scikit-learn 1.3+
- Seaborn 0.12+
- Pillow 10.0+

See `requirements.txt` for exact versions.

## File Sizes and Performance

- Model size: ~50-100 MB (trained state)
- Training time: 15-45 minutes (GPU recommended)
- Inference time: <1 second per image

## License

MIT License

## Author

Rial1608

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please create an issue on GitHub.

## References

- TensorFlow/Keras Documentation: https://www.tensorflow.org/
- Grad-CAM Paper: https://arxiv.org/abs/1610.02055
- OpenCV: https://opencv.org/
