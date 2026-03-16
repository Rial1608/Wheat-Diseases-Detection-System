#!/usr/bin/env python
"""
Project Setup Verification Script
Checks if all dependencies are installed and working
"""

import sys
import os

print("\n" + "="*70)
print("WHEAT DISEASE DETECTION - ENVIRONMENT VERIFICATION")
print("="*70 + "\n")

# Check Python version
print("[Python Version]")
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"  Version: {python_version}")
print(f"  Executable: {sys.executable}")
print()

# Check virtual environment
print("[Virtual Environment]")
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
if in_venv:
    print(f"  ✓ Running in virtual environment: {sys.prefix}")
else:
    print("  ⚠ NOT in virtual environment (may cause issues)")
print()

# Check required packages
print("[Required Packages]")
packages = {
    'flask': 'Flask',
    'werkzeug': 'Werkzeug',
    'numpy': 'NumPy',
    'cv2': 'OpenCV',
    'PIL': 'Pillow',
    'scipy': 'SciPy',
    'sklearn': 'scikit-learn',
    'reportlab': 'ReportLab',
    'matplotlib': 'Matplotlib',
}

all_ok = True
for module, name in packages.items():
    try:
        exec(f"import {module}")
        print(f"  ✓ {name}")
    except ImportError:
        print(f"  ✗ {name} - NOT INSTALLED")
        all_ok = False

print()

# Check TensorFlow (optional but recommended)
print("[Optional Packages]")
try:
    import tensorflow as tf
    print(f"  ✓ TensorFlow {tf.__version__}")
except ImportError:
    print("  ⚠ TensorFlow not installed (GPU acceleration won't work)")

print()

# Check project structure
print("[Project Structure]")
required_dirs = ['templates', 'static', 'uploads', 'wheat-disease-detection', '.venv1']
for directory in required_dirs:
    if os.path.exists(directory):
        print(f"  ✓ {directory}/")
    else:
        print(f"  ✗ {directory}/ - MISSING")

print()

# Check important files
print("[Important Files]")
required_files = ['app.py', 'requirements.txt', 'templates/index.html']
for file in required_files:
    if os.path.exists(file):
        print(f"  ✓ {file}")
    else:
        print(f"  ✗ {file} - MISSING")

print()

# Summary
print("="*70)
if all_ok:
    print("✓ All required packages are installed!")
    print("\nYou can now run the application:")
    print("  Windows: run_app.bat")
    print("  Mac/Linux: bash run_app.sh")
else:
    print("✗ Some packages are missing. Install them with:")
    print("\n  .venv1\\Scripts\\activate")
    print("  pip install -r requirements.txt")

print("="*70 + "\n")
