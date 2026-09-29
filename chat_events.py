from datetime import datetime
from flask import request, session
from flask_socketio import emit, join_room, leave_room
from database import get_db

# Map of user_id -> set of socket session ids
user_sockets = {}
# Map of socket session id -> user_id
socket_users = {}

def register_chat_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        if user_id:
            uid = int(user_id)
            if uid not in user_sockets:
                user_sockets[uid] = set()
            user_sockets[uid].add(request.sid)
            socket_users[request.sid] = uid
            join_room(f"user_{uid}")
            print(f"[SocketIO] User {uid} connected via session, sid={request.sid}", flush=True)
            emit('user_connected', {'user_id': uid, 'status': 'online'}, broadcast=True)

    @socketio.on('authenticate')
    def handle_authenticate(data):
        """Explicitly register user ID room when session cookies aren't passed across ports."""
        uid = (data or {}).get('user_id') or session.get('user_id')
        if uid:
            uid = int(uid)
            if uid not in user_sockets:
                user_sockets[uid] = set()
            user_sockets[uid].add(request.sid)
            socket_users[request.sid] = uid
            join_room(f"user_{uid}")
            print(f"[SocketIO] User {uid} authenticated explicitly, sid={request.sid}", flush=True)

            # Also join all group rooms this user belongs to
            try:
                db = get_db()
                group_rows = db.execute(
                    'SELECT group_id FROM group_members WHERE user_id = ?', (uid,)
                ).fetchall()
                for row in group_rows:
                    gid = row['group_id']
                    join_room(f"group_{gid}")
                    print(f"[SocketIO] User {uid} joined group room group_{gid}", flush=True)
            except Exception as e:
                print(f"[SocketIO] Could not join group rooms for user {uid}: {e}", flush=True)

            emit('authenticated', {'user_id': uid, 'status': 'ok'})

    @socketio.on('join_group_rooms')
    def handle_join_group_rooms(data):
        """Called when user is added to a new group mid-session so they join the Socket.IO room."""
        uid = socket_users.get(request.sid) or session.get('user_id')
        group_id = (data or {}).get('group_id')
        if uid and group_id:
            uid = int(uid)
            g_id = int(group_id)
            try:
                db = get_db()
                membership = db.execute(
                    'SELECT id FROM group_members WHERE group_id = ? AND user_id = ?',
                    (g_id, uid)
                ).fetchone()
                if membership:
                    join_room(f"group_{g_id}")
                    print(f"[SocketIO] User {uid} joined new group room group_{g_id}", flush=True)
            except Exception as e:
                print(f"[SocketIO] join_group_rooms error: {e}", flush=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        uid = socket_users.pop(request.sid, None) or session.get('user_id')
        if uid:
            uid = int(uid)
            sids = user_sockets.get(uid)
            if sids and request.sid in sids:
                sids.discard(request.sid)
            if not sids:
                user_sockets.pop(uid, None)
                print(f"[SocketIO] User {uid} fully disconnected", flush=True)
                emit('user_disconnected', {'user_id': uid, 'status': 'offline'}, broadcast=True)
            else:
                print(f"[SocketIO] User {uid} closed 1 socket, {len(sids)} active", flush=True)

    @socketio.on('send_message')
    def handle_send_message(data):
        """Save message to SQLite and deliver in real-time. Supports both 1:1 and group messages."""
        data = data or {}
        sender_id = session.get('user_id') or socket_users.get(request.sid) or data.get('sender_id')
        if not sender_id:
            return {'error': 'Unauthorized'}

        group_id = data.get('group_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content', '')
        message_type = data.get('message_type', 'text')
        file_url = data.get('file_url')
        file_name = data.get('file_name')
        file_size = data.get('file_size')

        if not group_id and not receiver_id:
            return {'error': 'Missing receiver or group'}

        s_id = int(sender_id)
        db = get_db()
        now_str = datetime.now().strftime('%I:%M %p')

        # ── GROUP MESSAGE PATH ──────────────────────────────────
        if group_id:
            g_id = int(group_id)
            cursor = db.execute('''
                INSERT INTO group_messages (group_id, sender_id, content, message_type, file_url, file_name, file_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (g_id, s_id, content, message_type, file_url, file_name, file_size))
            db.commit()
            msg_id = cursor.lastrowid

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

            emit('receive_group_message', msg_payload, room=f"group_{g_id}")
            return {'status': 'sent', 'message': msg_payload}

        # ── 1:1 MESSAGE PATH (unchanged) ───────────────────────
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

        # Emit to both sender and receiver rooms
        emit('receive_message', msg_payload, room=f"user_{r_id}")
        emit('receive_message', msg_payload, room=f"user_{s_id}")
        return {'status': 'sent', 'message': msg_payload}

    # ─────────────────────────────────────────────────────────────
    # WebRTC Signaling Handlers (Peer-to-Peer Audio/Video)
    # ─────────────────────────────────────────────────────────────
    @socketio.on('call_user')
    def handle_call_user(data):
        """Forward SDP Offer to target peer."""
        caller_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        offer = (data or {}).get('offer')
        caller_name = session.get('full_name') or session.get('username') or 'Campus Peer'
        
        if target_id and caller_id:
            c_id = int(caller_id)
            t_id = int(target_id)
            print(f"[WebRTC] call_user: {c_id} ({caller_name}) -> {t_id}", flush=True)
            emit('incoming_call', {
                'caller_id': c_id,
                'caller_name': caller_name,
                'offer': offer
            }, room=f"user_{t_id}")

    @socketio.on('answer_call')
    def handle_answer_call(data):
        """Forward SDP Answer back to the caller."""
        user_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        answer = (data or {}).get('answer')
        if target_id and user_id:
            u_id = int(user_id)
            t_id = int(target_id)
            print(f"[WebRTC] answer_call: {u_id} -> {t_id}", flush=True)
            emit('call_answered', {
                'answer': answer,
                'from_user_id': u_id
            }, room=f"user_{t_id}")

    @socketio.on('ice_candidate')
    def handle_ice_candidate(data):
        """Relay ICE candidates between peers for WebRTC connectivity."""
        user_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        candidate = (data or {}).get('candidate')
        if target_id and user_id and candidate:
            u_id = int(user_id)
            t_id = int(target_id)
            cand_str = ''
            if isinstance(candidate, dict):
                cand_str = str(candidate.get('candidate') or '')
            typ = 'unknown'
            if ' typ relay ' in f' {cand_str} ':
                typ = 'relay'
            elif ' typ srflx ' in f' {cand_str} ':
                typ = 'srflx'
            elif ' typ host ' in f' {cand_str} ':
                typ = 'host'
            print(f"[WebRTC] ice_candidate: {u_id} -> {t_id} ({typ})", flush=True)
            emit('ice_candidate', {
                'candidate': candidate,
                'from_user_id': u_id
            }, room=f"user_{t_id}")

    @socketio.on('renegotiate')
    def handle_renegotiate(data):
        """Forward ICE-restart offer so a failed pair can try TURN relay."""
        user_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        offer = (data or {}).get('offer')
        if target_id and user_id and offer:
            u_id = int(user_id)
            t_id = int(target_id)
            print(f"[WebRTC] renegotiate: {u_id} -> {t_id}", flush=True)
            emit('renegotiate', {
                'offer': offer,
                'from_user_id': u_id
            }, room=f"user_{t_id}")

    @socketio.on('renegotiate_answer')
    def handle_renegotiate_answer(data):
        user_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        answer = (data or {}).get('answer')
        if target_id and user_id and answer:
            u_id = int(user_id)
            t_id = int(target_id)
            print(f"[WebRTC] renegotiate_answer: {u_id} -> {t_id}", flush=True)
            emit('renegotiate_answer', {
                'answer': answer,
                'from_user_id': u_id
            }, room=f"user_{t_id}")

    @socketio.on('end_call')
    def handle_end_call(data):
        """Notify peer that call has been terminated."""
        user_id = session.get('user_id') or socket_users.get(request.sid)
        target_id = (data or {}).get('target_user_id')
        if target_id and user_id:
            u_id = int(user_id)
            t_id = int(target_id)
            print(f"[WebRTC] end_call: {u_id} -> {t_id}", flush=True)
            emit('call_ended', {
                'from_user_id': u_id
            }, room=f"user_{t_id}")
