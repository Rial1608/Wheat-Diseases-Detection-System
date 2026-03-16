#!/usr/bin/env python3
"""
TensorFlow Installation Fix Script for Wheat Disease Detection System

This script helps diagnose and fix TensorFlow installation issues,
particularly related to Python version compatibility.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

print("\n" + "="*70)
print("🌾 WHEAT DISEASE DETECTION - TENSORFLOW FIX SCRIPT")
print("="*70)

# ============================================
# STEP 1: CHECK PYTHON VERSION
# ============================================

print("\n[STEP 1] Checking Python Version")
print("-" * 70)
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"Current Python: {python_version}")
print(f"Python Executable: {sys.executable}")

PYTHON_MAJOR = sys.version_info.major
PYTHON_MINOR = sys.version_info.minor

if PYTHON_MAJOR == 3 and 9 <= PYTHON_MINOR <= 12:
    print("✓ Python version is compatible with TensorFlow")
    PYTHON_OK = True
elif PYTHON_MAJOR == 3 and PYTHON_MINOR >= 13:
    print(f"✗ Python {PYTHON_MAJOR}.{PYTHON_MINOR} is TOO NEW for TensorFlow")
    print("  TensorFlow requires Python 3.9-3.12")
    PYTHON_OK = False
else:
    print(f"✗ Python {PYTHON_MAJOR}.{PYTHON_MINOR} is TOO OLD for TensorFlow")
    print("  TensorFlow requires Python 3.9-3.12")
    PYTHON_OK = False

# ============================================
# STEP 2: CHECK TENSORFLOW
# ============================================

print("\n[STEP 2] Checking TensorFlow Installation")
print("-" * 70)

try:
    import tensorflow as tf
    print(f"✓ TensorFlow is installed (version {tf.__version__})")
    TENSORFLOW_OK = True
except ImportError as e:
    print(f"✗ TensorFlow is NOT installed")
    print(f"  Error: {e}")
    TENSORFLOW_OK = False

# ============================================
# STEP 3: CHECK VIRTUAL ENVIRONMENT
# ============================================

print("\n[STEP 3] Checking Virtual Environment")
print("-" * 70)

in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
if in_venv:
    print(f"✓ Virtual environment detected: {sys.prefix}")
    VENV_OK = True
else:
    print("✗ Not in a virtual environment")
    print("  It's recommended to use: python -m venv .venv")
    VENV_OK = False

# ============================================
# STEP 4: RECOMMENDATIONS
# ============================================

print("\n[STEP 4] Fix Recommendations")
print("-" * 70)

if TENSORFLOW_OK:
    print("✓ No action needed - TensorFlow is already installed!")

elif not PYTHON_OK and PYTHON_MINOR >= 13:
    print("\n❌ MAIN ISSUE: Python version is too new for TensorFlow")
    print("\nRECOMMENDED FIX OPTIONS:")
    print("\nOPTION 1: Downgrade Python (RECOMMENDED)")
    print("  The safest option is to use Python 3.11 with TensorFlow")
    print("  1. Install Python 3.11 from python.org")
    print("  2. Create a new virtual environment:")
    print("     python3.11 -m venv .venv")
    print("  3. Activate the environment:")
    if platform.system() == "Windows":
        print("     .venv\\Scripts\\activate")
    else:
        print("     source .venv/bin/activate")
    print("  4. Install TensorFlow:")
    print("     pip install --upgrade pip")
    print("     pip install tensorflow==2.15.0")
    print("  5. Run Flask server:")
    print("     python app.py")
    
    print("\nOPTION 2: Use CPU-only TensorFlow (FASTER TO TRY NOW)")
    print("  If Python 3.13+ has tensorflow-cpu support:")
    print("  1. pip install --upgrade pip")
    print("  2. pip install tensorflow-cpu")
    print("  3. If successful, run: python app.py")
    
    print("\nOPTION 3: Use Pre-release TensorFlow (EXPERIMENTAL)")
    print("  Try the development version:")
    print("  1. pip install --upgrade pip")
    print("  2. pip install --pre tensorflow")
    print("  3. If successful, run: python app.py")

else:
    print("\nRECOMMENDED FIX: Install TensorFlow")
    print("  1. Ensure you're in the virtual environment:")
    if platform.system() == "Windows":
        print("     .venv\\Scripts\\activate")
    else:
        print("     source .venv/bin/activate")
    print("  2. Upgrade pip:")
    print("     python -m pip install --upgrade pip")
    print("  3. Install TensorFlow:")
    print("     pip install tensorflow==2.15.0")
    print("  4. Verify installation:")
    print("     python -c \"import tensorflow as tf; print(tf.__version__)\"")
    print("  5. Run Flask server:")
    print("     python app.py")

# ============================================
# STEP 5: AUTO-FIX ATTEMPT
# ============================================

print("\n[STEP 5] Auto-Fix Attempt")
print("-" * 70)

if not TENSORFLOW_OK:
    user_choice = input("\nWould you like to try installing TensorFlow now? (y/n): ").strip().lower()
    
    if user_choice == 'y':
        print("\nAttempting to install TensorFlow...")
        
        if not in_venv:
            print("⚠ WARNING: Not in a virtual environment!")
            confirm = input("Continue anyway? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                sys.exit(0)
        
        try:
            print("\n1. Upgrading pip...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            
            print("\n2. Installing TensorFlow...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tensorflow"])
            
            print("\n✓ TensorFlow installation completed!")
            print("\nVerifying installation...")
            
            # Try to import and check version
            import importlib
            import tensorflow as tf
            print(f"✓ TensorFlow {tf.__version__} is now available!")
            
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Installation failed: {e}")
            print("This is expected if Python version is incompatible.")
            print("Please try the manual fix options listed above.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
            print("Please try the manual fix options listed above.")

# ============================================
# STEP 6: SUMMARY
# ============================================

print("\n[STEP 6] Summary")
print("-" * 70)

print("System Status:")
print(f"  Python Version:       {python_version} {'✓' if PYTHON_OK else '✗'}")
print(f"  Virtual Environment:  {'✓' if VENV_OK else '✗'}")
print(f"  TensorFlow Installed: {'✓' if TENSORFLOW_OK else '✗'}")

if TENSORFLOW_OK and PYTHON_OK:
    print("\n✓ All systems ready! Run: python app.py")
else:
    print("\n⚠ Please fix the issues listed above before running the Flask app.")

print("\n" + "="*70)
print("For more help, see: README.md, INSTALLATION.md")
print("="*70 + "\n")
