import os
import json
import base64
import sys
import shutil
from datetime import datetime
from pathlib import Path
import importlib.util
from typing import Tuple, Optional, Dict, Any
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file, session
import numpy as np
import cv2

# Import configuration
from config import config

# ============================================
# SYSTEM INITIALIZATION & VALIDATION
# ============================================

print("\n" + "="*70)
print("🌾 WHEAT DISEASE DETECTION SYSTEM - INITIALIZING")
print("="*70)

# Check Python version
print(f"\n[Python Version Check]")
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"Python: {python_version}")
print(f"Executable: {sys.executable}")

if sys.version_info.major == 3 and 9 <= sys.version_info.minor <= 12:
    print("✓ Python version compatible with TensorFlow")
elif sys.version_info.major == 3 and sys.version_info.minor >= 13:
    print("⚠ Python 3.13+ detected - TensorFlow compatibility may vary")
else:
    print("⚠ Python < 3.9 detected - TensorFlow may not work")

# TensorFlow & Keras import with detailed error handling
print(f"\n[TensorFlow & Keras Check]")
TENSORFLOW_AVAILABLE = False
TF_ERROR = None

try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing import image
    TENSORFLOW_AVAILABLE = True
    print(f"✓ TensorFlow {tf.__version__} loaded successfully")
except ImportError as e:
    TF_ERROR = str(e)
    print(f"✗ TensorFlow import failed: {e}")
    print("  Note: TensorFlow requires Python 3.9-3.12 for wheels")
except Exception as e:
    TF_ERROR = str(e)
    print(f"✗ TensorFlow error: {e}")

# Disease utilities import (BEFORE adding wheat-disease-detection to sys.path)
print(f"\n[Disease Utilities Check]")
try:
    from utils.infection_severity import estimate_infection_severity
    from utils.pdf_generator import generate_pdf_report
    from utils.disease_knowledge import get_disease_info, get_treatment_recommendations
    print("✓ Disease utilities loaded successfully")
except ImportError as e:
    print(f"✗ Could not import disease utilities: {e}")

# Grad-CAM utilities import
print(f"\n[Grad-CAM Utilities Check]")
GRADCAM_AVAILABLE = False
GradCAM = None
save_heatmap_visualization = None

# Dynamically load gradcam module using importlib
try:
    gradcam_path = os.path.join(os.path.dirname(__file__), 'wheat-disease-detection', 'utils', 'gradcam.py')
    spec = importlib.util.spec_from_file_location("gradcam", gradcam_path)
    gradcam_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gradcam_module)
    GradCAM = gradcam_module.GradCAM
    
    # Load visualize module
    visualize_path = os.path.join(os.path.dirname(__file__), 'wheat-disease-detection', 'utils', 'visualize.py')
    spec_viz = importlib.util.spec_from_file_location("visualize", visualize_path)
    visualize_module = importlib.util.module_from_spec(spec_viz)
    spec_viz.loader.exec_module(visualize_module)
    save_heatmap_visualization = visualize_module.save_heatmap_visualization
    
    GRADCAM_AVAILABLE = True
    print("✓ Grad-CAM utilities loaded successfully")
except Exception as e:
    print(f"✗ Could not import Grad-CAM utilities: {e}")

# ============================================
# DATABASE & PATHS
# ============================================

print(f"\n[Paths & Directories Check]")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WHEAT_DIR = os.path.join(BASE_DIR, 'wheat-disease-detection')
MODEL_PATH = config.get_model_path()

print(f"Base Directory: {BASE_DIR}")
print(f"Model Path: {MODEL_PATH}")

if os.path.exists(WHEAT_DIR):
    print(f"✓ Wheat disease detection directory exists")
else:
    print(f"✗ Wheat disease detection directory NOT found")

if os.path.exists(MODEL_PATH):
    model_size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
    print(f"✓ Model file exists ({model_size_mb:.2f} MB)")
else:
    print(f"✗ Model file NOT found at {MODEL_PATH}")

# ============================================
# FLASK APP INITIALIZATION
# ============================================

print(f"\n[Flask Initialization]")
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config.from_object(config)
app.secret_key = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = config.get_upload_folder()
app.config['RESULTS_FOLDER'] = config.get_results_folder()
app.config['ALLOWED_EXTENSIONS'] = config.ALLOWED_EXTENSIONS

print(f"✓ Flask app configured")
print(f"✓ Upload folder: {app.config['UPLOAD_FOLDER']}")
print(f"✓ Environment: {'PRODUCTION' if not config.DEBUG else 'DEVELOPMENT'}")

# Model configuration
CLASS_NAMES = config.CLASS_NAMES
INPUT_SHAPE = config.INPUT_SHAPE

# ============================================
# MODEL LOADING
# ============================================

print(f"\n[Model Loading Check]")
MODEL = None
MODEL_READY = False

def validate_upload_path(upload_folder: str, filename: str) -> Optional[str]:
    """
    Validate that the file path stays within the upload folder.
    Prevents path traversal attacks.
    
    Args:
        upload_folder: The base upload directory
        filename: The filename to validate
        
    Returns:
        Safe filepath if valid, None otherwise
    """
    # Get absolute paths
    base_abs = os.path.abspath(upload_folder)
    file_abs = os.path.abspath(os.path.join(upload_folder, filename))
    
    # Ensure the file path is within the upload folder
    if not file_abs.startswith(base_abs):
        return None
    
    return file_abs

def load_model_once() -> bool:
    """Load the model once and cache in memory."""
    global MODEL, MODEL_READY
    
    if MODEL is not None:
        print("✓ Model already loaded in memory")
        return True
    
    if not TENSORFLOW_AVAILABLE:
        print("✗ Cannot load model: TensorFlow not available")
        print(f"  Error: {TF_ERROR}")
        print("  Fix: Install TensorFlow with: pip install tensorflow")
        return False
    
    if not os.path.exists(MODEL_PATH):
        print(f"✗ Model file not found: {MODEL_PATH}")
        return False
    
    try:
        print(f"Loading model from {MODEL_PATH}...")
        MODEL = load_model(MODEL_PATH)
        MODEL_READY = True
        print(f"✓ Model loaded successfully")
        print(f"  Model shape: {MODEL.input_shape}")
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        MODEL_READY = False
        return False

# Attempt initial model load
load_model_once()

# ============================================
# GLOBAL STATUS
# ============================================

print(f"\n[STARTUP STATUS SUMMARY]")
print(f"  TensorFlow Available: {'✓ YES' if TENSORFLOW_AVAILABLE else '✗ NO'}")
print(f"  Model Ready: {'✓ YES' if MODEL_READY else '✗ NO'}")
print(f"  Grad-CAM Available: {'✓ YES' if GRADCAM_AVAILABLE else '✗ NO'}")
print("\n" + "="*70)
print("Initialization complete!")
print("="*70 + "\n")

# Global data
prediction_history = []


def get_last_conv_layer_name(model) -> Optional[str]:
    """Find the last convolutional layer in the model"""
    for layer in reversed(model.layers):
        if 'conv' in layer.name.lower():
            return layer.name
    return None

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index() -> str:
    """Main upload page"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict() -> Tuple[Dict[str, Any], int]:
    """API endpoint for disease prediction"""
    try:
        # Check if TensorFlow is available
        if not TENSORFLOW_AVAILABLE:
            return jsonify({'error': 'Model service unavailable. TensorFlow not installed. Please fix environment.'}), 503
        
        # Check if model is loaded
        if MODEL is None or not MODEL_READY:
            return jsonify({'error': 'Model not loaded. Please install TensorFlow.'}), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'error': 'Invalid file type. Allowed: jpg, jpeg, png'}), 400
        
        # Save uploaded file with security validation
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        
        # Validate path to prevent directory traversal
        filepath = validate_upload_path(app.config['UPLOAD_FOLDER'], filename)
        if filepath is None:
            return jsonify({'error': 'Invalid filename'}), 400
            
        file.save(filepath)
        
        # Prepare image for prediction
        img = image.load_img(filepath, target_size=INPUT_SHAPE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        
        # Make prediction
        predictions = MODEL.predict(img_array, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = CLASS_NAMES[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])
        
        # Generate Grad-CAM heatmap (if available)
        heatmap = None
        output_filename = None
        severity_percentage = 0
        severity_level = "Unknown"
        
        # Default severity based on disease type and confidence
        if predicted_class.lower() == 'healthy':
            severity_percentage = 0
            severity_level = 'Healthy'
        else:
            # Estimate severity based on confidence if Grad-CAM not available
            severity_percentage = min(confidence * 100, 100)  # Use confidence as proxy
            if severity_percentage < 10:
                severity_level = 'Trace'
            elif severity_percentage < 20:
                severity_level = 'Low Infection'
            elif severity_percentage < 50:
                severity_level = 'Moderate Infection'
            else:
                severity_level = 'Severe Infection'
        
        if GRADCAM_AVAILABLE:
            try:
                last_conv_layer = get_last_conv_layer_name(MODEL)
                gradcam = GradCAM(MODEL, last_conv_layer)
                heatmap = gradcam.generate_heatmap(img_array)
                
                # Generate heatmap visualization
                original_image = cv2.imread(filepath)
                if original_image is None:
                    print(f"✗ Could not read original image from {filepath}")
                else:
                    output_filename = f"gradcam_{os.path.splitext(filename)[0]}.png"
                    output_path = os.path.join(app.config['RESULTS_FOLDER'], output_filename)
                    print(f"📊 Saving heatmap to: {output_path}")
                    print(f"   Original image shape: {original_image.shape}")
                    print(f"   Heatmap shape: {heatmap.shape}")
                    
                    save_heatmap_visualization(original_image, heatmap, predicted_class, confidence, output_path)
                    
                    # Verify file was created
                    if os.path.exists(output_path):
                        file_size = os.path.getsize(output_path)
                        print(f"✓ Heatmap created successfully ({file_size} bytes)")
                    else:
                        print(f"✗ Heatmap file was not created at {output_path}")
                        output_filename = None
                    
                    # Estimate infection severity using Grad-CAM heatmap
                    severity_percentage, severity_level = estimate_infection_severity(heatmap, predicted_class)
            except Exception as grad_error:
                print(f"✗ Grad-CAM generation failed: {grad_error}")
                import traceback
                traceback.print_exc()
                output_filename = None
                heatmap = None
        else:
            print("⚠ Grad-CAM not available, using confidence-based severity estimation")
        
        # Create result dictionary
        result = {
            'image_name': filename,
            'original_filename': file.filename,
            'predicted_disease': predicted_class,
            'confidence': confidence,
            'confidence_percentage': f"{confidence * 100:.1f}%",
            'severity_percentage': severity_percentage,
            'severity_level': severity_level,
            'all_predictions': {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))},
            'gradcam_image': output_filename if output_filename else None,
            'upload_path': filepath,
            'timestamp': datetime.now().isoformat(),
            'disease_info': get_disease_info(predicted_class),
            'treatment_recommendations': get_treatment_recommendations(predicted_class)
        }
        
        # Store in session for later use
        if 'predictions' not in session:
            session['predictions'] = []
        session['predictions'].append(result)
        session.modified = True
        
        # Add to prediction history
        prediction_history.append(result)
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    """Results page - shows last prediction"""
    if 'predictions' not in session or len(session['predictions']) == 0:
        return render_template('results.html', prediction=None)
    
    latest_prediction = session['predictions'][-1]
    return render_template('results.html', prediction=latest_prediction)

@app.route('/api/latest-prediction')
def get_latest_prediction():
    """Get the latest prediction data"""
    if 'predictions' not in session or len(session['predictions']) == 0:
        return jsonify({'error': 'No predictions yet'}), 404
    
    return jsonify(session['predictions'][-1]), 200

@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    if 'predictions' not in session:
        session['predictions'] = []
    
    predictions = session['predictions']
    return render_template('dashboard.html', predictions=predictions)

@app.route('/api/dashboard-data')
def get_dashboard_data():
    """Get analytics data for dashboard"""
    if 'predictions' not in session:
        session['predictions'] = []
    
    predictions = session['predictions']
    
    # Calculate statistics
    total_predictions = len(predictions)
    
    # Disease distribution
    disease_counts = {}
    for pred in predictions:
        disease = pred['predicted_disease']
        disease_counts[disease] = disease_counts.get(disease, 0) + 1
    
    # Healthy vs Infected
    healthy_count = disease_counts.get('Healthy', 0)
    infected_count = total_predictions - healthy_count
    
    # Average confidence by disease
    avg_confidence_by_disease = {}
    disease_predictions = {}
    for pred in predictions:
        disease = pred['predicted_disease']
        if disease not in disease_predictions:
            disease_predictions[disease] = []
        disease_predictions[disease].append(pred['confidence'])
    
    for disease, confidences in disease_predictions.items():
        avg_confidence_by_disease[disease] = np.mean(confidences)
    
    # Severity distribution
    severity_distribution = {}
    for pred in predictions:
        severity = pred['severity_level']
        severity_distribution[severity] = severity_distribution.get(severity, 0) + 1
    
    data = {
        'total_predictions': total_predictions,
        'disease_distribution': disease_counts,
        'healthy_count': healthy_count,
        'infected_count': infected_count,
        'average_confidence_by_disease': {k: float(v) for k, v in avg_confidence_by_disease.items()},
        'severity_distribution': severity_distribution,
        'recent_predictions': predictions[-10:] if len(predictions) > 10 else predictions
    }
    
    return jsonify(data), 200

@app.route('/api/download-report', methods=['POST'])
def download_report():
    """Generate and download PDF report"""
    try:
        if 'predictions' not in session or len(session['predictions']) == 0:
            return jsonify({'error': 'No predictions to report'}), 404
        
        prediction = session['predictions'][-1]
        
        # Get the uploaded image
        uploaded_image_path = prediction['upload_path']
        gradcam_image_path = os.path.join(app.config['RESULTS_FOLDER'], prediction['gradcam_image'])
        
        # Generate PDF
        pdf_path = generate_pdf_report(
            prediction=prediction,
            uploaded_image_path=uploaded_image_path,
            gradcam_image_path=gradcam_image_path,
            results_folder=app.config['RESULTS_FOLDER']
        )
        
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"wheat_disease_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    
    except Exception as e:
        print(f"Report generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/prediction-history')
def get_prediction_history():
    """Get all predictions from current session"""
    if 'predictions' not in session:
        return jsonify([]), 200
    
    return jsonify(session['predictions']), 200

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear prediction history"""
    session['predictions'] = []
    session.modified = True
    return jsonify({'message': 'History cleared'}), 200

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'tensorflow_available': TENSORFLOW_AVAILABLE,
        'model_ready': MODEL_READY,
        'gradcam_available': GRADCAM_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        'tensorflow_available': TENSORFLOW_AVAILABLE,
        'tensorflow_error': TF_ERROR,
        'model_ready': MODEL_READY,
        'model_path': MODEL_PATH,
        'model_exists': os.path.exists(MODEL_PATH),
        'gradcam_available': GRADCAM_AVAILABLE,
        'uploads_folder': app.config['UPLOAD_FOLDER'],
        'uploads_folder_exists': os.path.exists(app.config['UPLOAD_FOLDER']),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'timestamp': datetime.now().isoformat()
    }), 200

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌾 STARTING FLASK SERVER")
    print("="*70)
    print("Server will be available at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("="*70 + "\n")
    
    if not MODEL_READY:
        print("⚠ WARNING: Model not ready. Predictions will not work.")
        print("To fix this issue, run: python check_env.py")
        print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
