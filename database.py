# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')

# For PostgreSQL on Railway, ensure it uses the correct driver
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with favorites
    favorites = relationship('Favorite', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

class Favorite(Base):
    """User favorites model"""
    __tablename__ = 'favorites'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    term = Column(String(100), nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship with user
    user = relationship('User', back_populates='favorites')
    
    __table_args__ = (
        # Ensure a user can only have one favorite per term
        # This is handled in the application logic
    )
    
    def __repr__(self):
        return f"<Favorite(user_id={self.user_id}, term={self.term})>"

class QuizHistory(Base):
    """Quiz history model"""
    __tablename__ = 'quiz_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<QuizHistory(user_id={self.user_id}, score={self.correct_answers}/{self.total_questions})>"

# Create tables
def init_db():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database operations
class DatabaseOps:
    """Database operations handler"""
    
    @staticmethod
    def get_or_create_user(db, telegram_id, username=None, first_name=None, last_name=None):
        """Get user or create if not exists"""
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        
        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created new user: {telegram_id}")
        
        # Update last active
        user.last_active = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def add_favorite(db, user_id, term):
        """Add term to user's favorites"""
        # Check if already exists
        existing = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.term == term
        ).first()
        
        if existing:
            return False, "Already in favorites"
        
        # Check limit
        count = db.query(Favorite).filter(Favorite.user_id == user_id).count()
        if count >= 50:
            return False, "Favorites limit reached (50)"
        
        favorite = Favorite(user_id=user_id, term=term)
        db.add(favorite)
        db.commit()
        
        return True, "Added to favorites"
    
    @staticmethod
    def remove_favorite(db, user_id, term):
        """Remove term from user's favorites"""
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.term == term
        ).first()
        
        if not favorite:
            return False, "Not in favorites"
        
        db.delete(favorite)
        db.commit()
        return True, "Removed from favorites"
    
    @staticmethod
    def get_favorites(db, user_id):
        """Get all favorites for a user"""
        favorites = db.query(Favorite).filter(Favorite.user_id == user_id).all()
        return [fav.term for fav in favorites]
    
    @staticmethod
    def save_quiz_result(db, user_id, total, correct):
        """Save quiz result"""
        quiz = QuizHistory(
            user_id=user_id,
            total_questions=total,
            correct_answers=correct
        )
        db.add(quiz)
        db.commit()
        return quiz
