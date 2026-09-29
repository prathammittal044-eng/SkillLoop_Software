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
    """Send a message via HTTP REST with real-time Socket.IO broadcast.
    Supports both 1:1 messages (receiver_id) and group messages (group_id).
    """
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.json or {}
    sender_id = session['user_id']
    group_id = data.get('group_id')       # present for group messages
    receiver_id = data.get('receiver_id') # present for 1:1 messages
    content = (data.get('content') or '').strip()
    message_type = data.get('message_type', 'text')
    file_url = data.get('file_url')
    file_name = data.get('file_name')
    file_size = data.get('file_size')

    if not group_id and not receiver_id:
        return jsonify({"error": "Missing receiver or group"}), 400
    if not content and not file_url:
        return jsonify({"error": "Cannot send empty message"}), 400

    db = get_db()
    s_id = int(sender_id)
    now_str = datetime.now().strftime('%I:%M %p')

    # ── GROUP MESSAGE PATH ──────────────────────────────────────
    if group_id:
        g_id = int(group_id)
        init_group_db(db)

        # Verify sender is a member
        membership = db.execute(
            'SELECT id FROM group_members WHERE group_id = ? AND user_id = ?',
            (g_id, s_id)
        ).fetchone()
        if not membership:
            return jsonify({"error": "Not a member of this group"}), 403

        cursor = db.execute('''
            INSERT INTO group_messages (group_id, sender_id, content, message_type, file_url, file_name, file_size)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (g_id, s_id, content, message_type, file_url, file_name, file_size))
        db.commit()
        msg_id = cursor.lastrowid

        # Get sender info for display in the group feed
        sender = db.execute(
            'SELECT full_name, username, avatar_color FROM users WHERE id = ?', (s_id,)
        ).fetchone()

        msg_payload = {
            'id': msg_id,
            'group_id': g_id,
            'sender_id': s_id,
            'sender_name': (sender['full_name'] or sender['username']) if sender else 'Unknown',
            'sender_username': sender['username'] if sender else '',
            'sender_avatar_color': sender['avatar_color'] if sender else '#543ce0',
            'content': content,
            'message_type': message_type,
            'file_url': file_url,
            'file_name': file_name,
            'file_size': file_size,
            'created_at': now_str,
        }

        sio = current_app.extensions.get('socketio')
        if sio:
            try:
                sio.emit('receive_group_message', msg_payload, room=f"group_{g_id}")
            except Exception as e:
                current_app.logger.warning(f"Socket.IO group emit error: {e}")

        return jsonify({"status": "sent", "message": msg_payload}), 201

    # ── 1:1 MESSAGE PATH (unchanged) ───────────────────────────
    init_chat_db(db)

    # Verify receiver exists
    receiver = db.execute('SELECT id FROM users WHERE id = ?', (receiver_id,)).fetchone()
    if not receiver:
        return jsonify({"error": "Recipient user not found"}), 404

    r_id = int(receiver_id)

    cursor = db.execute('''
        INSERT INTO messages (sender_id, receiver_id, content, message_type, file_url, file_name, file_size)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (s_id, r_id, content, message_type, file_url, file_name, file_size))
    db.commit()
    msg_id = cursor.lastrowid

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


# ─────────────────────────────────────────────────────────────
# Group Chat Routes
# ─────────────────────────────────────────────────────────────

def init_group_db(db):
    """Ensure group tables exist (mirrors database.py for runtime safety)."""
    db.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            avatar_color TEXT NOT NULL DEFAULT '#543ce0',
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS group_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(group_id, user_id)
        )
    ''')
    db.execute('''
        CREATE TABLE IF NOT EXISTS group_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            content TEXT,
            message_type TEXT DEFAULT 'text',
            file_url TEXT,
            file_name TEXT,
            file_size TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (sender_id) REFERENCES users(id)
        )
    ''')
    db.commit()


import random

AVATAR_COLORS = [
    '#543ce0', '#99366c', '#1a7a4a', '#c45c0d', '#1565c0',
    '#6a1b9a', '#00838f', '#e53935', '#2e7d32', '#f57f17'
]

def _random_color():
    return random.choice(AVATAR_COLORS)


@chat_bp.route('/api/chat/groups', methods=['POST'])
def create_group():
    """Create a new group chat. Caller becomes admin."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.json or {}
    name = (data.get('name') or '').strip()
    description = (data.get('description') or '').strip()
    member_ids = data.get('member_ids', [])  # list of user IDs to add

    if not name:
        return jsonify({"error": "Group name is required"}), 400

    creator_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    avatar_color = _random_color()

    cursor = db.execute(
        'INSERT INTO groups (name, description, avatar_color, created_by) VALUES (?, ?, ?, ?)',
        (name, description, avatar_color, creator_id)
    )
    group_id = cursor.lastrowid

    # Add creator as admin
    db.execute(
        'INSERT INTO group_members (group_id, user_id, role) VALUES (?, ?, ?)',
        (group_id, creator_id, 'admin')
    )

    # Add selected members (ignore duplicates or invalid IDs)
    added_member_ids = [creator_id]
    for uid in member_ids:
        try:
            uid = int(uid)
            if uid == creator_id:
                continue
            user_exists = db.execute('SELECT id FROM users WHERE id = ?', (uid,)).fetchone()
            if user_exists:
                db.execute(
                    'INSERT OR IGNORE INTO group_members (group_id, user_id, role) VALUES (?, ?, ?)',
                    (group_id, uid, 'member')
                )
                added_member_ids.append(uid)
        except (ValueError, TypeError):
            continue

    db.commit()

    group_data = {
        'id': group_id,
        'name': name,
        'description': description,
        'avatar_color': avatar_color,
        'created_by': creator_id,
        'member_count': len(added_member_ids),
        'last_message': None,
        'last_message_time': None,
        'unread_count': 0
    }

    # Notify all members via Socket.IO
    sio = current_app.extensions.get('socketio')
    if sio:
        try:
            for uid in added_member_ids:
                sio.emit('group_created', group_data, room=f"user_{uid}")
        except Exception as e:
            current_app.logger.warning(f"Socket.IO group_created emit error: {e}")

    return jsonify({"status": "created", "group": group_data}), 201


@chat_bp.route('/api/chat/groups', methods=['GET'])
def list_groups():
    """List all groups the current user is a member of."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    rows = db.execute('''
        SELECT g.id, g.name, g.description, g.avatar_color, g.created_by,
               gm.role,
               (SELECT COUNT(*) FROM group_members WHERE group_id = g.id) AS member_count,
               (SELECT content FROM group_messages WHERE group_id = g.id ORDER BY id DESC LIMIT 1) AS last_message,
               (SELECT created_at FROM group_messages WHERE group_id = g.id ORDER BY id DESC LIMIT 1) AS last_message_time,
               (SELECT message_type FROM group_messages WHERE group_id = g.id ORDER BY id DESC LIMIT 1) AS last_message_type
        FROM groups g
        JOIN group_members gm ON gm.group_id = g.id AND gm.user_id = ?
        ORDER BY last_message_time DESC NULLS LAST, g.created_at DESC
    ''', (user_id,)).fetchall()

    groups_list = []
    for r in rows:
        groups_list.append({
            'id': r['id'],
            'name': r['name'],
            'description': r['description'],
            'avatar_color': r['avatar_color'],
            'created_by': r['created_by'],
            'role': r['role'],
            'member_count': r['member_count'],
            'last_message': r['last_message'],
            'last_message_time': r['last_message_time'],
            'last_message_type': r['last_message_type'],
            'unread_count': 0  # Future enhancement: track per-user read pointers
        })

    return jsonify({"groups": groups_list}), 200


@chat_bp.route('/api/chat/groups/<int:group_id>', methods=['GET'])
def get_group_detail(group_id):
    """Get group info + member list."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    # Verify caller is a member
    membership = db.execute(
        'SELECT role FROM group_members WHERE group_id = ? AND user_id = ?',
        (group_id, user_id)
    ).fetchone()
    if not membership:
        return jsonify({"error": "Not a member of this group"}), 403

    group = db.execute('SELECT * FROM groups WHERE id = ?', (group_id,)).fetchone()
    if not group:
        return jsonify({"error": "Group not found"}), 404

    members = db.execute('''
        SELECT u.id, u.username, u.full_name, u.avatar_color, gm.role, gm.joined_at
        FROM group_members gm
        JOIN users u ON u.id = gm.user_id
        WHERE gm.group_id = ?
        ORDER BY gm.role DESC, u.full_name ASC
    ''', (group_id,)).fetchall()

    return jsonify({
        "group": {
            'id': group['id'],
            'name': group['name'],
            'description': group['description'],
            'avatar_color': group['avatar_color'],
            'created_by': group['created_by'],
        },
        "members": [dict(m) for m in members],
        "my_role": membership['role']
    }), 200


@chat_bp.route('/api/chat/groups/<int:group_id>/members', methods=['POST'])
def add_group_members(group_id):
    """Add new members to a group (admin only)."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    caller_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    membership = db.execute(
        'SELECT role FROM group_members WHERE group_id = ? AND user_id = ?',
        (group_id, caller_id)
    ).fetchone()
    if not membership or membership['role'] != 'admin':
        return jsonify({"error": "Only admins can add members"}), 403

    data = request.json or {}
    user_ids = data.get('user_ids', [])

    added = []
    for uid in user_ids:
        try:
            uid = int(uid)
            user_exists = db.execute('SELECT id FROM users WHERE id = ?', (uid,)).fetchone()
            if user_exists:
                db.execute(
                    'INSERT OR IGNORE INTO group_members (group_id, user_id, role) VALUES (?, ?, ?)',
                    (group_id, uid, 'member')
                )
                added.append(uid)
        except (ValueError, TypeError):
            continue

    db.commit()

    group_data = db.execute('SELECT * FROM groups WHERE id = ?', (group_id,)).fetchone()
    # Notify newly added members
    sio = current_app.extensions.get('socketio')
    if sio and group_data:
        payload = {
            'id': group_data['id'],
            'name': group_data['name'],
            'description': group_data['description'],
            'avatar_color': group_data['avatar_color'],
            'created_by': group_data['created_by'],
        }
        for uid in added:
            try:
                sio.emit('group_created', payload, room=f"user_{uid}")
                sio.emit('join_group_room', {'group_id': group_id}, room=f"user_{uid}")
            except Exception as e:
                current_app.logger.warning(f"Socket.IO add member emit error: {e}")

    return jsonify({"status": "added", "added_count": len(added)}), 200


@chat_bp.route('/api/chat/groups/<int:group_id>/members/<int:target_uid>', methods=['DELETE'])
def remove_group_member(group_id, target_uid):
    """Remove a member from a group (admin removes others; any member can leave by removing themselves)."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    caller_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    membership = db.execute(
        'SELECT role FROM group_members WHERE group_id = ? AND user_id = ?',
        (group_id, caller_id)
    ).fetchone()

    if not membership:
        return jsonify({"error": "Not a member of this group"}), 403

    # Allow self-removal (leave) or admin removal
    if caller_id != target_uid and membership['role'] != 'admin':
        return jsonify({"error": "Only admins can remove other members"}), 403

    # Prevent removing the last admin
    if target_uid == caller_id and membership['role'] == 'admin':
        other_admins = db.execute(
            "SELECT COUNT(*) as cnt FROM group_members WHERE group_id = ? AND role = 'admin' AND user_id != ?",
            (group_id, caller_id)
        ).fetchone()['cnt']
        total_members = db.execute(
            "SELECT COUNT(*) as cnt FROM group_members WHERE group_id = ?",
            (group_id,)
        ).fetchone()['cnt']
        if other_admins == 0 and total_members > 1:
            return jsonify({"error": "Transfer admin role before leaving"}), 400

    db.execute(
        'DELETE FROM group_members WHERE group_id = ? AND user_id = ?',
        (group_id, target_uid)
    )
    db.commit()

    # Notify the removed user
    sio = current_app.extensions.get('socketio')
    if sio:
        try:
            sio.emit('removed_from_group', {'group_id': group_id}, room=f"user_{target_uid}")
        except Exception as e:
            current_app.logger.warning(f"Socket.IO remove member emit error: {e}")

    return jsonify({"status": "removed"}), 200


@chat_bp.route('/api/chat/groups/<int:group_id>/messages', methods=['GET'])
def get_group_messages(group_id):
    """Fetch group message history with optional delta sync (?after=<id>)."""
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_id = int(session['user_id'])
    db = get_db()
    init_group_db(db)

    # Verify caller is a member
    membership = db.execute(
        'SELECT id FROM group_members WHERE group_id = ? AND user_id = ?',
        (group_id, user_id)
    ).fetchone()
    if not membership:
        return jsonify({"error": "Not a member of this group"}), 403

    after_id = request.args.get('after', type=int)
    if after_id is not None:
        rows = db.execute('''
            SELECT gm.id, gm.group_id, gm.sender_id, gm.content, gm.message_type,
                   gm.file_url, gm.file_name, gm.file_size, gm.created_at,
                   u.username AS sender_username, u.full_name AS sender_name,
                   u.avatar_color AS sender_avatar_color
            FROM group_messages gm
            JOIN users u ON u.id = gm.sender_id
            WHERE gm.group_id = ? AND gm.id > ?
            ORDER BY gm.id ASC
        ''', (group_id, after_id)).fetchall()
    else:
        rows = db.execute('''
            SELECT gm.id, gm.group_id, gm.sender_id, gm.content, gm.message_type,
                   gm.file_url, gm.file_name, gm.file_size, gm.created_at,
                   u.username AS sender_username, u.full_name AS sender_name,
                   u.avatar_color AS sender_avatar_color
            FROM group_messages gm
            JOIN users u ON u.id = gm.sender_id
            WHERE gm.group_id = ?
            ORDER BY gm.id ASC
        ''', (group_id,)).fetchall()

    messages = [dict(r) for r in rows]
    return jsonify({"messages": messages}), 200

