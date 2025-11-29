"""
Database Models Package
ORM Entity Models

All models are automatically registered with Base.metadata when imported.
Simply add your model files here and they will be auto-discovered during init_db()
"""

from model.user import User

# Add new models here as you create them
# from model.product import Product
# from model.order import Order

__all__ = ["User"]
