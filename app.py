import os

def _load_dotenv(path='.env'):
    """Load key=value pairs from a .env file into os.environ (no external deps)."""
    try:
        with open(path, encoding='utf-8') as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith('#') and '=' in _line:
                    _k, _, _v = _line.partition('=')
                    os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass

_load_dotenv()

import random
import sqlite3
import html as html_module
from datetime import datetime
try:
    import requests as http_requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database import get_db, close_db, init_db
from chat_routes import chat_bp
from chat_events import register_chat_events
from institutions import search_institutions
from turn_config import turn_bp

app = Flask(__name__)
app.config.from_object(Config)

# Build allowed origins list: always include localhost, and add Vercel domain in production
_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5000",
]
# Accept the FRONTEND_URL env var (set this in Render to your Vercel URL)
_FRONTEND_URL = os.environ.get('FRONTEND_URL', '')
if _FRONTEND_URL:
    _ALLOWED_ORIGINS.append(_FRONTEND_URL.rstrip('/'))
# Also allow any *.vercel.app domain for preview deployments
CORS(app, supports_credentials=True, origins=_ALLOWED_ORIGINS)

# Register modular Chat blueprint
app.register_blueprint(chat_bp)
app.register_blueprint(turn_bp)

# Initialize SocketIO for real-time messaging & WebRTC signaling
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False, ping_interval=5, ping_timeout=5)
register_chat_events(socketio)

# Initialize database tables
with app.app_context():
    init_db()

app.teardown_appcontext(close_db)

GRADIENTS = [
    'linear-gradient(135deg, #FF6B6B, #FF8E53)',
    'linear-gradient(135deg, #667eea, #764ba2)',
    'linear-gradient(135deg, #f093fb, #f5576c)',
    'linear-gradient(135deg, #4facfe, #00f2fe)',
    'linear-gradient(135deg, #43e97b, #38f9d7)',
    'linear-gradient(135deg, #fa709a, #fee140)',
    'linear-gradient(135deg, #a18cd1, #fbc2eb)',
    'linear-gradient(135deg, #fccb90, #d57eeb)'
]

@app.route('/api/status')
def status():
    return jsonify({"status": "online", "message": "SkillLoop API is running"})


def create_notification(user_id, actor_id, notif_type, title, message, link=''):
    """Helper to persist a notification and emit via socketio to user_{uid}."""
    try:
        db = get_db()
        cursor = db.execute('''
            INSERT INTO notifications (user_id, actor_id, type, title, message, link)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, actor_id, notif_type, title, message, link))
        db.commit()
        notif_id = cursor.lastrowid

        actor = None
        if actor_id:
            row = db.execute('SELECT id, username, full_name, profile_picture, avatar_color FROM users WHERE id = ?', (actor_id,)).fetchone()
            if row:
                actor = dict(row)

        payload = {
            'id': notif_id,
            'user_id': user_id,
            'actor_id': actor_id,
            'type': notif_type,
            'title': title,
            'message': message,
            'link': link,
            'is_read': False,
            'created_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            'actor': actor
        }
        try:
            socketio.emit('new_notification', payload, room=f"user_{user_id}")
        except Exception:
            pass
        return payload
    except Exception as e:
        app.logger.warning(f"Error creating notification: {e}")
        return None


@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    user_id = session['user_id']
    db = get_db()

    rows = db.execute('''
        SELECT n.id, n.user_id, n.actor_id, n.type, n.title, n.message, n.link, n.is_read, n.created_at,
               u.username as actor_username, u.full_name as actor_name, 
               u.profile_picture as actor_pic, u.avatar_color as actor_color
        FROM notifications n
        LEFT JOIN users u ON n.actor_id = u.id
        WHERE n.user_id = ?
        ORDER BY n.id DESC
        LIMIT 50
    ''', (user_id,)).fetchall()

    notifications = []
    unread_count = 0
    for r in rows:
        if not r['is_read']:
            unread_count += 1
        notifications.append({
            'id': r['id'],
            'user_id': r['user_id'],
            'actor_id': r['actor_id'],
            'type': r['type'],
            'title': r['title'],
            'message': r['message'],
            'link': r['link'],
            'is_read': bool(r['is_read']),
            'created_at': r['created_at'],
            'actor': {
                'id': r['actor_id'],
                'username': r['actor_username'],
                'full_name': r['actor_name'],
                'profile_picture': r['actor_pic'],
                'avatar_color': r['actor_color'] or '#543ce0'
            } if r['actor_id'] else None
        })

    # If user has no notifications yet, synthesize from pending connections & sessions
    if not notifications:
        pending_conns = db.execute('''
            SELECT c.id, c.requester_id, u.username, u.full_name, u.avatar_color, u.profile_picture, c.created_at
            FROM connections c
            JOIN users u ON c.requester_id = u.id
            WHERE c.receiver_id = ? AND c.status = 'pending'
        ''', (user_id,)).fetchall()
        for pc in pending_conns:
            p_name = pc['full_name'] or pc['username']
            notifications.append({
                'id': f"conn_{pc['id']}",
                'user_id': user_id,
                'actor_id': pc['requester_id'],
                'type': 'connection_request',
                'title': 'New Connection Request',
                'message': f"{p_name} sent you a connection request to swap skills.",
                'link': '/dashboard',
                'is_read': False,
                'created_at': pc['created_at'],
                'actor': {
                    'id': pc['requester_id'],
                    'username': pc['username'],
                    'full_name': pc['full_name'],
                    'profile_picture': pc['profile_picture'],
                    'avatar_color': pc['avatar_color'] or '#543ce0'
                }
            })
            unread_count += 1

        pending_sess = db.execute('''
            SELECT s.id, s.learner_id, s.skill_name, u.username, u.full_name, u.avatar_color, u.profile_picture, s.created_at
            FROM exchange_sessions s
            JOIN users u ON s.learner_id = u.id
            WHERE s.teacher_id = ? AND s.status = 'pending'
        ''', (user_id,)).fetchall()
        for ps in pending_sess:
            l_name = ps['full_name'] or ps['username']
            notifications.append({
                'id': f"sess_{ps['id']}",
                'user_id': user_id,
                'actor_id': ps['learner_id'],
                'type': 'session_requested',
                'title': 'Exchange Session Request',
                'message': f"{l_name} booked a session to learn {ps['skill_name']} from you.",
                'link': '/dashboard',
                'is_read': False,
                'created_at': ps['created_at'],
                'actor': {
                    'id': ps['learner_id'],
                    'username': ps['username'],
                    'full_name': ps['full_name'],
                    'profile_picture': ps['profile_picture'],
                    'avatar_color': ps['avatar_color'] or '#543ce0'
                }
            })
            unread_count += 1

    return jsonify({
        'notifications': notifications,
        'unread_count': unread_count
    }), 200


@app.route('/api/notifications/mark-read', methods=['POST'])
def mark_notifications_read():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    user_id = session['user_id']
    data = request.json or {}
    db = get_db()

    notif_id = data.get('id')
    if notif_id and not str(notif_id).startswith(('conn_', 'sess_')):
        db.execute('UPDATE notifications SET is_read = 1 WHERE id = ? AND user_id = ?', (notif_id, user_id))
    else:
        db.execute('UPDATE notifications SET is_read = 1 WHERE user_id = ?', (user_id,))
    db.commit()
    return jsonify({"status": "ok"}), 200


@app.route('/api/notifications/<int:notif_id>', methods=['DELETE'])
def delete_notification(notif_id):
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    user_id = session['user_id']
    db = get_db()
    db.execute('DELETE FROM notifications WHERE id = ? AND user_id = ?', (notif_id, user_id))
    db.commit()
    return jsonify({"status": "deleted"}), 200


@app.route('/api/notifications/clear-all', methods=['DELETE'])
def clear_all_notifications():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    user_id = session['user_id']
    db = get_db()
    db.execute('DELETE FROM notifications WHERE user_id = ?', (user_id,))
    db.commit()
    return jsonify({"status": "cleared"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    department = data.get('department')
    semester = data.get('semester')

    if not all([username, email, password, full_name, department, semester]):
        return jsonify({"error": "All fields are required"}), 400
    
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    db = get_db()
    
    # Check uniqueness
    user = db.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email)).fetchone()
    if user:
        return jsonify({"error": "Username or email already exists"}), 409

    password_hash = generate_password_hash(password)
    avatar_color = random.choice(GRADIENTS)

    try:
        cursor = db.execute('''
            INSERT INTO users (username, email, password_hash, full_name, department, semester, avatar_color)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, department, semester, avatar_color))
        db.commit()
        
        user_id = cursor.lastrowid
        session.permanent = True
        session['user_id'] = user_id
        session['username'] = username
        session['full_name'] = full_name
        session.modified = True
        
        return jsonify({"message": "Registration successful", "user_id": user_id}), 201
    except Exception as e:
        return jsonify({"error": "An error occurred during registration"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get('username', '').strip()
    password = data.get('password', '')
    remember_me = data.get('remember_me', True)
    
    if not username or not password:
        return jsonify({"error": "Please enter username and password"}), 400
        
    db = get_db()
    clean_username = username.lstrip('@').strip()
    user = db.execute('SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)', 
                      (clean_username, clean_username)).fetchone()
    
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid username or password"}), 401
        
    session.permanent = bool(remember_me)
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['full_name'] = user['full_name']
    session.modified = True
    
    return jsonify({
        "message": "Logged in successfully",
        "user": {
            "id": user['id'],
            "username": user['username'],
            "full_name": user['full_name'],
            "avatar_color": user['avatar_color']
        }
    }), 200

@app.route('/api/user/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    db = get_db()
    user = db.execute('''
        SELECT id, username, email, full_name, department, semester, bio,
               education, qualifications, experience, github, linkedin,
               xp, level, streak_count, time_credits, avatar_color, created_at,
               rating_avg, rating_count, total_sessions, skills_taught, skills_learned,
               total_teaching_seconds, total_learning_seconds,
               headline, github_url, linkedin_url, portfolio_url,
               graduation_year, profile_picture, banner_image
        FROM users WHERE id = ?
    ''', (session['user_id'],)).fetchone()
    
    if user is None:
        session.clear()
        return jsonify({"error": "User not found"}), 404
        
    session.modified = True
    return jsonify({"user": dict(user)}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    resp = jsonify({"message": "Logged out successfully"})
    cookie_name = app.config.get('SESSION_COOKIE_NAME', 'skillloop_session')
    resp.delete_cookie(cookie_name)
    return resp, 200

# ─── Profile Picture & Banner Upload ─────────────────────────────────────────
# NOTE: Images are stored as Base64 data URLs directly in the database.
# This ensures images persist across Render restarts (no ephemeral disk dependency).
import uuid
import base64

ALLOWED_IMAGE_EXTS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
# 5 MB limit per image (base64 inflates ~33%, so raw file max ~3.75 MB)
MAX_IMAGE_BYTES = 5 * 1024 * 1024

MIME_MAP = {'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'gif': 'image/gif', 'webp': 'image/webp'}

def _allowed_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTS

def _file_to_data_url(file_obj, ext):
    """Read uploaded file and return a data: URL string (persistent in DB)."""
    raw = file_obj.read()
    if len(raw) > MAX_IMAGE_BYTES:
        return None, "Image is too large (max 5 MB)"
    mime = MIME_MAP.get(ext, 'image/jpeg')
    b64 = base64.b64encode(raw).decode('ascii')
    return f"data:{mime};base64,{b64}", None

@app.route('/api/user/upload-avatar', methods=['POST'])
def upload_avatar():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data_url = None
    if request.is_json:
        data = request.get_json(silent=True) or {}
        img = data.get('image') or data.get('data_url')
        if img and str(img).startswith('data:image/'):
            data_url = str(img)
        else:
            return jsonify({"error": "Invalid base64 image data"}), 400
    elif 'file' in request.files:
        f = request.files['file']
        if not f.filename or not _allowed_image(f.filename):
            return jsonify({"error": "Invalid image file (png, jpg, jpeg, gif, webp allowed)"}), 400
        ext = f.filename.rsplit('.', 1)[1].lower()
        data_url, err = _file_to_data_url(f, ext)
        if err:
            return jsonify({"error": err}), 400
    else:
        return jsonify({"error": "No image data or file provided"}), 400

    db = get_db()
    db.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (data_url, session['user_id']))
    db.commit()
    return jsonify({"url": data_url}), 200

@app.route('/api/user/upload-banner', methods=['POST'])
def upload_banner():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data_url = None
    if request.is_json:
        data = request.get_json(silent=True) or {}
        img = data.get('image') or data.get('data_url')
        if img and str(img).startswith('data:image/'):
            data_url = str(img)
        else:
            return jsonify({"error": "Invalid base64 image data"}), 400
    elif 'file' in request.files:
        f = request.files['file']
        if not f.filename or not _allowed_image(f.filename):
            return jsonify({"error": "Invalid image file (png, jpg, jpeg, gif, webp allowed)"}), 400
        ext = f.filename.rsplit('.', 1)[1].lower()
        data_url, err = _file_to_data_url(f, ext)
        if err:
            return jsonify({"error": err}), 400
    else:
        return jsonify({"error": "No image data or file provided"}), 400

    db = get_db()
    db.execute("UPDATE users SET banner_image = ? WHERE id = ?", (data_url, session['user_id']))
    db.commit()
    return jsonify({"url": data_url}), 200


@app.route('/api/user/xp', methods=['POST'])
def add_xp():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.json
    xp_gained = data.get('xp_gained', 0)
    
    if not isinstance(xp_gained, int) or xp_gained <= 0:
        return jsonify({"error": "Invalid XP amount"}), 400
        
    db = get_db()
    user = db.execute('SELECT xp, level FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    new_xp = user['xp'] + xp_gained
    # Simple leveling system: 1 level per 100 XP
    new_level = (new_xp // 100) + 1
    
    db.execute('UPDATE users SET xp = ?, level = ? WHERE id = ?', (new_xp, new_level, session['user_id']))
    db.commit()
    
    return jsonify({
        "message": "XP updated successfully",
        "xp": new_xp,
        "level": new_level,
        "leveled_up": new_level > user['level']
    }), 200

@app.route('/api/skills', methods=['GET', 'POST'])
def manage_skills():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    db = get_db()
    user_id = session['user_id']
    
    if request.method == 'GET':
        skills = db.execute('SELECT id, skill_name, skill_type FROM user_skills WHERE user_id = ?', (user_id,)).fetchall()
        
        teaches = [{"id": s['id'], "name": s['skill_name']} for s in skills if s['skill_type'] == 'teaches']
        learns = [{"id": s['id'], "name": s['skill_name']} for s in skills if s['skill_type'] == 'learns']
        
        return jsonify({"teaches": teaches, "learns": learns}), 200
        
    if request.method == 'POST':
        data = request.json
        skill_name = data.get('skill_name', '').strip().lower()
        skill_type = data.get('skill_type')
        
        if not skill_name or skill_type not in ('teaches', 'learns'):
            return jsonify({"error": "Invalid input"}), 400
            
        try:
            cursor = db.execute('INSERT INTO user_skills (user_id, skill_name, skill_type) VALUES (?, ?, ?)',
                                (user_id, skill_name, skill_type))
            db.commit()
            return jsonify({"message": "Skill added", "id": cursor.lastrowid, "name": skill_name, "type": skill_type}), 201
        except sqlite3.IntegrityError:
            return jsonify({"error": "Skill already added"}), 409

@app.route('/api/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    db = get_db()
    db.execute('DELETE FROM user_skills WHERE id = ? AND user_id = ?', (skill_id, session['user_id']))
    db.commit()
    return jsonify({"message": "Skill removed"}), 200

@app.route('/api/matches', methods=['GET'])
def get_matches():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    db = get_db()
    current_user_id = session['user_id']

    try:
        # â”€â”€ 1. Load all users â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        all_users_rows = db.execute(
            'SELECT id, username, full_name, avatar_color FROM users'
        ).fetchall()

        # Only columns that actually exist in the DB
        all_skills_rows = db.execute(
            'SELECT user_id, skill_name, skill_type FROM user_skills'
        ).fetchall()

        # Verification data â€” table may not exist on older DBs
        try:
            all_verif_rows = db.execute(
                'SELECT user_id, skill_name, verified_level FROM skill_verifications'
            ).fetchall()
        except Exception:
            all_verif_rows = []

        # â”€â”€ 2. Build user data structures â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        users_data = {}
        for r in all_users_rows:
            users_data[r['id']] = {
                "id":        r['id'],
                "username":  r['username'],
                "full_name": r['full_name'],
                "avatar":    r['avatar_color'],
                "teaches":   set(),   # lowercase skill names
                "learns":    set(),   # lowercase skill names
                "verified":  {}       # skill_name -> verified_level
            }

        for r in all_skills_rows:
            uid = r['user_id']
            if uid not in users_data:
                continue
            skill = r['skill_name'].lower().strip()
            if r['skill_type'] == 'teaches':
                users_data[uid]['teaches'].add(skill)
            else:
                users_data[uid]['learns'].add(skill)

        for r in all_verif_rows:
            uid = r['user_id']
            if uid in users_data:
                users_data[uid]['verified'][r['skill_name'].lower().strip()] = r['verified_level'].lower()

        # â”€â”€ 3. Build adjacency list â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # Edge Aâ†’B if A teaches anything B wants to learn.
        # Store skill info per edge for scoring/display.
        adj = {uid: {} for uid in users_data}

        for a_id, a_data in users_data.items():
            for b_id, b_data in users_data.items():
                if a_id == b_id:
                    continue
                shared = a_data['teaches'] & b_data['learns']
                if not shared:
                    continue
                skill_infos = [
                    {"skill": s.title(), "verified": s in a_data['verified']}
                    for s in shared
                ]
                adj[a_id][b_id] = skill_infos

        # â”€â”€ 4. DFS â€” find all cycles involving current user â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        raw_cycles = []
        MAX_DEPTH = 4  # cap at 4-person chains

        def dfs(node, path, visited, edge_data):
            if len(path) > MAX_DEPTH:
                return
            for neighbor, skills in adj.get(node, {}).items():
                if neighbor == current_user_id and len(path) >= 2:
                    raw_cycles.append({
                        "path":  path + [current_user_id],
                        "edges": edge_data + [skills]
                    })
                elif neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor, path + [neighbor], visited, edge_data + [skills])
                    visited.remove(neighbor)

        dfs(current_user_id, [current_user_id], {current_user_id}, [])

        # â”€â”€ 5. Validity check â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # A cycle is only valid if EVERY person in it actually receives something.
        # i.e. for every Aâ†’B edge, B must also teach something to someone later
        # in the cycle.  The DFS already ensures we loop back to current_user,
        # so we just make sure every member both teaches AND learns within the cycle.
        def is_valid_cycle(c):
            path = c["path"][:-1]  # members without the duplicate closing node
            member_set = set(path)
            for uid in member_set:
                u = users_data[uid]
                # Must both give and receive something within the cycle
                teaches_in_cycle = any(
                    u['teaches'] & users_data[other]['learns']
                    for other in member_set if other != uid
                )
                learns_in_cycle = any(
                    u['learns'] & users_data[other]['teaches']
                    for other in member_set if other != uid
                )
                if not (teaches_in_cycle and learns_in_cycle):
                    return False
            return True

        valid_cycles = [c for c in raw_cycles if is_valid_cycle(c)]

        # â”€â”€ 6. Score each valid cycle â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # Shorter cycles score higher. Verified teachers give a bonus.
        LENGTH_SCORES = {2: 100, 3: 60, 4: 30}

        def score_cycle(c):
            base  = LENGTH_SCORES.get(len(c["path"]) - 1, 10)
            bonus = sum(25 for edge in c["edges"] for s in edge if s["verified"])
            return base + bonus

        sorted_cycles = sorted(valid_cycles, key=score_cycle, reverse=True)

        # â”€â”€ 7. Greedy Disjoint Cycle Selection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        # Core rule: once a user is committed to a cycle they CANNOT appear
        # in any other cycle shown to the current user. This prevents the bug
        # where the same person shows up in multiple trade suggestions.
        #
        # Algorithm:
        #   1. Pick the highest-scoring cycle â†’ add to results, lock its members
        #   2. Discard any remaining cycle that shares a member with a locked user
        #   3. Repeat until no valid cycles remain or we have MAX_RESULTS results
        MAX_RESULTS = 5
        committed_users = set()   # other users already committed to a selected cycle
        selected_cycles = []

        for c in sorted_cycles:
            # Check other users in this cycle (excluding the current user, who is in all cycles)
            other_members = set(c["path"][:-1]) - {current_user_id}

            # Skip if any other peer in this cycle is already committed to another suggested cycle
            if other_members & committed_users:
                continue

            selected_cycles.append(c)
            committed_users.update(other_members)

            if len(selected_cycles) >= MAX_RESULTS:
                break

        # â”€â”€ 8. Assign quality labels â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        def quality_label(c):
            sc = score_cycle(c)
            if sc >= 150:  return "Perfect Match"
            if sc >= 100:  return "Great Match"
            if sc >= 60:   return "Good Match"
            return "Fair Match"

        # â”€â”€ 9. Format for frontend â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        formatted = []
        for c in selected_cycles:
            path, edges = c["path"], c["edges"]
            nodes = []
            for i in range(len(path) - 1):
                gid     = path[i]
                g       = users_data[gid]
                infos   = edges[i]
                best    = next((s for s in infos if s["verified"]), infos[0])
                v_level = g['verified'].get(best["skill"].lower(), 'beginner')
                nodes.append({
                    "user_id":       gid,
                    "name":          (g['full_name'] or g['username']).split()[0],
                    "full_name":     g['full_name'] or g['username'],
                    "avatar":        g['avatar'],
                    "teaches_next":  best["skill"],
                    "verified":      best["verified"],
                    "teacher_level": v_level,
                    "all_skills":    [s["skill"] for s in infos]
                })

            sc = score_cycle(c)
            formatted.append({
                "nodes":        nodes,
                "score":        sc,
                "length":       len(path) - 1,
                "all_verified": all(n["verified"] for n in nodes),
                "quality":      quality_label(c)
            })

        return jsonify({"cycles": formatted}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"cycles": [], "error": str(e)}), 200



@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    db = get_db()
    users = db.execute('''
        SELECT username, full_name, avatar_color, xp, level, time_credits 
        FROM users 
        ORDER BY xp DESC 
        LIMIT 10
    ''').fetchall()
    return jsonify({"leaderboard": [dict(u) for u in users]}), 200

@app.route('/api/connect', methods=['POST'])
def send_connection():
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    data = request.json or {}
    receiver_id = data.get('receiver_id')
    target_username = data.get('username')
    db = get_db()

    if not receiver_id and target_username:
        clean_user = target_username.lstrip('@').strip().lower()
        target = db.execute('SELECT id FROM users WHERE LOWER(username) = ?', (clean_user,)).fetchone()
        if not target:
            return jsonify({"error": f"User '@{clean_user}' not found"}), 404
        receiver_id = target['id']

    if not receiver_id or receiver_id == session['user_id']:
        return jsonify({"error": "Invalid receiver"}), 400

    # Check if a connection already exists in either direction
    existing = db.execute('''
        SELECT id, requester_id, receiver_id, status 
        FROM connections 
        WHERE (requester_id = ? AND receiver_id = ?) 
           OR (requester_id = ? AND receiver_id = ?)
    ''', (session['user_id'], receiver_id, receiver_id, session['user_id'])).fetchone()

    if existing:
        if existing['status'] == 'accepted':
            return jsonify({"message": "You are already connected with this peer!", "status": "accepted"}), 200
        elif existing['requester_id'] == receiver_id and existing['status'] == 'pending':
            # Mutual connection: the other user already sent a pending request to us!
            db.execute("UPDATE connections SET status = 'accepted' WHERE id = ?", (existing['id'],))
            db.commit()
            return jsonify({"message": "Mutual connection! You are now connected!", "status": "accepted"}), 200
        else:
            return jsonify({"message": "Connection request is already pending.", "status": "pending"}), 200

    sender = db.execute('SELECT id, username, full_name, department FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    sender_skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (session['user_id'],)).fetchall()
    sender_teaches = [s['skill_name'] for s in sender_skills if s['skill_type'] == 'teaches']
    sender_learns  = [s['skill_name'] for s in sender_skills if s['skill_type'] == 'learns']

    cursor = db.execute('INSERT INTO connections (requester_id, receiver_id, status) VALUES (?, ?, "pending")',
               (session['user_id'], receiver_id))
    db.commit()
    conn_id = cursor.lastrowid

    # Emit real-time notification to the receiver
    create_notification(
        receiver_id, session['user_id'], 'connection_request',
        'New Connection Request',
        f"{sender['full_name'] or sender['username']} sent you a connection request to swap skills.",
        '/dashboard'
    )
    socketio.emit('connection_request', {
        'connection_id': conn_id,
        'requester_id': session['user_id'],
        'full_name': sender['full_name'] or sender['username'],
        'username': sender['username'],
        'department': sender['department'] or 'Campus Peer',
        'teaches': sender_teaches,
        'learns': sender_learns,
    }, room=f"user_{receiver_id}")

    return jsonify({"message": "Connection request sent successfully!", "status": "pending"}), 201

@app.route('/api/connect/<int:conn_id>', methods=['PUT'])
def update_connection(conn_id):
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    status = request.json.get('status')
    if status not in ('accepted', 'rejected'): return jsonify({"error": "Invalid status"}), 400
    
    db = get_db()
    conn = db.execute('SELECT requester_id, receiver_id FROM connections WHERE id = ?', (conn_id,)).fetchone()
    db.execute('UPDATE connections SET status = ? WHERE id = ? AND receiver_id = ?', (status, conn_id, session['user_id']))
    db.commit()

    # Notify the requester in real-time
    if conn and status == 'accepted':
        accepter = db.execute('SELECT username, full_name FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        a_name = (accepter['full_name'] or accepter['username']) if accepter else 'Peer'
        create_notification(
            conn['requester_id'], session['user_id'], 'connection_accepted',
            'Connection Accepted!',
            f"{a_name} accepted your connection request! You can now chat and video call.",
            f'/chat?id={session["user_id"]}'
        )
        socketio.emit('connection_accepted', {
            'connection_id': conn_id,
            'accepted_by_id': session['user_id'],
            'accepted_by_name': a_name,
            'accepted_by_username': accepter['username'] if accepter else '',
        }, room=f"user_{conn['requester_id']}")

    return jsonify({"message": f"Connection {status}"}), 200

@app.route('/api/connections', methods=['GET'])
def get_connections():
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    db = get_db()
    uid = session['user_id']
    
    # Get incoming pending
    pending_rows = db.execute('''
        SELECT c.id, c.requester_id, u.id as user_id, u.username, u.full_name, u.department, u.avatar_color, c.created_at
        FROM connections c JOIN users u ON c.requester_id = u.id 
        WHERE c.receiver_id = ? AND c.status = 'pending'
        ORDER BY c.created_at DESC
    ''', (uid,)).fetchall()

    pending = []
    for p in pending_rows:
        skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (p['user_id'],)).fetchall()
        teaches = [s['skill_name'].title() for s in skills if s['skill_type'] == 'teaches']
        learns = [s['skill_name'].title() for s in skills if s['skill_type'] == 'learns']
        pending.append({
            "id": p['id'],
            "user_id": p['user_id'],
            "username": p['username'],
            "full_name": p['full_name'] or p['username'],
            "department": p['department'] or 'Campus Peer',
            "avatar_color": p['avatar_color'],
            "skill_offered": ", ".join(teaches) if teaches else "Various Skills",
            "skill_wanted": ", ".join(learns) if learns else "New Skills",
            "teaches": teaches,
            "learns": learns,
            "created_at": p['created_at']
        })

    # Get active connections (where user is either requester or receiver)
    active_rows = db.execute('''
        SELECT c.id, u.id as user_id, u.username, u.full_name, u.department, u.avatar_color, c.created_at
        FROM connections c JOIN users u ON (c.requester_id = u.id OR c.receiver_id = u.id)
        WHERE (c.requester_id = ? OR c.receiver_id = ?) AND c.status = 'accepted' AND u.id != ?
        ORDER BY c.created_at DESC
    ''', (uid, uid, uid)).fetchall()

    active = []
    for a in active_rows:
        skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (a['user_id'],)).fetchall()
        teaches = [s['skill_name'].title() for s in skills if s['skill_type'] == 'teaches']
        learns = [s['skill_name'].title() for s in skills if s['skill_type'] == 'learns']
        active.append({
            "id": a['id'],
            "user_id": a['user_id'],
            "username": a['username'],
            "full_name": a['full_name'] or a['username'],
            "department": a['department'] or 'Campus Peer',
            "avatar_color": a['avatar_color'],
            "teaches": teaches,
            "learns": learns,
            "created_at": a['created_at']
        })

    return jsonify({"pending": pending, "active": active}), 200

@app.route('/api/users/search', methods=['GET'])
def search_users():
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    q = request.args.get('q', '').strip().lstrip('@').lower()
    if not q:
        return jsonify({"users": []}), 200
    
    db = get_db()
    current_uid = session['user_id']
    like = f"%{q}%"
    rows = db.execute('''
        SELECT id, username, full_name, department, semester, avatar_color
        FROM users
        WHERE id != ? AND (LOWER(username) LIKE ? OR LOWER(full_name) LIKE ?)
        LIMIT 10
    ''', (current_uid, like, like)).fetchall()
    
    results = []
    for r in rows:
        uid = r['id']
        skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (uid,)).fetchall()
        teaches = [s['skill_name'].title() for s in skills if s['skill_type'] == 'teaches']
        learns = [s['skill_name'].title() for s in skills if s['skill_type'] == 'learns']
        
        conn = db.execute('''
            SELECT id, status, requester_id FROM connections
            WHERE (requester_id = ? AND receiver_id = ?) OR (requester_id = ? AND receiver_id = ?)
        ''', (current_uid, uid, uid, current_uid)).fetchone()
        
        conn_status = 'none'
        conn_id = None
        if conn:
            conn_id = conn['id']
            if conn['status'] == 'accepted':
                conn_status = 'connected'
            elif conn['requester_id'] == current_uid:
                conn_status = 'pending_sent'
            else:
                conn_status = 'pending_received'
                
        results.append({
            "id": uid,
            "username": r['username'],
            "full_name": r['full_name'] or r['username'],
            "department": r['department'] or 'Campus Peer',
            "semester": r['semester'],
            "avatar_color": r['avatar_color'],
            "teaches": teaches,
            "learns": learns,
            "connection_status": conn_status,
            "connection_id": conn_id
        })
        
    return jsonify({"users": results}), 200

@app.route('/api/session/log', methods=['POST'])
def log_session():
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    data = request.json
    hours = data.get('hours', 1)
    db = get_db()
    # Assuming current user is the teacher logging their hours
    db.execute('UPDATE users SET time_credits = time_credits + ?, streak_count = streak_count + 1, xp = xp + ? WHERE id = ?', (hours, hours * 10, session['user_id']))
    db.commit()
    return jsonify({"message": "Session logged successfully"}), 200

@app.route('/api/user/me', methods=['PUT'])
def update_profile():
    if 'user_id' not in session: return jsonify({"error": "Not authenticated"}), 401
    data = request.json
    db = get_db()
    db.execute('''
        UPDATE users SET 
            full_name = ?, 
            department = ?, 
            semester = ?,
            bio = ?,
            education = ?,
            qualifications = ?,
            experience = ?,
            github = ?,
            linkedin = ?,
            headline = ?,
            github_url = ?,
            linkedin_url = ?,
            portfolio_url = ?,
            graduation_year = ?
        WHERE id = ?
    ''', (
        data.get('full_name'), data.get('department'), data.get('semester'),
        data.get('bio'), data.get('education'), data.get('qualifications'),
        data.get('experience'), data.get('github'), data.get('linkedin'),
        data.get('headline', ''), data.get('github_url', ''),
        data.get('linkedin_url', ''), data.get('portfolio_url', ''),
        data.get('graduation_year'),
        session['user_id']
    ))
    db.commit()
    return jsonify({"message": "Profile updated"}), 200

@app.route('/api/user/<username>', methods=['GET'])
def get_public_profile(username):
    db = get_db()
    user = db.execute('''
        SELECT id, username, full_name, department, semester, bio,
               xp, level, avatar_color, rating_avg, rating_count,
               total_sessions, total_teaching_seconds, total_learning_seconds,
               headline, github_url, linkedin_url, portfolio_url,
               graduation_year, profile_picture, banner_image, created_at
        FROM users WHERE username = ?
    ''', (username,)).fetchone()
    if not user: return jsonify({"error": "User not found"}), 404

    user_id = user['id']

    # Skills
    skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (user_id,)).fetchall()
    teaches = [s['skill_name'] for s in skills if s['skill_type'] == 'teaches']
    learns = [s['skill_name'] for s in skills if s['skill_type'] == 'learns']

    # Verified skills
    verified = db.execute(
        'SELECT skill_name, verified_level, verified_at, sessions_taught FROM skill_verifications WHERE user_id = ? ORDER BY verified_at DESC',
        (user_id,)
    ).fetchall()
    verified_list = [dict(v) for v in verified]

    # Reviews received (last 10)
    reviews = db.execute('''
        SELECT sr.rating, sr.comment, sr.role, sr.created_at,
               u.full_name AS reviewer_name, u.username AS reviewer_username, u.avatar_color AS reviewer_color
        FROM session_reviews sr
        JOIN users u ON u.id = sr.reviewer_id
        WHERE sr.reviewee_id = ?
        ORDER BY sr.created_at DESC
        LIMIT 10
    ''', (user_id,)).fetchall()
    reviews_list = [dict(r) for r in reviews]

    # Connection status with currently logged-in user
    conn_status = None
    if 'user_id' in session and session['user_id'] != user_id:
        me = session['user_id']
        conn = db.execute('''
            SELECT status, requester_id FROM connections
            WHERE (requester_id = ? AND receiver_id = ?) OR (requester_id = ? AND receiver_id = ?)
        ''', (me, user_id, user_id, me)).fetchone()
        if conn:
            conn_status = {'status': conn['status'], 'i_sent': conn['requester_id'] == me}

    profile = dict(user)
    profile['teaches'] = teaches
    profile['learns'] = learns
    profile['verified_skills'] = verified_list
    profile['reviews'] = reviews_list
    profile['connection_status'] = conn_status
    return jsonify({"profile": profile}), 200


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SKILL VERIFICATION QUIZ ENGINE v3.0  â€” AI-Powered (Gemini)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

import json as _json
def _load_dotenv(path='.env'):
    """Load key=value pairs from a .env file into os.environ (no external deps)."""
    try:
        with open(path, encoding='utf-8') as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith('#') and '=' in _line:
                    _k, _, _v = _line.partition('=')
                    os.environ.setdefault(_k.strip(), _v.strip().strip('"').strip("'"))
    except FileNotFoundError:
        pass

_load_dotenv()  # loads GEMINI_API_KEY and other vars from .env

try:
    from google import genai as _genai
    from google.genai import types as _genai_types
    _GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
    if _GEMINI_KEY:
        _genai_client = _genai.Client(api_key=_GEMINI_KEY)
    else:
        _genai_client = None
    GEMINI_AVAILABLE = bool(_GEMINI_KEY)
except ImportError:
    _genai_client = None
    GEMINI_AVAILABLE = False

QUIZ_TIME_MAP = {'beginner': 20, 'intermediate': 15, 'advanced': 10}

# How many questions per quiz
QUIZ_QUESTION_COUNT = 7

def _get_gemini_models(client):
    """Return available Gemini model names dynamically, prioritized for speed & quality."""
    try:
        discovered = []
        for m in client.models.list():
            name = getattr(m, 'name', '') or ''
            clean = name.replace('models/', '').strip()
            methods = getattr(m, 'supported_actions', []) or getattr(m, 'supported_generation_methods', []) or []
            if not methods or 'generateContent' in methods:
                discovered.append(clean)
        if discovered:
            prioritized = []
            for pref in ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-2.5-flash', 'gemini-1.5-pro']:
                for d in discovered:
                    if pref in d and d not in prioritized:
                        prioritized.append(d)
            for d in discovered:
                if d not in prioritized:
                    prioritized.append(d)
            if prioritized:
                return prioritized
    except Exception as e:
        app.logger.warning(f"Could not list models from Google GenAI: {e}")
    # Fallback to verified GA model names
    return ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-2.5-flash']


def generate_ai_questions(skill_name: str, difficulty: str):
    """
    Ask Google Gemini to generate QUIZ_QUESTION_COUNT multiple-choice questions
    about `skill_name` at `difficulty` level.
    Returns (validated_questions, None) on success or (None, error_str) on failure.
    """
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        return None, "GEMINI_API_KEY is not set in Render environment variables."

    try:
        client = _genai.Client(api_key=key)
    except Exception as e:
        return None, f"Failed to initialize Gemini client: {e}"

    difficulty_guidance = {
        'beginner':     'very basic, introductory concepts that a complete newcomer would know after a week of learning',
        'intermediate': 'practical, hands-on concepts that someone with 6-12 months of experience should know',
        'advanced':     'deep, nuanced, expert-level concepts including edge cases, internals, and best practices',
    }
    guidance = difficulty_guidance.get(difficulty, 'general knowledge')

    prompt = f"""You are a quiz generator for a skill-exchange learning platform.

Generate exactly {QUIZ_QUESTION_COUNT} multiple-choice questions about "{skill_name}" at a "{difficulty}" difficulty level.

Difficulty guidance: {guidance}

Rules:
- Every question must be directly and specifically about "{skill_name}"
- Each question must have exactly 4 answer options (A, B, C, D)
- Exactly one option must be correct
- The other three must be plausible but clearly wrong
- Questions must test genuine understanding, NOT trivia or dates
- Do NOT number the questions
- Return ONLY a valid JSON array. No markdown, no explanation, no extra text.

Required JSON format:
[
  {{
    "q": "question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": 0
  }}
]

The "answer" field is the 0-based index of the correct option in the "options" array.
"""

    candidate_models = _get_gemini_models(client)
    app.logger.info(f"Trying Gemini models for quiz: {candidate_models[:3]}")

    all_errors = []
    for model_name in candidate_models:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=_genai_types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=2048,
                )
            )
            raw = (response.text or '').strip()

            # Strip markdown code fences if Gemini wraps in ```json ... ```
            if raw.startswith('```'):
                raw = raw.split('```')[1]
                if raw.startswith('json'):
                    raw = raw[4:]
                raw = raw.strip()

            questions = _json.loads(raw)

            # Validate structure
            validated = []
            for q in questions:
                if (isinstance(q, dict)
                        and 'q' in q
                        and 'options' in q
                        and 'answer' in q
                        and isinstance(q['options'], list)
                        and len(q['options']) == 4
                        and isinstance(q['answer'], int)
                        and 0 <= q['answer'] <= 3):
                    validated.append(q)

            if len(validated) >= 3:
                app.logger.info(f'Quiz generated successfully via model={model_name} for skill={skill_name}')
                return validated, None

            all_errors.append(f"[{model_name}]: Returned {len(validated)} questions (need at least 3)")
        except Exception as e:
            err_msg = str(e)
            all_errors.append(f"[{model_name}]: {err_msg}")
            app.logger.warning(f'Gemini model={model_name} failed for "{skill_name}": {err_msg}')
            continue

    summary_error = " | ".join(all_errors[:3])
    app.logger.error(f'All Gemini models failed for "{skill_name}": {summary_error}')
    return None, summary_error


@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json
    skill_name = (data.get('skill_name') or '').strip().lower()
    difficulty  = (data.get('difficulty') or 'beginner').strip().lower()

    if not skill_name:
        return jsonify({"error": "Skill name is required"}), 400
    if difficulty not in ('beginner', 'intermediate', 'advanced'):
        return jsonify({"error": "Invalid difficulty. Choose: beginner, intermediate, or advanced"}), 400

    if not GEMINI_AVAILABLE:
        return jsonify({"error": "AI quiz engine is not configured. Please set GEMINI_API_KEY in your .env file."}), 503

    # Generate fresh questions from Gemini (returns (questions, error) tuple)
    result = generate_ai_questions(skill_name, difficulty)
    if isinstance(result, tuple):
        questions, gen_error = result
    else:
        questions, gen_error = result, None

    if not questions:
        error_msg = gen_error or f"Could not generate questions for '{skill_name}'. Please try again."
        return jsonify({"error": error_msg}), 503

    # Shuffle option order for each question to prevent pattern recognition
    for q in questions:
        correct_text = q['options'][q['answer']]
        random.shuffle(q['options'])
        q['answer'] = q['options'].index(correct_text)

    selected = questions[:QUIZ_QUESTION_COUNT]
    time_per_q = QUIZ_TIME_MAP.get(difficulty, 15)

    # Store answers server-side ONLY â€” never send to client
    session['quiz_answers']        = [q['answer'] for q in selected]
    session['quiz_skill']          = skill_name
    session['quiz_difficulty']     = difficulty
    session['quiz_question_count'] = len(selected)

    questions_for_client = [{'q': q['q'], 'options': q['options']} for q in selected]

    return jsonify({
        'questions':        questions_for_client,
        'time_per_question': time_per_q,
        'skill':            skill_name,
        'difficulty':       difficulty,
        'total':            len(selected),
        'source':           'ai'
    }), 200





@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    if 'quiz_answers' not in session:
        db = get_db()
        recent = db.execute('''
            SELECT skill_name, difficulty, score, total, passed, xp_earned, tab_switches, created_at 
            FROM quiz_attempts 
            WHERE user_id = ? 
            ORDER BY id DESC LIMIT 1
        ''', (session['user_id'],)).fetchone()
        if recent:
            return jsonify({
                "correct": recent['score'],
                "effective_correct": recent['score'],
                "total": recent['total'],
                "passed": bool(recent['passed']),
                "xp_earned": recent['xp_earned'],
                "skill": recent['skill_name'],
                "difficulty": recent['difficulty'],
                "tab_switches": recent['tab_switches']
            }), 200
        return jsonify({"error": "No active quiz session"}), 400
    
    data = request.json
    user_answers = data.get('answers', [])
    tab_switches = data.get('tab_switches', 0)
    correct_answers = session.pop('quiz_answers')
    skill_name = session.pop('quiz_skill', 'unknown')
    difficulty = session.pop('quiz_difficulty', 'beginner')
    total = session.pop('quiz_question_count', len(correct_answers))
    
    correct = sum(1 for i in range(min(len(user_answers), len(correct_answers))) if user_answers[i] == correct_answers[i])
    
    # Penalize tab switches: subtract 1 correct for every 2 tab switches
    penalty = tab_switches // 2
    effective_correct = max(0, correct - penalty)
    
    passed = effective_correct >= (total * 0.6)
    
    # XP scaling by difficulty
    xp_multiplier = {'beginner': 10, 'intermediate': 20, 'advanced': 35}
    xp_earned = effective_correct * xp_multiplier.get(difficulty, 10) if passed else effective_correct * 3
    
    db = get_db()
    user = db.execute('SELECT xp, level FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    new_xp = user['xp'] + xp_earned
    new_level = (new_xp // 100) + 1
    leveled_up = new_level > user['level']
    
    db.execute('UPDATE users SET xp = ?, level = ? WHERE id = ?', (new_xp, new_level, session['user_id']))
    
    # Record attempt
    db.execute('INSERT INTO quiz_attempts (user_id, skill_name, difficulty, score, total, passed, xp_earned, tab_switches) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
               (session['user_id'], skill_name, difficulty, effective_correct, total, passed, xp_earned, tab_switches))
    
    # Update verification if passed (resets 180-day heartbeat)
    if passed:
        level_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        existing = db.execute('SELECT verified_level FROM skill_verifications WHERE user_id = ? AND LOWER(skill_name) = ?', (session['user_id'], skill_name)).fetchone()
        if existing:
            new_level = difficulty if level_order.get(difficulty, 0) > level_order.get(existing['verified_level'], 0) else existing['verified_level']
            db.execute('''
                UPDATE skill_verifications 
                SET verified_level = ?, verified_at = CURRENT_TIMESTAMP, 
                    last_activity_at = CURRENT_TIMESTAMP, activity_type = 'quiz' 
                WHERE user_id = ? AND LOWER(skill_name) = ?
            ''', (new_level, session['user_id'], skill_name))
        else:
            db.execute('''
                INSERT INTO skill_verifications (user_id, skill_name, verified_level, verified_at, last_activity_at, activity_type, sessions_taught) 
                VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'quiz', 0)
            ''', (session['user_id'], skill_name, difficulty))
    
    db.commit()
    
    return jsonify({
        "correct": correct,
        "effective_correct": effective_correct,
        "total": total,
        "passed": passed,
        "xp_earned": xp_earned,
        "new_xp": new_xp,
        "new_level": new_level,
        "leveled_up": leveled_up,
        "skill": skill_name,
        "difficulty": difficulty,
        "tab_switches": tab_switches,
        "penalty_applied": penalty > 0
    }), 200


@app.route('/api/quiz/history', methods=['GET'])
def quiz_history():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    db = get_db()
    attempts = db.execute('SELECT skill_name, difficulty, score, total, passed, xp_earned, tab_switches, created_at FROM quiz_attempts WHERE user_id = ? ORDER BY created_at DESC LIMIT 20', (session['user_id'],)).fetchall()
    return jsonify({"history": [dict(a) for a in attempts]}), 200


# =============================================================================
# SKILL DECAY (PROOF-OF-WORK HALF-LIFE) & A.E.E. PROTOCOL
# =============================================================================

DECAY_WINDOW_DAYS = 180   # 6-month proof-of-work half-life
WARNING_WINDOW_DAYS = 60  # Warning alert when <= 60 days remaining

def calculate_decay_metrics(activity_timestamp_str):
    """
    Computes dynamic decay health for a verified skill based on elapsed time
    since its last Proof-of-Work (quiz pass or confirmed A.E.E. teaching session).
    """
    if not activity_timestamp_str:
        activity_timestamp_str = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    clean_str = str(activity_timestamp_str).replace('T', ' ').split('.')[0]
    try:
        activity_dt = datetime.strptime(clean_str, '%Y-%m-%d %H:%M:%S')
    except Exception:
        activity_dt = datetime.utcnow()

    now_dt = datetime.utcnow()
    days_elapsed = max(0, int((now_dt - activity_dt).total_seconds() / 86400))
    days_remaining = max(0, DECAY_WINDOW_DAYS - days_elapsed)
    health_percent = min(100, max(0, round((days_remaining / DECAY_WINDOW_DAYS) * 100)))

    if days_remaining == 0:
        decay_status = 'decayed'       # Dormant / Stale verification
    elif days_remaining <= WARNING_WINDOW_DAYS:
        decay_status = 'expiring_soon' # Amber warning: needs A.E.E. teaching
    else:
        decay_status = 'active'        # Healthy active heartbeat

    return {
        'days_elapsed': days_elapsed,
        'days_remaining': days_remaining,
        'health_percent': health_percent,
        'decay_status': decay_status,
        'is_active': decay_status != 'decayed'
    }


@app.route('/api/quiz/verified', methods=['GET'])
def verified_skills():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    db = get_db()
    rows = db.execute('''
        SELECT id, skill_name, verified_level, verified_at, last_activity_at, 
               activity_type, sessions_taught 
        FROM skill_verifications 
        WHERE user_id = ?
        ORDER BY verified_at DESC
    ''', (session['user_id'],)).fetchall()

    verified = []
    for r in rows:
        d = dict(r)
        metrics = calculate_decay_metrics(d.get('last_activity_at') or d.get('verified_at'))
        d.update(metrics)
        verified.append(d)

    return jsonify({"verified": verified}), 200


@app.route('/api/aee/pending', methods=['GET'])
def get_pending_aee():
    """Returns incoming and outbound pending A.E.E. confirmation requests."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    db = get_db()
    uid = session['user_id']

    # Incoming: where current user is the LEARNER (needs to confirm the session)
    incoming_rows = db.execute('''
        SELECT a.id, a.teacher_id, a.learner_id, a.skill_name, a.duration_minutes, 
               a.topic_notes, a.status, a.created_at,
               u.full_name AS teacher_name, u.username AS teacher_username, u.avatar_color AS teacher_avatar
        FROM aee_sessions a
        JOIN users u ON a.teacher_id = u.id
        WHERE a.learner_id = ? AND a.status = 'pending'
        ORDER BY a.created_at DESC
    ''', (uid,)).fetchall()

    # Outbound: where current user is the TEACHER (waiting for learner to confirm)
    outbound_rows = db.execute('''
        SELECT a.id, a.teacher_id, a.learner_id, a.skill_name, a.duration_minutes, 
               a.topic_notes, a.status, a.created_at,
               u.full_name AS learner_name, u.username AS learner_username, u.avatar_color AS learner_avatar
        FROM aee_sessions a
        JOIN users u ON a.learner_id = u.id
        WHERE a.teacher_id = ? AND a.status = 'pending'
        ORDER BY a.created_at DESC
    ''', (uid,)).fetchall()

    return jsonify({
        "incoming": [dict(r) for r in incoming_rows],
        "outbound": [dict(r) for r in outbound_rows]
    }), 200


@app.route('/api/aee/log', methods=['POST'])
def log_aee_session():
    """Teacher logs an Applied Exchange & Execution (A.E.E.) session with a peer."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    teacher_id = session['user_id']
    data = request.json or {}
    learner_id = data.get('learner_id')
    skill_name = (data.get('skill_name') or '').strip().lower()
    duration = int(data.get('duration_minutes') or 30)
    topic_notes = (data.get('topic_notes') or '').strip()

    if not learner_id or not skill_name:
        return jsonify({"error": "Learner and skill name are required"}), 400
    if int(learner_id) == teacher_id:
        return jsonify({"error": "You cannot log an A.E.E. session with yourself"}), 400

    db = get_db()

    learner = db.execute('SELECT id, full_name, username FROM users WHERE id = ?', (learner_id,)).fetchone()
    if not learner:
        return jsonify({"error": "Selected learning partner not found"}), 404

    # Require teacher to have this skill in skill_verifications
    verif = db.execute('SELECT id FROM skill_verifications WHERE user_id = ? AND LOWER(skill_name) = ?', (teacher_id, skill_name)).fetchone()
    if not verif:
        return jsonify({"error": "You can only renew verification for skills you have verified (e.g. via quiz)."}), 400

    # Prevent duplicate pending requests for the same pair and skill
    dup = db.execute('''
        SELECT id FROM aee_sessions 
        WHERE teacher_id = ? AND learner_id = ? AND LOWER(skill_name) = ? AND status = "pending"
    ''', (teacher_id, learner_id, skill_name)).fetchone()
    if dup:
        return jsonify({"error": "A pending confirmation request already exists for this peer and skill."}), 400

    db.execute('''
        INSERT INTO aee_sessions (teacher_id, learner_id, skill_name, duration_minutes, topic_notes, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
    ''', (teacher_id, learner_id, skill_name, duration, topic_notes))

    session_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]
    db.commit()

    teacher_user = db.execute('SELECT full_name, username FROM users WHERE id = ?', (teacher_id,)).fetchone()
    t_name = teacher_user['full_name'] or teacher_user['username'] if teacher_user else 'A peer'
    try:
        socketio.emit('aee_request_received', {
            'session_id': session_id,
            'teacher_id': teacher_id,
            'teacher_name': t_name,
            'skill_name': skill_name,
            'duration_minutes': duration,
            'topic_notes': topic_notes
        }, room=f"user_{learner_id}")
    except Exception as e:
        print(f"[AEE Socket Error] {e}", flush=True)

    return jsonify({
        "message": f"A.E.E. session logged! Confirmation request sent to {learner['full_name'] or learner['username']}.",
        "session_id": session_id
    }), 201


@app.route('/api/aee/respond', methods=['POST'])
def respond_aee_session():
    """Learner confirms or declines an A.E.E. session, completing the proof-of-work handshake."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    learner_id = session['user_id']
    data = request.json or {}
    session_id = data.get('session_id')
    action = (data.get('action') or '').strip().lower()

    if not session_id or action not in ('confirm', 'reject'):
        return jsonify({"error": "Invalid session or action"}), 400

    db = get_db()
    sess_row = db.execute('SELECT * FROM aee_sessions WHERE id = ?', (session_id,)).fetchone()
    if not sess_row:
        return jsonify({"error": "A.E.E. session not found"}), 404

    if sess_row['learner_id'] != learner_id:
        return jsonify({"error": "You are not authorized to confirm this session"}), 403

    if sess_row['status'] != 'pending':
        return jsonify({"error": f"Session has already been {sess_row['status']}"}), 400

    teacher_id = sess_row['teacher_id']
    skill_name = sess_row['skill_name'].lower()

    if action == 'reject':
        db.execute('UPDATE aee_sessions SET status = "rejected" WHERE id = ?', (session_id,))
        db.commit()
        try:
            socketio.emit('aee_request_declined', {
                'session_id': session_id,
                'skill_name': skill_name
            }, room=f"user_{teacher_id}")
        except Exception:
            pass
        return jsonify({"message": "Session confirmation declined."}), 200

    # action == 'confirm'
    # 7-day rate-limit check for same pair & skill (prevents rapid collusion farming)
    recent = db.execute('''
        SELECT id, confirmed_at FROM aee_sessions 
        WHERE teacher_id = ? AND learner_id = ? AND LOWER(skill_name) = ?
          AND status = 'confirmed' AND id != ?
          AND confirmed_at >= datetime('now', '-7 days')
    ''', (teacher_id, learner_id, skill_name, session_id)).fetchone()

    rate_limited = recent is not None

    db.execute('UPDATE aee_sessions SET status = "confirmed", confirmed_at = CURRENT_TIMESTAMP WHERE id = ?', (session_id,))

    # Reset the 180-day heartbeat for teacher's verified skill!
    db.execute('''
        UPDATE skill_verifications 
        SET last_activity_at = CURRENT_TIMESTAMP,
            activity_type = 'aee_session',
            sessions_taught = COALESCE(sessions_taught, 0) + 1
        WHERE user_id = ? AND LOWER(skill_name) = ?
    ''', (teacher_id, skill_name))

    # Award XP and session counts
    if not rate_limited:
        db.execute('UPDATE users SET xp = xp + 25, skills_taught = skills_taught + 1, total_sessions = total_sessions + 1 WHERE id = ?', (teacher_id,))
        db.execute('UPDATE users SET xp = xp + 15, skills_learned = skills_learned + 1, total_sessions = total_sessions + 1 WHERE id = ?', (learner_id,))
    else:
        db.execute('UPDATE users SET skills_taught = skills_taught + 1, total_sessions = total_sessions + 1 WHERE id = ?', (teacher_id,))
        db.execute('UPDATE users SET skills_learned = skills_learned + 1, total_sessions = total_sessions + 1 WHERE id = ?', (learner_id,))

    db.commit()

    learner_user = db.execute('SELECT full_name, username FROM users WHERE id = ?', (learner_id,)).fetchone()
    l_name = learner_user['full_name'] or learner_user['username'] if learner_user else 'Your peer'
    try:
        socketio.emit('aee_request_confirmed', {
            'session_id': session_id,
            'learner_name': l_name,
            'skill_name': skill_name,
            'days_remaining': 180
        }, room=f"user_{teacher_id}")
    except Exception as e:
        print(f"[AEE Socket Error] {e}", flush=True)

    return jsonify({
        "message": "Proof-of-Work confirmed! Skill heartbeat reset to 180 days.",
        "xp_awarded": 15 if not rate_limited else 0
    }), 200


# =============================================================================
# EXCHANGE SESSIONS, ESCROW & RATINGS LIFECYCLE (PILLAR 1)
# =============================================================================

def init_sessions_db(db):
    """Runtime safety DDL to guarantee exchange_sessions and session_reviews exist."""
    db.execute('''
        CREATE TABLE IF NOT EXISTS exchange_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            learner_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            duration_minutes INTEGER DEFAULT 60,
            credit_cost REAL DEFAULT 1.0,
            scheduled_at TIMESTAMP,
            topic_notes TEXT DEFAULT '',
            status TEXT DEFAULT 'pending',
            escrow_status TEXT DEFAULT 'held',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id),
            FOREIGN KEY (learner_id) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS session_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            reviewer_id INTEGER NOT NULL,
            reviewee_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
            tags TEXT DEFAULT '[]',
            comment TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES exchange_sessions(id),
            FOREIGN KEY (reviewer_id) REFERENCES users(id),
            FOREIGN KEY (reviewee_id) REFERENCES users(id),
            UNIQUE(session_id, reviewer_id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS teaching_call_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            learner_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            session_id INTEGER,
            duration_seconds INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES users(id),
            FOREIGN KEY (learner_id) REFERENCES users(id)
        )
    ''')

    cursor = db.cursor()
    cursor.execute("PRAGMA table_info(users)")
    u_cols = [row[1] for row in cursor.fetchall()]
    if 'total_teaching_seconds' not in u_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN total_teaching_seconds INTEGER DEFAULT 0")
    if 'total_learning_seconds' not in u_cols:
        cursor.execute("ALTER TABLE users ADD COLUMN total_learning_seconds INTEGER DEFAULT 0")

    cursor.execute("PRAGMA table_info(exchange_sessions)")
    s_cols = [row[1] for row in cursor.fetchall()]
    if 'actual_duration_seconds' not in s_cols:
        cursor.execute("ALTER TABLE exchange_sessions ADD COLUMN actual_duration_seconds INTEGER DEFAULT 0")

    db.commit()


@app.route('/api/sessions/book', methods=['POST'])
def book_session():
    """Book a skill exchange session with a peer.
    Deducts credit cost from learner and locks it in escrow until session completion.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    learner_id = session['user_id']
    data = request.json or {}
    teacher_id = data.get('teacher_id')
    skill_name = (data.get('skill_name') or '').strip()
    raw_scheduled = data.get('scheduled_at')
    scheduled_at = None
    if raw_scheduled and isinstance(raw_scheduled, str) and raw_scheduled.strip():
        scheduled_at = raw_scheduled.strip()
    topic_notes = (data.get('topic_notes') or '').strip()

    if not teacher_id or not skill_name:
        return jsonify({"error": "Teacher and skill name are required"}), 400

    teacher_id = int(teacher_id)
    if teacher_id == learner_id:
        return jsonify({"error": "You cannot book a session with yourself"}), 400

    # Pricing: 30 mins = 0.5 credits, 60 mins = 1.0 credit
    credit_cost = 0.5 if duration <= 30 else 1.0

    db = get_db()
    init_sessions_db(db)

    # 1. Verify teacher exists
    teacher = db.execute('SELECT id, full_name, username FROM users WHERE id = ?', (teacher_id,)).fetchone()
    if not teacher:
        return jsonify({"error": "Teacher not found"}), 404

    # 2. Check learner credit balance
    learner = db.execute('SELECT id, full_name, username, avatar_color, time_credits FROM users WHERE id = ?', (learner_id,)).fetchone()
    if not learner:
        return jsonify({"error": "Learner not found"}), 404

    avail_credits = float(learner['time_credits'] or 0.0)
    if avail_credits < credit_cost:
        return jsonify({
            "error": f"Insufficient time credits. You have {avail_credits:.1f} credits but this session requires {credit_cost:.1f}."
        }), 400

    # 3. Deduct credit from learner (Escrow Lock)
    db.execute('UPDATE users SET time_credits = ROUND(time_credits - ?, 2) WHERE id = ?', (credit_cost, learner_id))

    # 4. Create exchange_sessions row
    cursor = db.execute('''
        INSERT INTO exchange_sessions (teacher_id, learner_id, skill_name, duration_minutes, credit_cost, scheduled_at, topic_notes, status, escrow_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', 'held')
    ''', (teacher_id, learner_id, skill_name, duration, credit_cost, scheduled_at, topic_notes))
    db.commit()
    session_id = cursor.lastrowid

    session_payload = {
        "id": session_id,
        "teacher_id": teacher_id,
        "learner_id": learner_id,
        "learner_name": learner['full_name'] or learner['username'],
        "learner_username": learner['username'],
        "learner_avatar": learner['avatar_color'],
        "teacher_name": teacher['full_name'] or teacher['username'],
        "teacher_username": teacher['username'],
        "skill_name": skill_name,
        "duration_minutes": duration,
        "credit_cost": credit_cost,
        "scheduled_at": scheduled_at,
        "topic_notes": topic_notes,
        "status": "pending",
        "escrow_status": "held"
    }

    # Real-time socket notification to teacher
    try:
        socketio.emit('session_requested', session_payload, room=f"user_{teacher_id}")
    except Exception as e:
        app.logger.warning(f"Socket emit error: {e}")

    return jsonify({
        "status": "created",
        "message": f"Session requested! {credit_cost:.1f} Time Credit held in escrow.",
        "session": session_payload
    }), 201


@app.route('/api/sessions', methods=['GET'])
def get_user_sessions():
    """Fetch all exchange sessions for the authenticated user, enriched with peer details and review status."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    uid = session['user_id']
    status_filter = request.args.get('status', 'all').lower()

    db = get_db()
    init_sessions_db(db)

    query = '''
        SELECT s.*,
               t.full_name AS teacher_name, t.username AS teacher_username, t.avatar_color AS teacher_avatar, t.department AS teacher_dept,
               l.full_name AS learner_name, l.username AS learner_username, l.avatar_color AS learner_avatar, l.department AS learner_dept
        FROM exchange_sessions s
        JOIN users t ON s.teacher_id = t.id
        JOIN users l ON s.learner_id = l.id
        WHERE (s.teacher_id = ? OR s.learner_id = ?)
    '''
    params = [uid, uid]

    if status_filter == 'upcoming':
        query += " AND s.status IN ('accepted', 'active')"
    elif status_filter == 'pending':
        query += " AND s.status = 'pending'"
    elif status_filter == 'completed':
        query += " AND s.status = 'completed'"

    query += " ORDER BY s.created_at DESC"

    rows = db.execute(query, params).fetchall()
    results = []

    for r in rows:
        d = dict(r)
        is_teacher = (r['teacher_id'] == uid)
        d['my_role'] = 'teacher' if is_teacher else 'learner'
        d['peer_id'] = r['learner_id'] if is_teacher else r['teacher_id']
        d['peer_name'] = r['learner_name'] if is_teacher else r['teacher_name']
        d['peer_username'] = r['learner_username'] if is_teacher else r['teacher_username']
        d['peer_avatar'] = r['learner_avatar'] if is_teacher else r['teacher_avatar']
        d['peer_dept'] = r['learner_dept'] if is_teacher else r['teacher_dept']

        # Check if current user has reviewed this session
        rev = db.execute(
            'SELECT id, rating, comment, tags FROM session_reviews WHERE session_id = ? AND reviewer_id = ?',
            (r['id'], uid)
        ).fetchone()
        d['my_review'] = dict(rev) if rev else None

        results.append(d)

    return jsonify({"sessions": results}), 200


@app.route('/api/sessions/<int:session_id>/respond', methods=['PUT'])
def respond_session(session_id):
    """Teacher accepts or declines a requested session.
    If declined: immediately refunds escrow credit to the learner.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    teacher_id = session['user_id']
    data = request.json or {}
    action = (data.get('action') or '').strip().lower()

    if action not in ('accept', 'reject'):
        return jsonify({"error": "Action must be 'accept' or 'reject'"}), 400

    db = get_db()
    init_sessions_db(db)

    sess_row = db.execute('SELECT * FROM exchange_sessions WHERE id = ?', (session_id,)).fetchone()
    if not sess_row:
        return jsonify({"error": "Session not found"}), 404

    if sess_row['teacher_id'] != teacher_id:
        return jsonify({"error": "Only the teacher can respond to this booking request"}), 403

    if sess_row['status'] != 'pending':
        return jsonify({"error": f"Session is already {sess_row['status']}"}), 400

    learner_id = sess_row['learner_id']
    credit_cost = float(sess_row['credit_cost'] or 1.0)

    if action == 'accept':
        db.execute('UPDATE exchange_sessions SET status = "accepted" WHERE id = ?', (session_id,))
        db.commit()

        teacher_user = db.execute('SELECT full_name, username FROM users WHERE id = ?', (teacher_id,)).fetchone()
        teacher_name = (teacher_user['full_name'] or teacher_user['username']) if teacher_user else 'Your mentor'

        try:
            socketio.emit('session_accepted', {
                "session_id": session_id,
                "skill_name": sess_row['skill_name'],
                "teacher_name": teacher_name,
                "teacher_id": teacher_id,
                "scheduled_at": sess_row['scheduled_at']
            }, room=f"user_{learner_id}")
        except Exception:
            pass

        return jsonify({"message": "Session accepted! Ready for skill exchange.", "status": "accepted"}), 200

    else:  # reject
        # Refund held escrow to learner
        db.execute('UPDATE users SET time_credits = ROUND(time_credits + ?, 2) WHERE id = ?', (credit_cost, learner_id))
        db.execute('UPDATE exchange_sessions SET status = "rejected", escrow_status = "refunded" WHERE id = ?', (session_id,))
        db.commit()

        try:
            socketio.emit('session_rejected', {
                "session_id": session_id,
                "skill_name": sess_row['skill_name'],
                "refunded_credits": credit_cost
            }, room=f"user_{learner_id}")
        except Exception:
            pass

        return jsonify({"message": f"Session declined. {credit_cost:.1f} Time Credit refunded to learner.", "status": "rejected"}), 200


@app.route('/api/sessions/<int:session_id>/cancel', methods=['POST'])
def cancel_session(session_id):
    """Cancel a pending or accepted session.
    Automatically refunds any held escrow credits to the learner.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    uid = session['user_id']
    db = get_db()
    init_sessions_db(db)

    sess_row = db.execute('SELECT * FROM exchange_sessions WHERE id = ?', (session_id,)).fetchone()
    if not sess_row:
        return jsonify({"error": "Session not found"}), 404

    if uid not in (sess_row['teacher_id'], sess_row['learner_id']):
        return jsonify({"error": "Unauthorized to cancel this session"}), 403

    if sess_row['status'] in ('completed', 'cancelled', 'rejected'):
        return jsonify({"error": f"Session cannot be cancelled because it is already {sess_row['status']}"}), 400

    credit_cost = float(sess_row['credit_cost'] or 1.0)
    learner_id = sess_row['learner_id']
    teacher_id = sess_row['teacher_id']

    # Refund held escrow if applicable
    if sess_row['escrow_status'] == 'held':
        db.execute('UPDATE users SET time_credits = ROUND(time_credits + ?, 2) WHERE id = ?', (credit_cost, learner_id))

    db.execute('UPDATE exchange_sessions SET status = "cancelled", escrow_status = "refunded" WHERE id = ?', (session_id,))
    db.commit()

    other_id = learner_id if uid == teacher_id else teacher_id
    try:
        socketio.emit('session_cancelled', {
            "session_id": session_id,
            "cancelled_by": uid
        }, room=f"user_{other_id}")
    except Exception:
        pass

    return jsonify({"message": "Session cancelled. Held credits have been refunded.", "status": "cancelled"}), 200


@app.route('/api/sessions/<int:session_id>/complete', methods=['POST'])
def complete_session(session_id):
    """Complete a session (either via chat or live exchange).
    Releases escrow credit to the teacher, awards XP, resets skill decay timer,
    and prompts both peers to leave a review.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    uid = session['user_id']
    db = get_db()
    init_sessions_db(db)

    sess_row = db.execute('SELECT * FROM exchange_sessions WHERE id = ?', (session_id,)).fetchone()
    if not sess_row:
        return jsonify({"error": "Session not found"}), 404

    if uid not in (sess_row['teacher_id'], sess_row['learner_id']):
        return jsonify({"error": "Unauthorized"}), 403

    if sess_row['status'] == 'completed':
        return jsonify({"message": "Session already completed", "status": "completed"}), 200

    teacher_id = sess_row['teacher_id']
    learner_id = sess_row['learner_id']
    credit_cost = float(sess_row['credit_cost'] or 1.0)
    skill_name = (sess_row['skill_name'] or '').lower()

    # 1. Release Escrow Credit to Teacher
    if sess_row['escrow_status'] == 'held':
        db.execute('UPDATE users SET time_credits = ROUND(time_credits + ?, 2) WHERE id = ?', (credit_cost, teacher_id))

    # 2. Award XP and Increment Stats
    # Teacher: +25 XP, skills_taught + 1, total_sessions + 1
    db.execute('''
        UPDATE users 
        SET xp = xp + 25, 
            skills_taught = skills_taught + 1, 
            total_sessions = total_sessions + 1,
            streak_count = streak_count + 1
        WHERE id = ?
    ''', (teacher_id,))

    # Learner: +15 XP, skills_learned + 1, total_sessions + 1
    db.execute('''
        UPDATE users 
        SET xp = xp + 15, 
            skills_learned = skills_learned + 1, 
            total_sessions = total_sessions + 1,
            streak_count = streak_count + 1
        WHERE id = ?
    ''', (learner_id,))

    # 3. Reset 180-Day Skill Decay Heartbeat for Teacher if verified
    db.execute('''
        UPDATE skill_verifications 
        SET last_activity_at = CURRENT_TIMESTAMP,
            activity_type = 'exchange_session',
            sessions_taught = COALESCE(sessions_taught, 0) + 1
        WHERE user_id = ? AND LOWER(skill_name) = ?
    ''', (teacher_id, skill_name))

    # 4. Mark Session Completed
    db.execute('''
        UPDATE exchange_sessions 
        SET status = "completed", 
            escrow_status = "released", 
            completed_at = CURRENT_TIMESTAMP 
        WHERE id = ?
    ''', (session_id,))
    db.commit()

    # Real-time event prompting review modal
    complete_payload = {
        "session_id": session_id,
        "teacher_id": teacher_id,
        "learner_id": learner_id,
        "skill_name": sess_row['skill_name'],
        "credit_transferred": credit_cost
    }
    try:
        socketio.emit('session_completed', complete_payload, room=f"user_{teacher_id}")
        socketio.emit('session_completed', complete_payload, room=f"user_{learner_id}")
    except Exception as e:
        app.logger.warning(f"Socket emit error: {e}")

    return jsonify({
        "status": "completed",
        "message": f"Session completed! {credit_cost:.1f} Time Credit transferred to teacher and XP awarded.",
        "credit_transferred": credit_cost
    }), 200


@app.route('/api/sessions/<int:session_id>/review', methods=['POST'])
def submit_session_review(session_id):
    """Submit a 1-5 star review with tags and comments after a completed session.
    Automatically recalculates the reviewee's rating_avg and rating_count.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    reviewer_id = session['user_id']
    data = request.json or {}
    rating = int(data.get('rating') or 5)
    tags = data.get('tags') or []
    comment = (data.get('comment') or '').strip()

    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    db = get_db()
    init_sessions_db(db)

    sess_row = db.execute('SELECT * FROM exchange_sessions WHERE id = ?', (session_id,)).fetchone()
    if not sess_row:
        return jsonify({"error": "Session not found"}), 404

    if sess_row['status'] != 'completed':
        return jsonify({"error": "Reviews can only be submitted for completed sessions"}), 400

    if reviewer_id not in (sess_row['teacher_id'], sess_row['learner_id']):
        return jsonify({"error": "Unauthorized to review this session"}), 403

    # Determine reviewee & role
    if reviewer_id == sess_row['learner_id']:
        reviewee_id = sess_row['teacher_id']
        role = 'learner_rating_teacher'
    else:
        reviewee_id = sess_row['learner_id']
        role = 'teacher_rating_learner'

    # Check for existing review
    existing = db.execute(
        'SELECT id FROM session_reviews WHERE session_id = ? AND reviewer_id = ?',
        (session_id, reviewer_id)
    ).fetchone()
    if existing:
        return jsonify({"error": "You have already reviewed this session"}), 400

    tags_json = _json.dumps(tags)

    # 1. Insert Review
    db.execute('''
        INSERT INTO session_reviews (session_id, reviewer_id, reviewee_id, role, rating, tags, comment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (session_id, reviewer_id, reviewee_id, role, rating, tags_json, comment))

    # 2. Recalculate Reviewee's rating_avg and rating_count
    db.execute('''
        UPDATE users 
        SET rating_avg = (SELECT ROUND(AVG(rating), 2) FROM session_reviews WHERE reviewee_id = ?),
            rating_count = (SELECT COUNT(*) FROM session_reviews WHERE reviewee_id = ?)
        WHERE id = ?
    ''', (reviewee_id, reviewee_id, reviewee_id))
    db.commit()

    # Get updated stats
    updated_user = db.execute('SELECT rating_avg, rating_count FROM users WHERE id = ?', (reviewee_id,)).fetchone()

    return jsonify({
        "status": "created",
        "message": "Review submitted successfully!",
        "new_rating_avg": updated_user['rating_avg'] if updated_user else rating,
        "new_rating_count": updated_user['rating_count'] if updated_user else 1
    }), 201


@app.route('/api/sessions/<int:session_id>/reviews', methods=['GET'])
def get_session_reviews(session_id):
    """Retrieve all reviews attached to a session."""
    db = get_db()
    init_sessions_db(db)

    rows = db.execute('''
        SELECT r.*, u.full_name AS reviewer_name, u.username AS reviewer_username, u.avatar_color AS reviewer_avatar
        FROM session_reviews r
        JOIN users u ON r.reviewer_id = u.id
        WHERE r.session_id = ?
        ORDER BY r.created_at ASC
    ''', (session_id,)).fetchall()

    reviews = []
    for r in rows:
        d = dict(r)
        try:
            d['tags'] = _json.loads(d['tags']) if d['tags'] else []
        except Exception:
            d['tags'] = []
        reviews.append(d)

    return jsonify({"reviews": reviews}), 200


@app.route('/api/sessions/record-teaching-time', methods=['POST'])
def record_teaching_time():
    """Records duration of a completed/ongoing video teaching call in the teacher's official record.
    Increments total_teaching_seconds for teacher and total_learning_seconds for learner,
    creates an entry in teaching_call_logs, renews skill decay heartbeat, and notifies peers via socket.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    current_user_id = session['user_id']
    data = request.json or {}
    teacher_id = data.get('teacher_id')
    learner_id = data.get('learner_id')
    duration_seconds = int(data.get('duration_seconds') or 0)
    skill_name = (data.get('skill_name') or 'Skill Exchange').strip()
    session_id = data.get('session_id')

    if not teacher_id or not learner_id:
        return jsonify({"error": "teacher_id and learner_id are required"}), 400

    teacher_id = int(teacher_id)
    learner_id = int(learner_id)

    # Validate caller is part of the session/call
    if current_user_id not in (teacher_id, learner_id):
        return jsonify({"error": "Unauthorized to log duration for this call"}), 403

    if duration_seconds < 5:
        return jsonify({"error": "Call duration too short to record (< 5 seconds)"}), 400

    db = get_db()
    init_sessions_db(db)

    # Deduplicate: Check if a matching log was already recorded in the last 20 seconds (e.g. by peer hanging up first)
    recent = db.execute('''
        SELECT id, duration_seconds FROM teaching_call_logs
        WHERE teacher_id = ? AND learner_id = ? AND skill_name = ?
        AND created_at >= datetime('now', '-20 seconds')
        ORDER BY id DESC LIMIT 1
    ''', (teacher_id, learner_id, skill_name)).fetchone()

    if recent:
        updated_teacher = db.execute('SELECT total_teaching_seconds, full_name, username FROM users WHERE id = ?', (teacher_id,)).fetchone()
        tot_teach = (updated_teacher['total_teaching_seconds'] or 0) if updated_teacher else duration_seconds
        tot_hours = tot_teach // 3600
        tot_mins = (tot_teach % 3600) // 60
        formatted_total_teaching = f"{tot_hours}h {tot_mins}m" if tot_hours > 0 else f"{tot_mins}m"
        minutes = duration_seconds // 60
        secs = duration_seconds % 60
        formatted_duration = f"{minutes}m {secs}s" if minutes > 0 else f"{secs}s"
        return jsonify({
            "status": "success",
            "message": "Call duration already recorded.",
            "recorded_duration_seconds": duration_seconds,
            "recorded_duration_formatted": formatted_duration,
            "total_teaching_seconds": tot_teach,
            "total_teaching_formatted": formatted_total_teaching
        }), 200

    # 1. Update teacher total_teaching_seconds
    db.execute('''
        UPDATE users 
        SET total_teaching_seconds = COALESCE(total_teaching_seconds, 0) + ? 
        WHERE id = ?
    ''', (duration_seconds, teacher_id))

    # 2. Update learner total_learning_seconds
    db.execute('''
        UPDATE users 
        SET total_learning_seconds = COALESCE(total_learning_seconds, 0) + ? 
        WHERE id = ?
    ''', (duration_seconds, learner_id))

    # 3. If tied to an exchange_session, record actual_duration_seconds
    if session_id:
        try:
            db.execute('''
                UPDATE exchange_sessions 
                SET actual_duration_seconds = COALESCE(actual_duration_seconds, 0) + ? 
                WHERE id = ?
            ''', (duration_seconds, int(session_id)))
        except Exception as e:
            app.logger.warning(f"Error updating exchange_session duration: {e}")

    # 4. Insert into teaching_call_logs
    db.execute('''
        INSERT INTO teaching_call_logs (teacher_id, learner_id, skill_name, session_id, duration_seconds)
        VALUES (?, ?, ?, ?, ?)
    ''', (teacher_id, learner_id, skill_name, session_id, duration_seconds))

    # 5. Heartbeat skill verification for teacher (keeps decay timer active)
    if skill_name:
        db.execute('''
            UPDATE skill_verifications 
            SET last_activity_at = CURRENT_TIMESTAMP,
                activity_type = 'live_teaching_call',
                sessions_taught = COALESCE(sessions_taught, 0) + 1
            WHERE user_id = ? AND LOWER(skill_name) = LOWER(?)
        ''', (teacher_id, skill_name))

    db.commit()

    # 6. Fetch updated record stats
    updated_teacher = db.execute('SELECT total_teaching_seconds, full_name, username FROM users WHERE id = ?', (teacher_id,)).fetchone()
    updated_learner = db.execute('SELECT total_learning_seconds, full_name, username FROM users WHERE id = ?', (learner_id,)).fetchone()

    minutes = duration_seconds // 60
    secs = duration_seconds % 60
    formatted_duration = f"{minutes}m {secs}s" if minutes > 0 else f"{secs}s"

    tot_teach = (updated_teacher['total_teaching_seconds'] or 0) if updated_teacher else duration_seconds
    tot_hours = tot_teach // 3600
    tot_mins = (tot_teach % 3600) // 60
    formatted_total_teaching = f"{tot_hours}h {tot_mins}m" if tot_hours > 0 else f"{tot_mins}m"

    t_name = (updated_teacher['full_name'] or updated_teacher['username']) if updated_teacher else 'Teacher'
    l_name = (updated_learner['full_name'] or updated_learner['username']) if updated_learner else 'Learner'

    # Send notifications to both users
    create_notification(
        teacher_id, learner_id, 'teaching_recorded',
        'Teaching Time Recorded!',
        f"You taught {skill_name} to {l_name} for {formatted_duration}. Recorded to your campus profile!",
        '/profile'
    )
    create_notification(
        learner_id, teacher_id, 'learning_completed',
        'Learning Session Completed!',
        f"You completed {formatted_duration} learning {skill_name} with {t_name}.",
        f'/chat?id={teacher_id}'
    )

    event_payload = {
        "teacher_id": teacher_id,
        "teacher_name": t_name,
        "learner_id": learner_id,
        "duration_seconds": duration_seconds,
        "duration_formatted": formatted_duration,
        "skill_name": skill_name,
        "session_id": session_id,
        "total_teaching_seconds": tot_teach,
        "total_teaching_formatted": formatted_total_teaching
    }

    try:
        socketio.emit('teaching_time_recorded', event_payload, room=f"user_{teacher_id}")
        socketio.emit('teaching_time_recorded', event_payload, room=f"user_{learner_id}")
    except Exception as e:
        app.logger.warning(f"Error emitting teaching_time_recorded: {e}")

    return jsonify({
        "status": "success",
        "message": f"Successfully recorded {formatted_duration} of teaching time!",
        "recorded_duration_seconds": duration_seconds,
        "recorded_duration_formatted": formatted_duration,
        "total_teaching_seconds": tot_teach,
        "total_teaching_formatted": formatted_total_teaching
    }), 200


# =============================================================================
# RESUME & LINKEDIN-STYLE PROFILE SYSTEM
# =============================================================================

@app.route('/api/resume', methods=['GET'])
def get_resume():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session['user_id']
    db = get_db()
    
    user = db.execute('SELECT id, username, email, full_name, department, semester, bio, education, experience, github, linkedin, time_credits, skills_taught, rating_avg, xp, level, total_teaching_seconds, total_learning_seconds FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Get teaching skills
    teaches = [r['skill_name'] for r in db.execute('SELECT skill_name FROM user_skills WHERE user_id = ? AND skill_type = "teaches"', (user_id,)).fetchall()]
    
    # Get verified skills with level and Proof-of-Work decay status
    verif_rows = db.execute('''
        SELECT skill_name, verified_level, verified_at, last_activity_at, activity_type, sessions_taught 
        FROM skill_verifications WHERE user_id = ?
    ''', (user_id,)).fetchall()
    verifications = []
    for v in verif_rows:
        d = dict(v)
        metrics = calculate_decay_metrics(d.get('last_activity_at') or d.get('verified_at'))
        d.update(metrics)
        verifications.append(d)
    
    # Get or initialize user_resumes
    resume_row = db.execute('SELECT * FROM user_resumes WHERE user_id = ?', (user_id,)).fetchone()
    
    if not resume_row:
        default_experiences = []
        if user['experience']:
            default_experiences.append({
                "id": 1,
                "title": "Software Contributor & Peer Lead",
                "company": "SkillLoop Campus Network",
                "location": "Campus Node",
                "start_date": "2024",
                "end_date": "Present",
                "is_current": True,
                "description": user['experience']
            })
            
        default_education = []
        cur_year = datetime.now().year
        sem = user['semester'] or 1
        years_completed = max(0, (sem - 1) // 2)
        calc_start_year = str(cur_year - years_completed)
        calc_end_year = str(int(calc_start_year) + 4)

        if user['education']:
            default_education.append({
                "id": 1,
                "institution": user['education'],
                "degree": f"Bachelor of Technology in {user['department'] or 'Engineering'}",
                "field_of_study": user['department'] or "Engineering",
                "start_year": calc_start_year,
                "end_year": calc_end_year,
                "grade": "",
                "description": ""
            })
            
        default_settings = {
            "show_teaching_skills": False,  # User controls if teaching skills appear
            "show_verified_badges": True,
            "show_ratings": True,
            "show_credits": False,
            "template": "modern"
        }
        
        target_role = f"{user['department'] or 'Software'} Engineer"
        summary = user['bio'] or "Passionate student technologist and peer collaborator with a track record of practical problem-solving."
        
        db.execute('''
            INSERT INTO user_resumes (user_id, target_role, summary, experiences, education, certifications, projects, custom_skills, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            target_role,
            summary,
            _json.dumps(default_experiences),
            _json.dumps(default_education),
            _json.dumps([]),
            _json.dumps([]),
            _json.dumps(teaches[:5]),
            _json.dumps(default_settings)
        ))
        db.commit()
        resume_row = db.execute('SELECT * FROM user_resumes WHERE user_id = ?', (user_id,)).fetchone()

    def parse_json(val, default):
        if not val:
            return default
        try:
            return _json.loads(val)
        except Exception:
            return default

    resume_data = {
        "id": resume_row['id'],
        "user_id": resume_row['user_id'],
        "target_role": resume_row['target_role'] or '',
        "summary": resume_row['summary'] or '',
        "experiences": parse_json(resume_row['experiences'], []),
        "education": parse_json(resume_row['education'], []),
        "certifications": parse_json(resume_row['certifications'], []),
        "projects": parse_json(resume_row['projects'], []),
        "custom_skills": parse_json(resume_row['custom_skills'], []),
        "settings": parse_json(resume_row['settings'], {
            "show_teaching_skills": False,
            "show_verified_badges": True,
            "show_ratings": True,
            "show_credits": False,
            "template": "modern"
        }),
        "updated_at": resume_row['updated_at']
    }
    
    return jsonify({
        "resume": resume_data,
        "user": dict(user),
        "teaches": teaches,
        "verifications": verifications
    }), 200


@app.route('/api/resume', methods=['PUT'])
def update_resume():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session['user_id']
    data = request.json or {}
    db = get_db()
    
    target_role = data.get('target_role', '')
    summary = data.get('summary', '')
    experiences = _json.dumps(data.get('experiences', []))
    education = _json.dumps(data.get('education', []))
    certifications = _json.dumps(data.get('certifications', []))
    projects = _json.dumps(data.get('projects', []))
    custom_skills = _json.dumps(data.get('custom_skills', []))
    settings = _json.dumps(data.get('settings', {}))
    
    existing = db.execute('SELECT id FROM user_resumes WHERE user_id = ?', (user_id,)).fetchone()
    if existing:
        db.execute('''
            UPDATE user_resumes
            SET target_role = ?, summary = ?, experiences = ?, education = ?, certifications = ?, projects = ?, custom_skills = ?, settings = ?, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (target_role, summary, experiences, education, certifications, projects, custom_skills, settings, user_id))
    else:
        db.execute('''
            INSERT INTO user_resumes (user_id, target_role, summary, experiences, education, certifications, projects, custom_skills, settings)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, target_role, summary, experiences, education, certifications, projects, custom_skills, settings))
        
    db.commit()
    return jsonify({"message": "Resume saved successfully"}), 200


@app.route('/api/resume/ai-polish', methods=['POST'])
def polish_resume_with_ai():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.json or {}
    target_role = data.get('target_role', 'Software Professional')
    field = data.get('field', 'summary')
    content = data.get('content', '')
    
    if not GEMINI_AVAILABLE:
        return jsonify({"error": "AI features are not configured"}), 503
        
    if not content.strip():
        return jsonify({"error": "Content to polish cannot be empty"}), 400
        
    prompt = f"""You are an expert executive resume writer and ATS optimization specialist.
Improve and polish the following resume {field} for an applicant targeting the role: "{target_role}".
Make it impactful, active, professional, and clear with strong action verbs.
Do NOT use markdown bold/italic asterisks (no ** or *). Return clean text suitable for a resume.
Return ONLY the polished text with no meta commentary.

Content:
\"\"\"{content}\"\"\"
"""
    try:
        key = os.environ.get('GEMINI_API_KEY', '').strip()
        client = _genai.Client(api_key=key) if key else None
        if not client:
            return jsonify({"error": "GEMINI_API_KEY not configured"}), 503
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
            config=_genai_types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=1024,
            )
        )
        polished_text = response.text.strip()
        if polished_text.startswith('"') and polished_text.endswith('"'):
            polished_text = polished_text[1:-1].strip()
        return jsonify({"polished": polished_text}), 200
    except Exception as e:
        app.logger.error(f"AI Polish error: {e}")
        return jsonify({"error": f"Failed to polish content: {str(e)}"}), 500


@app.route('/api/gemini/test', methods=['GET'])
def test_gemini_endpoint():
    """Diagnostic route to test Gemini API connectivity directly from browser."""
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not key:
        return jsonify({
            "status": "error",
            "message": "GEMINI_API_KEY environment variable is empty or not set."
        }), 500
    try:
        client = _genai.Client(api_key=key)
        # 1. Discover models
        models = [m.name.replace('models/', '') for m in client.models.list()]
        # 2. Run test generation
        test_model = 'gemini-2.0-flash' if 'gemini-2.0-flash' in models else (models[0] if models else 'gemini-2.0-flash')
        resp = client.models.generate_content(
            model=test_model,
            contents="Say 'SkillLoop Gemini integration is active!' in 6 words or less."
        )
        return jsonify({
            "status": "ok",
            "active_model": test_model,
            "test_response": (resp.text or '').strip(),
            "discovered_models": models[:10]
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "key_prefix": key[:6] + "..." if len(key) >= 6 else "short"
        }), 500


@app.route('/api/institutions/search', methods=['GET'])
def search_institutions_api():
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 15, type=int)
    results = search_institutions(query, limit=limit)
    return jsonify({"results": results, "query": query}), 200


@app.route('/', methods=['GET'])
@app.route('/api/test', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "SkillLoop API",
        "message": "SkillLoop Backend is running successfully!",
        "timestamp": datetime.now().isoformat()
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    print(f"[SkillLoop] Starting server on 0.0.0.0:{port} (debug={debug})", flush=True)
    socketio.run(app, host='0.0.0.0', debug=debug, use_reloader=False, port=port)


