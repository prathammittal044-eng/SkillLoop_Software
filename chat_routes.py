import os
import sqlite3
from datetime import datetime
from flask import Blueprint, request, jsonify, session, send_from_directory, current_app
from werkzeug.utils import secure_filename
from database import get_db

chat_bp = Blueprint('chat_bp', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads', 'chat')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'zip', 'py', 'js', 'json'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_chat_db(db):
    """Ensure chat messages table exists."""
    db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT,
            message_type TEXT DEFAULT 'text', -- 'text', 'image', 'file'
            file_url TEXT,
            file_name TEXT,
            file_size TEXT,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    ''')
    db.commit()

@chat_bp.route('/api/chat/peers', methods=['GET'])
def get_chat_peers():
    """Get list of users with whom the current user has connected via loop or has chat history."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    current_user_id = session['user_id']
    db = get_db()
    init_chat_db(db)

    # Optional target peer from query parameters
    target_id = request.args.get('id', type=int)
    target_username = request.args.get('user', '').strip().lstrip('@').lower()

    # Query users who have a loop connection, exchanged messages, or explicitly requested
    query = '''
        SELECT DISTINCT u.id, u.username, u.full_name, u.department, u.semester, u.avatar_color
        FROM users u
        WHERE u.id != ? AND (
            u.id IN (
                SELECT CASE WHEN requester_id = ? THEN receiver_id ELSE requester_id END
                FROM connections
                WHERE requester_id = ? OR receiver_id = ?
            )
            OR u.id IN (
                SELECT CASE WHEN sender_id = ? THEN receiver_id ELSE sender_id END
                FROM messages
                WHERE sender_id = ? OR receiver_id = ?
            )
            OR (? IS NOT NULL AND u.id = ?)
            OR (? != '' AND LOWER(u.username) = ?)
        )
        ORDER BY u.id DESC
    '''
    users = db.execute(query, (
        current_user_id,
        current_user_id, current_user_id, current_user_id,
        current_user_id, current_user_id, current_user_id,
        target_id, target_id,
        target_username, target_username
    )).fetchall()
    
    # If user has no active chats or connections, show campus peers so chat is immediately usable
    if not users:
        users = db.execute('''
            SELECT id, username, full_name, department, semester, avatar_color
            FROM users
            WHERE id != ?
            ORDER BY id ASC
            LIMIT 10
        ''', (current_user_id,)).fetchall()

    peers_list = []
    for u in users:
        peer_id = u['id']
        
        # Get teaching and learning skills for this peer
        skills_rows = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (peer_id,)).fetchall()
        teaches = [s['skill_name'].title() for s in skills_rows if s['skill_type'] == 'teaches']
        learns = [s['skill_name'].title() for s in skills_rows if s['skill_type'] == 'learns']

        # Get last message between current user and this peer
        last_msg = db.execute('''
            SELECT content, message_type, file_name, created_at, sender_id
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY created_at DESC LIMIT 1
        ''', (current_user_id, peer_id, peer_id, current_user_id)).fetchone()

        # Count unread messages from this peer
        unread_count = db.execute('''
            SELECT COUNT(*) as count FROM messages
            WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
        ''', (peer_id, current_user_id)).fetchone()['count']

        # Check connection status
        conn_row = db.execute('''
            SELECT status FROM connections 
            WHERE (requester_id = ? AND receiver_id = ?) OR (requester_id = ? AND receiver_id = ?)
            LIMIT 1
        ''', (current_user_id, peer_id, peer_id, current_user_id)).fetchone()
        
        status_label = 'connected' if (conn_row and conn_row['status'] == 'accepted') else ('pending' if conn_row else 'peer')

        peers_list.append({
            "id": peer_id,
            "username": u['username'],
            "full_name": u['full_name'] or u['username'],
            "department": u['department'] or 'Campus Peer',
            "semester": u['semester'] or 1,
            "avatar_color": u['avatar_color'],
            "teaches": teaches,
            "learns": learns,
            "connection_status": status_label,
            "has_chat": bool(last_msg),
            "last_message": last_msg['content'] if last_msg else "Connected on Loop",
            "last_message_type": last_msg['message_type'] if last_msg else "text",
            "last_message_time": last_msg['created_at'] if last_msg else None,
            "unread_count": unread_count,
            "is_online": True # Campus network online
        })

    # Sort peers: unread first, then by whether they have messages
    peers_list.sort(key=lambda p: (p["unread_count"] == 0, not p["has_chat"]))

    return jsonify({"peers": peers_list}), 200

@chat_bp.route('/api/chat/send', methods=['POST'])
def send_message_http():
    """Send a message via HTTP REST with real-time Socket.IO broadcast."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json or {}
    sender_id = session['user_id']
    receiver_id = data.get('receiver_id')
    content = (data.get('content') or '').strip()
    message_type = data.get('message_type', 'text')
    file_url = data.get('file_url')
    file_name = data.get('file_name')
    file_size = data.get('file_size')

    if not receiver_id:
        return jsonify({"error": "Missing receiver"}), 400
    if not content and not file_url:
        return jsonify({"error": "Cannot send empty message"}), 400

    db = get_db()
    init_chat_db(db)

    # Verify receiver exists
    receiver = db.execute('SELECT id FROM users WHERE id = ?', (receiver_id,)).fetchone()
    if not receiver:
        return jsonify({"error": "Recipient user not found"}), 404

    s_id = int(sender_id)
    r_id = int(receiver_id)

    cursor = db.execute('''
        INSERT INTO messages (sender_id, receiver_id, content, message_type, file_url, file_name, file_size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (s_id, r_id, content, message_type, file_url, file_name, file_size))
    db.commit()
    msg_id = cursor.lastrowid

    now_str = datetime.now().strftime('%I:%M %p')

    msg_payload = {
        'id': msg_id,
        'sender_id': s_id,
        'receiver_id': r_id,
        'content': content,
        'message_type': message_type,
        'file_url': file_url,
        'file_name': file_name,
        'file_size': file_size,
        'created_at': now_str,
        'is_read': 0
    }

    # Real-time broadcast via SocketIO if available
    sio = current_app.extensions.get('socketio')
    if sio:
        try:
            sio.emit('receive_message', msg_payload, room=f"user_{r_id}")
            sio.emit('receive_message', msg_payload, room=f"user_{s_id}")
        except Exception as e:
            current_app.logger.warning(f"Socket.IO emit error: {e}")

    return jsonify({"status": "sent", "message": msg_payload}), 201

@chat_bp.route('/api/chat/messages/<int:peer_id>', methods=['GET'])
def get_messages(peer_id):
    """Fetch message history between current user and peer, supporting incremental delta sync."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    current_user_id = session['user_id']
    db = get_db()
    init_chat_db(db)

    # Mark received unread messages from this peer as read
    db.execute('''
        UPDATE messages 
        SET is_read = 1 
        WHERE sender_id = ? AND receiver_id = ? AND is_read = 0
    ''', (peer_id, current_user_id))
    db.commit()

    after_id = request.args.get('after', type=int)
    if after_id is not None:
        rows = db.execute('''
            SELECT id, sender_id, receiver_id, content, message_type, file_url, file_name, file_size, created_at, is_read
            FROM messages
            WHERE ((sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?))
              AND id > ?
            ORDER BY id ASC
        ''', (current_user_id, peer_id, peer_id, current_user_id, after_id)).fetchall()
    else:
        rows = db.execute('''
            SELECT id, sender_id, receiver_id, content, message_type, file_url, file_name, file_size, created_at, is_read
            FROM messages
            WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)
            ORDER BY id ASC
        ''', (current_user_id, peer_id, peer_id, current_user_id)).fetchall()

    messages = [dict(r) for r in rows]
    return jsonify({"messages": messages}), 200

@chat_bp.route('/api/chat/upload', methods=['POST'])
def upload_file():
    """Upload media or documents for chat."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        original_name = secure_filename(file.filename)
        import time
        unique_name = f"{int(time.time())}_{original_name}"
        save_path = os.path.join(UPLOAD_FOLDER, unique_name)
        file.save(save_path)

        file_size_bytes = os.path.getsize(save_path)
        if file_size_bytes < 1024 * 1024:
            file_size_str = f"{file_size_bytes / 1024:.1f} KB"
        else:
            file_size_str = f"{file_size_bytes / (1024 * 1024):.1f} MB"

        ext = original_name.rsplit('.', 1)[1].lower()
        msg_type = 'image' if ext in {'png', 'jpg', 'jpeg', 'gif'} else 'file'

        return jsonify({
            "file_url": f"/api/chat/files/{unique_name}",
            "file_name": original_name,
            "file_size": file_size_str,
            "message_type": msg_type
        }), 200

    return jsonify({"error": "File type not supported"}), 400

@chat_bp.route('/api/chat/files/<filename>', methods=['GET'])
def get_file(filename):
    """Serve uploaded chat files."""
    return send_from_directory(UPLOAD_FOLDER, filename)
