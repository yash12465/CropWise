import os

class Config:
    # Application configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    DEBUG = True
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    
    # Babel configuration for translations
    LANGUAGES = {
        'en': 'English',
        'hi': 'हिन्दी',
        'mr': 'मराठी',
        'ta': 'தமிழ்',
        'te': 'తెలుగు',
        'gu': 'ગુજરાતી',
        'bn': 'বাংলা',
        'kn': 'ಕನ್ನಡ',
        'ml': 'മലയാളം',
        'pa': 'ਪੰਜਾਬੀ'
    }
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    
    # External API configuration
    OPENWEATHERMAP_API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
    
    # IoT integration configuration
    IOT_API_ENDPOINT = os.environ.get('IOT_API_ENDPOINT')
    IOT_API_KEY = os.environ.get('IOT_API_KEY')
    
    # File upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload