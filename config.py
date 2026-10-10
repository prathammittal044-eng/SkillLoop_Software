import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillloop-secret-key-2026'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skillloop.db')
    DEBUG = True
    
    # Persistent Session Configuration (Keeps users logged in across browser restarts for 30 days)
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_NAME = 'skillloop_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    # Allow cookies over HTTP on localhost / LAN and HTTPS tunnels
    SESSION_COOKIE_SECURE = False
