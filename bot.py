import os
import sys
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Forex Dictionary Data
FOREX_DICT = {
    "pip": "The smallest price move that a given exchange rate can make. For most currency pairs, it's 0.0001.",
    "spread": "The difference between the bid (buy) and ask (sell) price of a currency pair.",
    "leverage": "Using borrowed capital to increase the potential return of an investment. Common ratios are 1:100 or 1:500.",
    "margin": "The amount of money required in your account to open and maintain a leveraged position.",
    "bullish": "A market outlook expecting prices to rise. A 'bull market' is characterized by rising prices.",
    "bearish": "A market outlook expecting prices to fall. A 'bear market' is characterized by falling prices.",
    "long": "Buying a currency pair with the expectation that its value will increase.",
    "short": "Selling a currency pair with the expectation that its value will decrease.",
    "stop loss": "An order placed to close a trade at a specific price to limit potential losses.",
    "take profit": "An order placed to close a trade at a specific price to secure profits.",
    "ask price": "The price at which you can buy a currency pair. Also known as the 'offer' price.",
    "bid price": "The price at which you can sell a currency pair.",
    "candlestick": "A type of price chart used in technical analysis that shows open, high, low, and close prices.",
    "support": "A price level where an asset tends to find buying interest, preventing it from falling further.",
    "resistance": "A price level where an asset tends to find selling interest, preventing it from rising further.",
    "trend": "The general direction in which a market is moving. Can be upward, downward, or sideways.",
    "volatility": "A statistical measure of the degree of variation in trading prices over time.",
    "liquidity": "A market with high trading volume where assets can be bought and sold easily.",
    "hedge": "An investment strategy used to offset potential losses in another investment.",
    "fundamental analysis": "Evaluating a currency based on economic indicators, news, and geopolitical events.",
    "technical analysis": "Forecasting price direction by analyzing historical price data and chart patterns.",
    "gdp": "Gross Domestic Product - a key economic indicator measuring a country's economic output.",
    "interest rate": "The rate at which a central bank lends money to commercial banks, affecting currency values.",
    "inflation": "The rate at which the general level of prices for goods and services rises.",
    "major pairs": "The most traded currency pairs: EUR/USD, USD/JPY, GBP/USD, USD/CHF.",
    "minor pairs": "Currency pairs that don't include the US dollar, like EUR/GBP or EUR/JPY.",
    "exotic pairs": "Currency pairs involving a major currency and a developing economy's currency.",
    "slippage": "The difference between the expected trade price and the actual executed price.",
    "lot size": "The standardized unit of measurement for a trade in forex. Standard lot = 100,000 units.",
    "swap": "The interest rate differential between two currencies in a forex trade held overnight.",
    "margin call": "When account equity falls below required margin, broker demands additional funds.",
    "stop out": "When broker automatically closes positions if margin level falls below required threshold."
}

# Helper Functions
def search_term(term):
    """Search for a term in the dictionary"""
    term_lower = term.lower().strip()
    
    # Exact match
    if term_lower in FOREX_DICT:
        return [(term_lower, FOREX_DICT[term_lower])]
    
    # Partial match
    results = []
    for key, value in FOREX_DICT.items():
        if term_lower in key.lower():
            results.append((key, value))
        if len(results) >= 10:
            break
    
    return results

def get_random_terms(count=5):
    """Get random terms for quiz"""
    import random
    keys = list(FOREX_DICT.keys())
    if len(keys) < count:
        count = len(keys)
    selected = random.sample(keys, count)
    return {k: FOREX_DICT[k] for k in selected}

# Get Bot Token from Environment
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN environment variable is required!")
    sys.exit(1)

logger.info(f"✅ Bot token loaded: {BOT_TOKEN[:10]}...")

# User favorites storage (in-memory)
user_favorites = {}

# ============ COMMAND HANDLERS ============

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
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

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
