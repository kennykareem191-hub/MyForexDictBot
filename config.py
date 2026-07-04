# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration settings"""
    
    # Telegram Bot Token
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    # Database (Railway provides PostgreSQL)
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')
    
    # Redis for caching (optional)
    REDIS_URL = os.getenv('REDIS_URL', None)
    
    # Bot settings
    MAX_FAVORITES = 50
    QUIZ_QUESTIONS = 5
    SEARCH_LIMIT = 10
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is required! Set it in environment variables.")
        return True

# Validate on import
Config.validate()
