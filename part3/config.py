import os

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']
    TESTING = os.environ.get('TESTING', 'False').lower() in ['true', '1', 't']
    DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///app.db'
    JSONIFY_PRETTYPRINT_REGULAR = False

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.environ.get('TEST_DATABASE_URI') or 'sqlite:///test.db'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False