# My Forex Dictionary Bot 📚

A comprehensive Telegram bot for learning Forex terminology.

## 🚀 Features

- **📖 Dictionary** - 60+ Forex terms with definitions
- **🔍 Smart Search** - Exact and partial matching
- **🧠 Interactive Quiz** - Test your knowledge
- **⭐ Favorites** - Save important terms
- **📊 Statistics** - Track your progress
- **💬 Natural Input** - Just type any term

## 📋 Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot |
| `/help` | Show help message |
| `/search [term]` | Look up a term |
| `/all` | Browse all terms |
| `/quiz` | Start a quiz |
| `/add [term]` | Add to favorites |
| `/remove [term]` | Remove from favorites |
| `/favorites` | View saved terms |
| `/stats` | View statistics |

## 🛠️ Technology Stack

- **Python 3.11** - Core language
- **python-telegram-bot** - Telegram API wrapper
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Production database (Railway)
- **SQLite** - Development database

## 📦 Installation

### Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/MyForexDictBot.git
cd MyForexDictBot

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your BOT_TOKEN

# Run bot
python bot.py
