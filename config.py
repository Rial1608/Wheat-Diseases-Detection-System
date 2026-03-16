"""
Application Configuration Module
Manages environment-based configuration for Wheat Disease Detection System
"""

import os
from pathlib import Path
from typing import Optional

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base configuration"""
    
    # Flask Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'wheat_disease_detection_dev_key_2024')
    DEBUG: bool = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    TESTING: bool = os.getenv('FLASK_TESTING', 'False').lower() == 'true'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH: int = 50 * 1024 * 1024  # 50MB max upload
    ALLOWED_EXTENSIONS: set = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
    
    # Directory Configuration
    UPLOAD_FOLDER: str = os.path.join(BASE_DIR, 'static', 'uploads')
    RESULTS_FOLDER: str = os.path.join(BASE_DIR, 'static', 'results')
    MODEL_DIR: str = os.path.join(BASE_DIR, 'wheat-disease-detection', 'results')
    
    # Model Configuration
    MODEL_NAME: str = 'wheat_disease_model.h5'
    INPUT_SHAPE: tuple = (224, 224, 3)
    CLASS_NAMES: list = ['Healthy', 'Brown_rust', 'Yellow_rust']
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME: int = 3600  # 1 hour in seconds
    SESSION_COOKIE_SECURE: bool = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = 'Lax'
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE', None)
    
    @classmethod
    def get_model_path(cls) -> str:
        """Get full path to the model file"""
        return os.path.join(cls.MODEL_DIR, cls.MODEL_NAME)
    
    @classmethod
    def get_upload_folder(cls) -> str:
        """Ensure upload folder exists and return path"""
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        return cls.UPLOAD_FOLDER
    
    @classmethod
    def get_results_folder(cls) -> str:
        """Ensure results folder exists and return path"""
        os.makedirs(cls.RESULTS_FOLDER, exist_ok=True)
        return cls.RESULTS_FOLDER


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'tests', 'uploads')
    RESULTS_FOLDER = os.path.join(BASE_DIR, 'tests', 'results')


def get_config() -> Config:
    """Get appropriate configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'development').lower()
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }
    
    return config_map.get(env, DevelopmentConfig)


# Export active config
config = get_config()
