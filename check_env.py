#!/usr/bin/env python
"""
Wheat Disease Detection System - Environment & Dependency Checker
Validates Python environment, TensorFlow installation, and model loading
"""

import sys
import os
import subprocess
from pathlib import Path

class EnvironmentChecker:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = []
        
    def print_header(self):
        print("\n" + "="*70)
        print("🌾 WHEAT DISEASE DETECTION SYSTEM - ENVIRONMENT CHECK")
        print("="*70 + "\n")
    
    def print_section(self, title):
        print(f"\n[{title}]")
        print("-" * 70)
    
    def check_python_version(self):
        self.print_section("Python Version Check")
        
        version_info = sys.version_info
        version_string = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
        
        print(f"Python Version: {version_string}")
        print(f"Executable: {sys.executable}")
        
        # TensorFlow 2.15 requires Python 3.9-3.12
        if version_info.major == 3 and 9 <= version_info.minor <= 12:
            print("✓ Python version is compatible with TensorFlow")
            self.checks_passed += 1
            return True
        elif version_info.major == 3 and version_info.minor < 9:
            print("✗ Python 3.9 or higher required for TensorFlow")
            self.checks_failed += 1
            self.warnings.append("Python version too old. Need Python 3.9+")
            return False
        else:
            print(f"⚠ Python {version_string} may have TensorFlow compatibility issues")
            print("  TensorFlow 2.15 is optimized for Python 3.9-3.12")
            self.warnings.append(f"Python {version_string} may not have TensorFlow wheel packages")
            self.checks_passed += 1
            return True
    
    def check_tensorflow(self):
        self.print_section("TensorFlow Installation Check")
        
        try:
            import tensorflow as tf
            print(f"✓ TensorFlow {tf.__version__} is installed")
            print(f"  Location: {tf.__file__}")
            self.checks_passed += 1
            return True
        except ImportError as e:
            print(f"✗ TensorFlow not found: {str(e)}")
            self.checks_failed += 1
            return False
    
    def check_required_packages(self):
        self.print_section("Required Packages Check")
        
        packages = {
            'flask': 'Flask',
            'numpy': 'NumPy',
            'cv2': 'OpenCV',
            'PIL': 'Pillow',
            'scipy': 'SciPy',
            'matplotlib': 'Matplotlib',
            'reportlab': 'ReportLab',
            'sklearn': 'scikit-learn',
            'werkzeug': 'Werkzeug'
        }
        
        missing = []
        for module, name in packages.items():
            try:
                __import__(module)
                print(f"✓ {name} is installed")
                self.checks_passed += 1
            except ImportError:
                print(f"✗ {name} is missing")
                missing.append(name)
                self.checks_failed += 1
        
        return len(missing) == 0, missing
    
    def check_model_file(self):
        self.print_section("Model File Check")
        
        model_path = Path(__file__).parent / 'wheat-disease-detection' / 'results' / 'wheat_disease_model.h5'
        
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"✓ Model file found: {model_path.name}")
            print(f"  Size: {size_mb:.2f} MB")
            self.checks_passed += 1
            return True
        else:
            print(f"✗ Model file not found at:")
            print(f"  {model_path}")
            self.checks_failed += 1
            return False
    
    def check_directories(self):
        self.print_section("Directory Structure Check")
        
        base_dir = Path(__file__).parent
        required_dirs = [
            'templates',
            'static/css',
            'static/js',
            'utils',
            'wheat-disease-detection'
        ]
        
        all_exist = True
        for dir_name in required_dirs:
            dir_path = base_dir / dir_name
            if dir_path.exists():
                print(f"✓ {dir_name}/")
                self.checks_passed += 1
            else:
                print(f"✗ {dir_name}/ - MISSING")
                self.checks_failed += 1
                all_exist = False
        
        # Create runtime directories if needed
        runtime_dirs = ['uploads', 'static/results', 'results']
        for dir_name in runtime_dirs:
            dir_path = base_dir / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
        
        return all_exist
    
    def suggest_fixes(self):
        self.print_section("Recommended Actions")
        
        if not self.checks_passed > 0:
            print("One or more critical checks failed.")
        
        if self.checks_failed > 0:
            print("\nTo fix the issues:")
            print("\n1. Install all dependencies:")
            print("   pip install -r requirements.txt")
            print("\n2. For TensorFlow on Python 3.13+:")
            print("   pip install --upgrade tensorflow")
            print("   OR")
            print("   pip install tensorflow-cpu")
            print("\n3. Verify installation:")
            print("   python -c \"import tensorflow; print(tensorflow.__version__)\"")
    
    def run_all_checks(self):
        self.print_header()
        
        self.check_python_version()
        self.check_required_packages()
        self.check_tensorflow()
        self.check_model_file()
        self.check_directories()
        
        # Summary
        self.print_section("Summary")
        print(f"Passed: {self.checks_passed}")
        print(f"Failed: {self.checks_failed}")
        
        if self.warnings:
            print(f"\nWarnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        self.suggest_fixes()
        
        # Final status
        print("\n" + "="*70)
        if self.checks_failed == 0:
            print("✓✓✓ All checks passed! Ready to run.")
            print("="*70 + "\n")
            return True
        else:
            print("✗✗✗ Some checks failed. See recommendations above.")
            print("="*70 + "\n")
            return False

if __name__ == '__main__':
    checker = EnvironmentChecker()
    success = checker.run_all_checks()
    sys.exit(0 if success else 1)
