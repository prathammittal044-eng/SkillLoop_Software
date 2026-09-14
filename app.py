import os
import random
import sqlite3
import html as html_module
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

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for the Nuxt frontend and local network peers (wildcard for LAN testing)
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://192.168.1.7:3000"])

# Register modular Chat blueprint
app.register_blueprint(chat_bp)

# Initialize SocketIO for real-time messaging & WebRTC signaling
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=False)
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
        session['user_id'] = user_id
        session['username'] = username
        session['full_name'] = full_name
        
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
    
    if not username or not password:
        return jsonify({"error": "Please enter username and password"}), 400
        
    db = get_db()
    clean_username = username.lstrip('@').strip()
    user = db.execute('SELECT * FROM users WHERE LOWER(username) = LOWER(?) OR LOWER(email) = LOWER(?)', 
                      (clean_username, clean_username)).fetchone()
    
    if user is None or not check_password_hash(user['password_hash'], password):
        return jsonify({"error": "Invalid username or password"}), 401
        
    session['user_id'] = user['id']
    session['username'] = user['username']
    session['full_name'] = user['full_name']
    
    return jsonify({"message": "Logged in successfully", "user": {"id": user['id'], "username": user['username'], "full_name": user['full_name']}}), 200

@app.route('/api/user/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    db = get_db()
    user = db.execute('SELECT id, username, email, full_name, department, semester, bio, education, qualifications, experience, github, linkedin, xp, level, streak_count, time_credits, avatar_color, created_at FROM users WHERE id = ?', (session['user_id'],)).fetchone()
    
    if user is None:
        session.clear()
        return jsonify({"error": "User not found"}), 404
        
    return jsonify({"user": dict(user)}), 200

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

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
        socketio.emit('connection_accepted', {
            'connection_id': conn_id,
            'accepted_by_id': session['user_id'],
            'accepted_by_name': accepter['full_name'] or accepter['username'],
            'accepted_by_username': accepter['username'],
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
            linkedin = ?
        WHERE id = ?
    ''', (
        data.get('full_name'), data.get('department'), data.get('semester'),
        data.get('bio'), data.get('education'), data.get('qualifications'),
        data.get('experience'), data.get('github'), data.get('linkedin'),
        session['user_id']
    ))
    db.commit()
    return jsonify({"message": "Profile updated"}), 200

@app.route('/api/user/<username>', methods=['GET'])
def get_public_profile(username):
    db = get_db()
    user = db.execute('SELECT id, username, full_name, department, semester, xp, level, avatar_color FROM users WHERE username = ?', (username,)).fetchone()
    if not user: return jsonify({"error": "User not found"}), 404
    
    skills = db.execute('SELECT skill_name, skill_type FROM user_skills WHERE user_id = ?', (user['id'],)).fetchall()
    teaches = [s['skill_name'] for s in skills if s['skill_type'] == 'teaches']
    learns = [s['skill_name'] for s in skills if s['skill_type'] == 'learns']
    
    profile = dict(user)
    profile['teaches'] = teaches
    profile['learns'] = learns
    return jsonify({"profile": profile}), 200

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# SKILL VERIFICATION QUIZ ENGINE v3.0  â€” AI-Powered (Gemini)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

import json as _json
from dotenv import load_dotenv
load_dotenv()  # loads GEMINI_API_KEY from .env

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

def generate_ai_questions(skill_name: str, difficulty: str) -> list | None:
    """
    Ask Google Gemini to generate QUIZ_QUESTION_COUNT multiple-choice questions
    about `skill_name` at `difficulty` level.
    Returns a list of dicts: [{'q': ..., 'options': [...], 'answer': int}, ...]
    or None if the call fails.
    """
    if not GEMINI_AVAILABLE:
        return None

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

    try:
        response = _genai_client.models.generate_content(
            model='models/gemini-3.1-flash-lite',
            contents=prompt,
            config=_genai_types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=2048,
            )
        )
        raw = response.text.strip()

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

        return validated if len(validated) >= 3 else None

    except Exception as e:
        app.logger.error(f'Gemini question generation failed for "{skill_name}" ({difficulty}): {e}')
        return None


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

    # Generate fresh questions from Gemini
    questions = generate_ai_questions(skill_name, difficulty)

    if not questions:
        return jsonify({"error": f"Could not generate questions for '{skill_name}'. Please try again."}), 503

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
    
    # Update verification if passed
    if passed:
        level_order = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        existing = db.execute('SELECT verified_level FROM skill_verifications WHERE user_id = ? AND skill_name = ?', (session['user_id'], skill_name)).fetchone()
        if existing:
            if level_order.get(difficulty, 0) > level_order.get(existing['verified_level'], 0):
                db.execute('UPDATE skill_verifications SET verified_level = ?, verified_at = CURRENT_TIMESTAMP WHERE user_id = ? AND skill_name = ?', (difficulty, session['user_id'], skill_name))
        else:
            db.execute('INSERT INTO skill_verifications (user_id, skill_name, verified_level) VALUES (?, ?, ?)', (session['user_id'], skill_name, difficulty))
    
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


@app.route('/api/quiz/verified', methods=['GET'])
def verified_skills():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    db = get_db()
    verifications = db.execute('SELECT skill_name, verified_level, verified_at FROM skill_verifications WHERE user_id = ?', (session['user_id'],)).fetchall()
    return jsonify({"verified": [dict(v) for v in verifications]}), 200


# =============================================================================
# RESUME & LINKEDIN-STYLE PROFILE SYSTEM
# =============================================================================

@app.route('/api/resume', methods=['GET'])
def get_resume():
    if 'user_id' not in session:
        return jsonify({"error": "Not authenticated"}), 401
    
    user_id = session['user_id']
    db = get_db()
    
    user = db.execute('SELECT id, username, email, full_name, department, semester, bio, education, experience, github, linkedin, time_credits, skills_taught, rating_avg, xp, level FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Get teaching skills
    teaches = [r['skill_name'] for r in db.execute('SELECT skill_name FROM user_skills WHERE user_id = ? AND skill_type = "teaches"', (user_id,)).fetchall()]
    
    # Get verified skills with level
    verifications = [dict(v) for v in db.execute('SELECT skill_name, verified_level, verified_at FROM skill_verifications WHERE user_id = ?', (user_id,)).fetchall()]
    
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
        if user['education']:
            default_education.append({
                "id": 1,
                "institution": "University Institute of Technology",
                "degree": f"Bachelor of Technology in {user['department'] or 'Engineering'}",
                "field_of_study": user['department'] or "Computer Science",
                "start_year": "2022",
                "end_year": "2026",
                "grade": "8.8 CGPA",
                "description": user['education']
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
        response = _genai_client.models.generate_content(
            model='models/gemini-3.1-flash-lite',
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


@app.route('/api/institutions/search', methods=['GET'])
def search_institutions_api():
    query = request.args.get('q', '').strip()
    limit = request.args.get('limit', 15, type=int)
    results = search_institutions(query, limit=limit)
    return jsonify({"results": results, "query": query}), 200


if __name__ == '__main__':
    # Listen on 0.0.0.0 so both localhost and teammate devices on LAN can connect.
    # use_reloader=False prevents Windows eventlet port collision crashes (WinError 10048)
    socketio.run(app, host='0.0.0.0', debug=True, use_reloader=False, port=5000)

