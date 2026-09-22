from flask import request, session
from flask_socketio import emit, join_room, leave_room
from database import get_db

# Map of user_id -> socket session id for direct signaling
user_sockets = {}

def register_chat_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        if user_id:
            uid = int(user_id)
            user_sockets[uid] = request.sid
            # Join personal user room so anyone can emit to room=f"user_{uid}"
            join_room(f"user_{uid}")
            print(f"[SocketIO] User {uid} connected, sid={request.sid}", flush=True)
            emit('user_connected', {'user_id': uid, 'status': 'online'}, broadcast=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = session.get('user_id')
        if user_id:
            uid = int(user_id)
            if uid in user_sockets and user_sockets[uid] == request.sid:
                del user_sockets[uid]
            print(f"[SocketIO] User {uid} disconnected", flush=True)
            emit('user_disconnected', {'user_id': uid, 'status': 'offline'}, broadcast=True)

    @socketio.on('send_message')
    def handle_send_message(data):
        """Save message to SQLite and deliver in real-time to receiver."""
        sender_id = session.get('user_id')
        if not sender_id:
            return {'error': 'Unauthorized'}
            
        receiver_id = data.get('receiver_id')
        content = data.get('content', '')
        message_type = data.get('message_type', 'text')
        file_url = data.get('file_url')
        file_name = data.get('file_name')
        file_size = data.get('file_size')

        if not receiver_id:
            return {'error': 'Missing receiver'}

        s_id = int(sender_id)
        r_id = int(receiver_id)

        db = get_db()
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
            'created_at': 'Just now',
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
        caller_id = session.get('user_id')
        target_id = data.get('target_user_id')
        offer = data.get('offer')
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
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        answer = data.get('answer')
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
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        candidate = data.get('candidate')
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
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        offer = data.get('offer')
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
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        answer = data.get('answer')
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
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        if target_id and user_id:
            u_id = int(user_id)
            t_id = int(target_id)
            print(f"[WebRTC] end_call: {u_id} -> {t_id}", flush=True)
            emit('call_ended', {
                'from_user_id': u_id
            }, room=f"user_{t_id}")
