# bot.py
import os
import sys
import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    JobQueue
)
from telegram.constants import ParseMode

# Local imports
from config import Config
from database import init_db, SessionLocal, DatabaseOps
from dictionary_data import (
    FOREX_DICT, 
    search_term, 
    get_all_terms, 
    get_random_terms,
    get_term_count
)

# Configure logging for Railway
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL),
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

# Constants
MAX_FAVORITES = Config.MAX_FAVORITES
QUIZ_QUESTIONS = Config.QUIZ_QUESTIONS

# Initialize database
try:
    init_db()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    sys.exit(1)

# --- Helper Functions ---

def format_definition(term: str, definition: str) -> str:
    """Format term and definition for display"""
    return f"📖 *{term.capitalize()}*\n\n{definition}"

def format_search_results(results: List[Tuple[str, str]]) -> str:
    """Format search results"""
    if not results:
        return "❌ No results found"
    
    if len(results) == 1:
        return format_definition(results[0][0], results[0][1])
    
    response = "🔍 *Search Results:*\n\n"
    for term, definition in results:
        response += f"• *{term.capitalize()}*: {definition[:100]}...\n\n"
    return response

def get_quiz_result_message(score: int, total: int) -> str:
    """Generate motivational message based on score"""
    percentage = (score / total) * 100 if total > 0 else 0
    
    if percentage >= 90:
        return "🌟 *Outstanding!* You're a Forex Master!"
    elif percentage >= 70:
        return "📈 *Great job!* Keep up the excellent work!"
    elif percentage >= 50:
        return "📖 *Good effort!* Practice makes perfect!"
    elif percentage >= 30:
        return "💪 *Keep learning!* You're making progress!"
    else:
        return "📚 *Don't give up!* Review the terms and try again!"

# --- Command Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command"""
    user = update.effective_user
    
    # Register user in database
    db = SessionLocal()
    try:
        DatabaseOps.get_or_create_user(
            db,
            user.id,
            user.username,
            user.first_name,
            user.last_name
        )
    finally:
        db.close()
    
    welcome_text = f"""
👋 *Welcome to My Forex Dictionary Bot, {user.first_name or 'Trader'}!*

📚 Your comprehensive guide to Forex terminology.

*Available Commands:*
🔍 `/search [term]` - Find definition of a forex term
📋 `/all` - Browse all available terms
🧠 `/quiz` - Test your knowledge with a quiz
⭐ `/favorites` - View your saved terms
➕ `/add [term]` - Save term to favorites
➖ `/remove [term]` - Remove term from favorites
❓ `/help` - Show this help message

*Quick Tip:* You can also just type a word and I'll try to find it!

Let's master Forex together! 💹
"""
    await update.message.reply_text(welcome_text, parse_mode=ParseMode.MARKDOWN)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command"""
    help_text = """
📖 *My Forex Dictionary Bot - Help Guide*

*Basic Commands:*
• `/start` - Initialize the bot
• `/help` - Show this help message

*Learning & Research:*
• `/search [term]` - Look up a specific term
• `/all` - View complete list of forex terms
• `/quiz` - Start a 5-question quiz

*Favorites Management:*
• `/add [term]` - Add term to your favorites
• `/remove [term]` - Remove from favorites  
• `/favorites` - View all your saved terms

*Examples:*
