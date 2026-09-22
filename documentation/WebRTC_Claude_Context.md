# SkillLoop WebRTC Video Calling - Debugging Context for Claude

## System Architecture
* **Frontend:** Vue 3 (Nuxt 3) with `<script setup>`. Runs on port 3000.
* **Backend:** Flask with Flask-SocketIO (Eventlet). Runs on port 5000.
* **Tunneling / Hosting:** Application is temporarily hosted using Ngrok (`npx ngrok http 3000`), which tunnels HTTP/HTTPS and WebSockets. Nuxt proxies `/api/**` and `/socket.io/**` to the Flask backend.
* **TURN Server:** We are using Metered.ca. The backend successfully authenticates using a Secret Key (`POST /credential`), fetches the ephemeral TURN credentials, and passes them to the frontend.

## The Problem
We are testing video calling across two different computers using the Ngrok URL. 
* **Signaling works perfectly**: Users can see each other online, text chat works, and clicking 'Call' makes the other person's screen ring.
* **Media works perfectly**: Both users successfully acquire local camera/mic streams (the browser grants permissions).
* **The Error**: The WebRTC `iceConnectionState` never connects. One user gets `ICE: NEW | Conn: NEW`, and the other gets `ICE: DISCONNECTED | Conn: FAILED`. The video stream is never transmitted.

We recently fixed a race condition where `pendingICECandidates` was being cleared incorrectly when `createPeerConnection()` was called on the receiver's end. However, the connection is still failing.

## Please Focus On:
1. Is there a flaw in how Vue 3 reactivity interacts with `RTCPeerConnection` or `MediaStream`? (Note: `peerConnection`, `localStream`, `remoteStream` are intentionally declared as plain `let` variables, not `ref`, to avoid Vue Proxy interference, but maybe there is another lifecycle issue).
2. Is the ICE Candidate exchange timing or format still incorrect?
3. Is `setLocalDescription` or `setRemoteDescription` out of order?
4. Are we missing a crucial WebRTC constraint or setting for Ngrok / cross-network connections?

---

## 1. Frontend: WebRTC Logic (`frontend/pages/chat.vue`)
*Note: This is the exact current WebRTC implementation.*

```javascript
// WebRTC Global State (Non-reactive to avoid Vue Proxy breaking C++ WebRTC bindings)
let peerConnection = null
let localStream = null
let remoteStream = null
let currentCallPeerId = null
let pendingICECandidates = []  // Queue ICE candidates before remote desc is set

let rtcConfig = {
  iceServers: [
    { urls: 'stun:stun.l.google.com:19302' },
    { urls: 'stun:stun.cloudflare.com:3478' }
  ],
  iceCandidatePoolSize: 10
}

// Fetch TURN credentials from backend on mount (CALLED IN onMounted)
const fetchTurnCredentials = async () => {
  try {
    const res = await fetch('/api/turn-credentials', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      rtcConfig = { ...rtcConfig, iceServers: data.iceServers }
      console.log('[WebRTC] TURN credentials loaded:', rtcConfig.iceServers.length, 'servers')
    }
  } catch (e) {
    console.warn('[WebRTC] Could not fetch TURN credentials, falling back to STUN-only:', e)
  }
}

// Socket.IO Listeners (Set up in onMounted after fetchTurnCredentials)
const setupSocket = () => {
  socket.value = io('/', { path: '/socket.io' })

  socket.value.on('incoming_call', async (data) => {
    pendingICECandidates = []
    incomingCall.value = data
  })

  socket.value.on('call_answered', async (data) => {
    if (peerConnection) {
      await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer))
      console.log('[WebRTC] Remote description set (answer)')
      
      // Drain any ICE candidates queued before we had remote desc
      for (const candidate of pendingICECandidates) {
        try {
          await peerConnection.addIceCandidate(new RTCIceCandidate(candidate))
          console.log('[WebRTC] Drained queued ICE candidate (caller side)')
        } catch (e) {
          console.warn('[WebRTC] Error draining ICE candidate', e)
        }
      }
      pendingICECandidates = []
    }
  })

  socket.value.on('ice_candidate', async (data) => {
    if (!data.candidate) return
    
    // If peer connection isn't ready or remote description not yet set, queue the candidate
    if (!peerConnection || !peerConnection.remoteDescription || !peerConnection.remoteDescription.type) {
      console.log('[WebRTC] Queuing ICE candidate (connection not ready)')
      pendingICECandidates.push(data.candidate)
      return
    }
    try {
      await peerConnection.addIceCandidate(new RTCIceCandidate(data.candidate))
      console.log('[WebRTC] Added ICE candidate')
    } catch (e) {
      console.error('[WebRTC] Error adding ICE candidate', e)
    }
  })
}

// ─── WebRTC Video Calling Implementation ─────────────────────────────────────

const startCall = async (peerId) => {
  if (isCallActive.value) return
  pendingICECandidates = []

  currentCallPeerId = peerId
  const peer = peers.value.find(p => p.id === peerId)
  activePeer.value = peer || { id: peerId, full_name: 'Peer' }

  try {
    localStream = await requestUserMediaSafe()
    isCallActive.value = true
    await nextTick()
    
    attachStream(localVideoRef, localStream)
    createPeerConnection()

    localStream.getTracks().forEach(track => {
      peerConnection.addTrack(track, localStream)
    })

    const offer = await peerConnection.createOffer()
    await peerConnection.setLocalDescription(offer)
    
    socket.value.emit('call_user', {
      target_user_id: peerId,
      offer: offer
    })
  } catch (e) {
    console.error(e)
    endCall()
  }
}

const acceptCall = async () => {
  const callData = incomingCall.value
  incomingCall.value = null
  if (!callData) return
  
  currentCallPeerId = callData.caller_id
  const callerPeer = peers.value.find(p => p.id === callData.caller_id)
  activePeer.value = callerPeer || { id: callData.caller_id, full_name: callData.caller_name || 'Caller' }

  try {
    localStream = await requestUserMediaSafe()
    isCallActive.value = true
    await nextTick()

    attachStream(localVideoRef, localStream)
    createPeerConnection()

    localStream.getTracks().forEach(track => {
      peerConnection.addTrack(track, localStream)
    })

    await peerConnection.setRemoteDescription(new RTCSessionDescription(callData.offer))

    const answer = await peerConnection.createAnswer()
    await peerConnection.setLocalDescription(answer)

    socket.value.emit('answer_call', {
      target_user_id: currentCallPeerId,
      answer: answer
    })

    // Drain any ICE candidates that arrived before remote description
    for (const candidate of pendingICECandidates) {
      try {
        await peerConnection.addIceCandidate(new RTCIceCandidate(candidate))
      } catch (e) {
        console.warn('[WebRTC] Error draining ICE candidate', e)
      }
    }
    pendingICECandidates = []

  } catch (e) {
    console.error('[WebRTC] Error accepting call:', e)
    endCall()
  }
}

const createPeerConnection = () => {
  if (remoteStream) {
    remoteStream.getTracks().forEach(t => t.stop())
  }
  remoteStream = new MediaStream()

  peerConnection = new RTCPeerConnection(rtcConfig)

  peerConnection.onicecandidate = (event) => {
    const targetId = currentCallPeerId || activePeer.value?.id
    if (event.candidate && targetId) {
      socket.value.emit('ice_candidate', {
        target_user_id: targetId,
        candidate: event.candidate
      })
    }
  }

  peerConnection.oniceconnectionstatechange = () => {
    const state = peerConnection?.iceConnectionState || 'unknown'
    iceConnectionStatus.value = `ICE: ${state}`
    updateCallDebug()
  }

  peerConnection.ontrack = (event) => {
    console.log('[WebRTC] Track received:', event.track.kind)
    event.streams[0].getTracks().forEach(track => {
      remoteStream.addTrack(track)
    })
    attachStream(remoteVideoRef, remoteStream)
  }
}
```

---

## 2. Backend: Signaling Events (`chat_events.py`)

```python
    @socketio.on('call_user')
    def handle_call_user(data):
        target_id = data.get('target_user_id')
        offer = data.get('offer')
        caller_id = session.get('user_id')
        caller_name = session.get('full_name') or session.get('username') or 'Campus Peer'
        
        if target_id and caller_id:
            c_id = int(caller_id)
            t_id = int(target_id)
            emit('incoming_call', {
                'caller_id': c_id,
                'caller_name': caller_name,
                'offer': offer
            }, room=f"user_{t_id}")

    @socketio.on('answer_call')
    def handle_answer_call(data):
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        answer = data.get('answer')
        if target_id and user_id:
            u_id = int(user_id)
            t_id = int(target_id)
            emit('call_answered', {
                'answer': answer,
                'from_user_id': u_id
            }, room=f"user_{t_id}")

    @socketio.on('ice_candidate')
    def handle_ice_candidate(data):
        user_id = session.get('user_id')
        target_id = data.get('target_user_id')
        candidate = data.get('candidate')
        if target_id and user_id:
            emit('ice_candidate', {
                'candidate': candidate,
                'from_user_id': user_id
            }, room=f"user_{target_id}")
```
