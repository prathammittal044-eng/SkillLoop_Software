import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillloop-secret-key-2026'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skillloop.db')
    DEBUG = True
