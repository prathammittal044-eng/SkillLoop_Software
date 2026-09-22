import base64
import hashlib
import hmac
import os
import time
from flask import Blueprint, jsonify

turn_bp = Blueprint('turn', __name__)

GOOGLE_STUN = [
    {'urls': 'stun:stun.l.google.com:19302'},
    {'urls': 'stun:stun1.l.google.com:19302'},
    {'urls': 'stun:stun2.l.google.com:19302'},
    {'urls': 'stun:stun.cloudflare.com:3478'},
]


def _hmac_turn_credential(secret, ttl_seconds=86400, user='skillloop'):
    """coturn long-term / REST auth: username = expiry:user, password = base64(hmac-sha1)."""
    expiry = int(time.time()) + ttl_seconds
    username = f'{expiry}:{user}'
    digest = hmac.new(secret.encode('utf-8'), username.encode('utf-8'), hashlib.sha1).digest()
    credential = base64.b64encode(digest).decode('ascii')
    return username, credential


def _openrelay_static_auth_servers():
    """
    Metered Open Relay static-auth (same secret documented for Nextcloud Talk).
    Gives a TURN relay when no Metered/Cloudflare API key is configured — required
    for Indian CGNAT / same-WiFi hairpin failures where STUN-only ICE never connects.
    """
    secret = os.environ.get('OPENRELAY_STATIC_SECRET', 'openrelayprojectsecret').strip()
    username, credential = _hmac_turn_credential(secret)
    urls = [
        'turn:staticauth.openrelay.metered.ca:80',
        'turn:staticauth.openrelay.metered.ca:443',
        'turn:staticauth.openrelay.metered.ca:443?transport=tcp',
        'turns:staticauth.openrelay.metered.ca:443?transport=tcp',
        'turn:openrelay.metered.ca:80',
        'turn:openrelay.metered.ca:443',
        'turn:openrelay.metered.ca:443?transport=tcp',
    ]
    return [{
        'urls': urls,
        'username': username,
        'credential': credential,
    }]


def _fetch_metered_servers():
    metered_app = os.environ.get('METERED_APP_NAME', '').strip()
    metered_api_key = os.environ.get('METERED_API_KEY', '').strip()
    if not (metered_app and metered_api_key):
        return None

    try:
        import urllib.request
        import json as _json

        # Step 1: POST to get a short-lived API key from secret key
        post_url = f'https://{metered_app}.metered.live/api/v1/turn/credential?secretKey={metered_api_key}'
        post_body = _json.dumps({'expiryInSeconds': 86400}).encode('utf-8')
        post_req = urllib.request.Request(
            post_url,
            data=post_body,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(post_req, timeout=5) as resp:
            if resp.status == 200:
                cred_data = _json.loads(resp.read().decode('utf-8'))
                temp_api_key = cred_data.get('apiKey')
                if temp_api_key:
                    # Step 2: GET ice servers using the temp API key
                    get_url = f'https://{metered_app}.metered.live/api/v1/turn/credentials?apiKey={temp_api_key}'
                    with urllib.request.urlopen(get_url, timeout=5) as get_resp:
                        if get_resp.status == 200:
                            servers = _json.loads(get_resp.read().decode('utf-8'))
                            if isinstance(servers, list) and servers:
                                print(f'[TURN] Metered returned {len(servers)} ICE servers', flush=True)
                                return servers

        # Fallback: try direct API key
        get_url = f'https://{metered_app}.metered.live/api/v1/turn/credentials?apiKey={metered_api_key}'
        with urllib.request.urlopen(get_url, timeout=5) as get_resp:
            if get_resp.status == 200:
                servers = _json.loads(get_resp.read().decode('utf-8'))
                if isinstance(servers, list) and servers:
                    print(f'[TURN] Metered API key returned {len(servers)} ICE servers', flush=True)
                    return servers
    except Exception as e:
        print(f'[TURN] Metered fetch failed: {e}', flush=True)
    return None


def _fetch_cloudflare_turn():
    """Cloudflare Calls TURN requires ephemeral ICE credentials, not the raw API token."""
    turn_key_id = os.environ.get('CLOUDFLARE_TURN_KEY_ID', '').strip()
    turn_api_token = os.environ.get('CLOUDFLARE_TURN_API_TOKEN', '').strip()
    if not (turn_key_id and turn_api_token):
        return None

    try:
        import urllib.request
        import json as _json

        url = f'https://rtc.live.cloudflare.com/v1/turn/keys/{turn_key_id}/credentials/generate-ice-servers'
        body = _json.dumps({'ttl': 86400}).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                'Authorization': f'Bearer {turn_api_token}',
                'Content-Type': 'application/json',
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            if resp.status == 200:
                data = _json.loads(resp.read().decode('utf-8'))
                servers = data.get('iceServers') or data.get('ice_servers')
                if isinstance(servers, list) and servers:
                    print(f'[TURN] Cloudflare returned {len(servers)} ICE servers', flush=True)
                    return servers
            print(f'[TURN] Cloudflare credential API HTTP {resp.status}', flush=True)
    except Exception as e:
        print(f'[TURN] Cloudflare fetch failed: {e}', flush=True)
    return None



def build_ice_servers():
    servers = list(GOOGLE_STUN)

    metered = _fetch_metered_servers()
    if metered:
        servers.extend(metered)
        return servers

    cloudflare = _fetch_cloudflare_turn()
    if cloudflare:
        servers.extend(cloudflare)
        return servers

    servers.extend(_openrelay_static_auth_servers())
    print('[TURN] Using OpenRelay static-auth HMAC fallback (set METERED_API_KEY for a dedicated free TURN app)', flush=True)
    return servers


@turn_bp.route('/api/turn-credentials', methods=['GET'])
def get_turn_credentials():
    ice_servers = build_ice_servers()
    has_turn = any(
        'turn:' in str(s.get('urls', '')).lower() or 'turns:' in str(s.get('urls', '')).lower()
        for s in ice_servers
    )
    return jsonify({
        'iceServers': ice_servers,
        'hasTurn': has_turn,
    })
