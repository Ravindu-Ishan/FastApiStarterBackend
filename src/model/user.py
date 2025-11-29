"""
User Model - SQLAlchemy Core Table Definition
"""

from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from datetime import datetime
from config.database_config import db

# Define users table using SQLAlchemy Core
users = Table(
    'users',
    db.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(50), unique=True, nullable=False, index=True),
    Column('email', String(100), unique=True, nullable=False, index=True),
    Column('full_name', String(100), nullable=True),
    Column('hashed_password', String(255), nullable=False),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow, nullable=False),
    Column('updated_at', DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False),
)
