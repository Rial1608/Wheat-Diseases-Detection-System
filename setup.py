#!/usr/bin/env python
"""
Wheat Disease Detection Web Application - Setup Script
Initializes the application environment and checks prerequisites.
"""

import os
import sys
import json
from pathlib import Path

def check_prerequisites():
    """Check if all prerequisites are installed"""
    print("\n" + "="*60)
    print("🌾 WHEAT DISEASE DETECTION SYSTEM - SETUP CHECK")
    print("="*60 + "\n")
    
    prerequisites = {
        'Python 3.8+': sys.version.split()[0],
        'Flask': None,
        'TensorFlow': None,
        'NumPy': None,
        'OpenCV': None,
        'Pandas': None,
    }
    
    # Check Python
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Try importing packages
    packages_to_check = [
        ('flask', 'Flask'),
        ('tensorflow', 'TensorFlow'),
        ('numpy', 'NumPy'),
        ('cv2', 'OpenCV'),
        ('reportlab', 'ReportLab'),
        ('scipy', 'SciPy'),
    ]
    
    missing_packages = []
    
    for module_name, package_name in packages_to_check:
        try:
            __import__(module_name)
            print(f"✓ {package_name} is installed")
        except ImportError:
            print(f"✗ {package_name} is NOT installed")
            missing_packages.append(package_name)
    
    return missing_packages


def check_directory_structure():
    """Check if all required directories and files exist"""
    print("\n" + "-"*60)
    print("Checking directory structure...")
    print("-"*60 + "\n")
    
    base_dir = Path(__file__).parent.absolute()
    
    required_structure = {
        'templates': ['index.html', 'results.html', 'dashboard.html', '404.html'],
        'static/css': ['style.css'],
        'static/js': ['upload.js', 'results.js', 'dashboard.js'],
        'utils': ['infection_severity.py', 'disease_knowledge.py', 'pdf_generator.py', '__init__.py'],
        'wheat-disease-detection/results': ['wheat_disease_model.h5'],
        'wheat-disease-detection/utils': ['gradcam.py', 'preprocessing.py', 'visualize.py'],
    }
    
    all_good = True
    
    for directory, files in required_structure.items():
        dir_path = base_dir / directory
        
        # Check if directory exists
        if dir_path.exists():
            print(f"✓ Directory exists: {directory}/")
        else:
            print(f"✗ Directory missing: {directory}/")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  → Created: {directory}/")
        
        # Check if files exist
        for file in files:
            file_path = dir_path / file
            if file_path.exists():
                print(f"  ✓ {file}")
            else:
                print(f"  ✗ {file} - MISSING")
                all_good = False
    
    return all_good


def create_required_folders():
    """Create runtime folders if they don't exist"""
    print("\n" + "-"*60)
    print("Creating runtime directories...")
    print("-"*60 + "\n")
    
    base_dir = Path(__file__).parent.absolute()
    
    runtime_folders = [
        'uploads',
        'static/results',
        'results',
    ]
    
    for folder in runtime_folders:
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Ensuring directory exists: {folder}/")


def check_model_file():
    """Check if the trained model file exists"""
    print("\n" + "-"*60)
    print("Checking trained model...")
    print("-"*60 + "\n")
    
    base_dir = Path(__file__).parent.absolute()
    model_path = base_dir / 'wheat-disease-detection' / 'results' / 'wheat_disease_model.h5'
    
    if model_path.exists():
        model_size = model_path.stat().st_size / (1024 * 1024)  # Size in MB
        print(f"✓ Model file found: wheat_disease_model.h5")
        print(f"  → Size: {model_size:.2f} MB")
        return True
    else:
        print(f"✗ Model file NOT found: wheat_disease_model.h5")
        print(f"  → Path: {model_path}")
        print(f"  → Please ensure the trained model is in the correct location")
        return False


def create_app_config():
    """Create app configuration checklist"""
    print("\n" + "="*60)
    print("Application Configuration")
    print("="*60 + "\n")
    
    config = {
        'Flask Secret Key': 'wheat_disease_detection_secret_key_2024',
        'Max Upload Size': '16 MB',
        'Server Port': '5000',
        'Server Host': '0.0.0.0',
        'Debug Mode': 'False (change in app.py if needed)',
        'Database': 'Session-based (in-memory)',
    }
    
    for key, value in config.items():
        print(f"  • {key}: {value}")


def print_startup_instructions():
    """Print startup instructions"""
    print("\n" + "="*60)
    print("🚀 READY TO START THE APPLICATION")
    print("="*60 + "\n")
    
    print("Follow these steps to run the application:\n")
    
    print("1. Activate virtual environment:")
    print("   Windows:  venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate\n")
    
    print("2. Start the Flask server:")
    print("   python app.py\n")
    
    print("3. Open in browser:")
    print("   http://localhost:5000\n")
    
    print("="*60)
    print("Features available:")
    print("="*60)
    print("  / ..................... Upload page")
    print("  /results ............... Prediction results")
    print("  /dashboard ............. Analytics dashboard")
    print("  /api/predict ........... Disease prediction API")
    print("  /api/dashboard-data .... Dashboard statistics API")
    print("  /api/download-report ... PDF report generation")
    print("="*60 + "\n")


def main():
    """Main setup execution"""
    try:
        # Check prerequisites
        missing = check_prerequisites()
        
        # Check directory structure
        structure_ok = check_directory_structure()
        
        # Create required folders
        create_required_folders()
        
        # Check model file
        model_ok = check_model_file()
        
        # Create app config
        create_app_config()
        
        # Print startup instructions
        print_startup_instructions()
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60 + "\n")
        
        if missing:
            print(f"⚠️  Missing packages ({len(missing)}):")
            for pkg in missing:
                print(f"   • {pkg}")
            print(f"\nInstall them with: pip install -r requirements.txt\n")
        else:
            print("✓ All packages are installed\n")
        
        if not structure_ok:
            print("⚠️  Some project files are missing. Check the output above.\n")
        else:
            print("✓ All project files are present\n")
        
        if not model_ok:
            print("⚠️  Trained model file is missing!")
            print("   The application will not work without the model.\n")
        else:
            print("✓ Trained model file is present\n")
        
        if missing or not structure_ok or not model_ok:
            print("Please resolve the above issues before running the application.\n")
            return 1
        else:
            print("✓✓✓ Application is ready to launch! ✓✓✓\n")
            return 0
            
    except Exception as e:
        print(f"\n✗ Error during setup: {str(e)}")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
