from . import db
from .base import BaseModel
from sqlalchemy.orm import validates
import bcrypt
import re
from datetime import datetime, timezone

class User(BaseModel):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    @validates('email')
    def validate_email(self, key: str, email: str) -> str:
        """Validate email format"""
        if not email:
            raise ValueError("Email cannot be empty")
        
        if not isinstance(email, str):
            raise ValueError("Email must be a string")
        
        email = email.strip().lower()
        
        # Basic email validation pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
        
        return email
    
    def set_password(self, password: str) -> None:
        """Hash and set the password"""
        if not password:
            raise ValueError("Password cannot be empty")
        
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        # Hash the password with bcrypt (12 rounds)
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        if not password:
            return False
        
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except Exception:
            return False
    
    def __repr__(self) -> str:
        return f'<User {self.email}>'
    
    def to_dict(self, include_timestamps: bool = False) -> dict:
        """Convert user to dictionary (never include password)"""
        user_dict = {
            'id': self.id,
            'email': self.email
        }
        
        if include_timestamps:
            user_dict['createdAt'] = self.created_at.isoformat() if self.created_at else None
            user_dict['updatedAt'] = self.updated_at.isoformat() if self.updated_at else None
        
        return user_dict
