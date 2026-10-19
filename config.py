import os
from datetime import timedelta

# Detect production (Render, Hugging Face Spaces, or explicit IS_PRODUCTION)
_IS_PRODUCTION = bool(
    os.environ.get('RENDER_EXTERNAL_URL')
    or os.environ.get('IS_PRODUCTION')
    or os.environ.get('SPACE_ID')
    or os.environ.get('SPACE_HOST')
)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'skillloop-secret-key-2026'
    DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skillloop.db')
    DEBUG = not _IS_PRODUCTION

    # Persistent Session Configuration (Keeps users logged in across browser restarts for 30 days)
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_NAME = 'skillloop_session'
    SESSION_COOKIE_HTTPONLY = True

    # In production (cross-origin: Vercel frontend → Render backend), cookies MUST be
    # SameSite=None + Secure=True, otherwise the browser silently blocks them.
    # Locally (same origin or HTTP), use SameSite=Lax + Secure=False.
    SESSION_COOKIE_SAMESITE = 'None' if _IS_PRODUCTION else os.environ.get('SESSION_COOKIE_SAMESITE', 'Lax')
    SESSION_COOKIE_SECURE = _IS_PRODUCTION or os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
