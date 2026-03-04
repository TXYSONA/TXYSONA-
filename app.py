"""
TXYSONA Flask Backend
=====================
Yahan sirf apna JSONBin Master Key aur Admin password daalo — baaki sab safe hai!
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'txysona-secret-change-this-2024'  # Koi bhi random string dal sakte ho

# ══════════════════════════════════════════════════════
#  SIRF YAHAN APNI DETAILS DAALO — BAAKI MAT CHHEDNA
# ══════════════════════════════════════════════════════
JSONBIN_MASTER_KEY = '$2a$10$zSszXFglhPYIWzsydqmzeODAtEFiSzjC5EWdhZozK.MBw8Pjt0Ave'   # <-- Apni JSONBin Master Key
ADMIN_USERNAME     = 'admin'              # <-- Adminsatyamtx
ADMIN_PASSWORD     = 'admin@txysona123'  # <-- Admintx@satyam2025!)
# ══════════════════════════════════════════════════════

JSONBIN_URL = 'https://api.jsonbin.io/v3'
BIN_ID_FILE = 'bin_id.txt'   # Bin ID yahan save hota hai

# ─── JSONBin Helpers ───────────────────────────────────

def jb_headers():
    return {
        'Content-Type': 'application/json',
        'X-Master-Key': JSONBIN_MASTER_KEY
    }

def get_bin_id():
    """Saved bin ID load karo ya dhundho ya banao"""
    # Pehle local file check karo
    try:
        with open(BIN_ID_FILE, 'r') as f:
            bid = f.read().strip()
            if bid:
                return bid
    except FileNotFoundError:
        pass

    # JSONBin par dhundho
    try:
        r = requests.get(f'{JSONBIN_URL}/b', headers=jb_headers(), timeout=10)
        bins = r.json()
        if isinstance(bins, list):
            for b in bins:
                meta = b.get('snippetMeta') or {}
                if meta.get('name') == 'txysona_data':
                    bid = b.get('id') or meta.get('id') or b.get('_id')
                    if bid:
                        save_bin_id(bid)
                        return bid
    except Exception:
        pass

    # Naya bin banao
    try:
        data = {'visitors': [], 'queries': [], 'app_status': 'on'}
        r = requests.post(
            f'{JSONBIN_URL}/b',
            headers={**jb_headers(), 'X-Bin-Name': 'txysona_data', 'X-Bin-Private': 'true'},
            json=data, timeout=10
        )
        result = r.json()
        bid = result.get('metadata', {}).get('id')
        if bid:
            save_bin_id(bid)
            return bid
    except Exception:
        pass

    return None

def save_bin_id(bid):
    try:
        with open(BIN_ID_FILE, 'w') as f:
            f.write(bid)
    except Exception:
        pass

def read_data():
    """JSONBin se data padhna"""
    bid = get_bin_id()
    if not bid:
        return {'visitors': [], 'queries': [], 'app_status': 'on'}
    try:
        r = requests.get(f'{JSONBIN_URL}/b/{bid}/latest', headers=jb_headers(), timeout=10)
        return r.json().get('record', {'visitors': [], 'queries': [], 'app_status': 'on'})
    except Exception:
        return {'visitors': [], 'queries': [], 'app_status': 'on'}

def write_data(data):
    """JSONBin mein data likhna"""
    bid = get_bin_id()
    if not bid:
        return False
    try:
        r = requests.put(f'{JSONBIN_URL}/b/{bid}', headers=jb_headers(), json=data, timeout=10)
        return r.ok
    except Exception:
        return False

# ─── Admin Auth Decorator ──────────────────────────────

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

# ─── Main App Routes ───────────────────────────────────

@app.route('/')
def index():
    """TXYSONA app serve karo"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """App on/off status check"""
    try:
        data = read_data()
        return jsonify({'status': data.get('app_status', 'on')})
    except Exception:
        return jsonify({'status': 'on'})

@app.route('/api/log-visit', methods=['POST'])
def api_log_visit():
    """Visitor log karo"""
    try:
        body    = request.get_json() or {}
        browser = body.get('browser', 'Unknown')
        device  = body.get('device', '')[:80]
        data    = read_data()

        if not isinstance(data.get('visitors'), list):
            data['visitors'] = []

        data['visitors'].append({
            'time':    datetime.utcnow().isoformat(),
            'browser': browser,
            'device':  device,
            'ip':      request.remote_addr
        })
        # Sirf last 500 rakhna
        data['visitors'] = data['visitors'][-500:]
        write_data(data)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False})

@app.route('/api/log-query', methods=['POST'])
def api_log_query():
    """User query log karo"""
    try:
        body    = request.get_json() or {}
        query   = body.get('query', '')[:200]
        browser = body.get('browser', 'Unknown')
        data    = read_data()

        if not isinstance(data.get('queries'), list):
            data['queries'] = []

        data['queries'].append({
            'time':    datetime.utcnow().isoformat(),
            'query':   query,
            'browser': browser,
            'ip':      request.remote_addr
        })
        data['queries'] = data['queries'][-500:]
        write_data(data)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False})

# ─── Admin Routes ──────────────────────────────────────

@app.route('/admin', methods=['GET'])
@admin_required
def admin():
    """Admin panel"""
    return render_template('admin.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    error = ''
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '')
        if u == ADMIN_USERNAME and p == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = '❌ Galat username ya password'
    return render_template('admin_login.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('admin_login'))

@app.route('/admin/api/data')
@admin_required
def admin_api_data():
    """Admin ko poora data do"""
    data = read_data()
    return jsonify(data)

@app.route('/admin/api/toggle', methods=['POST'])
@admin_required
def admin_api_toggle():
    """App on/off toggle"""
    data = read_data()
    current = data.get('app_status', 'on')
    data['app_status'] = 'off' if current == 'on' else 'on'
    write_data(data)
    return jsonify({'status': data['app_status']})

@app.route('/admin/api/clear', methods=['POST'])
@admin_required
def admin_api_clear():
    """Data clear karo"""
    what = request.get_json().get('what', '')
    data = read_data()
    if what == 'visitors':
        data['visitors'] = []
    elif what == 'queries':
        data['queries'] = []
    write_data(data)
    return jsonify({'ok': True})

# ─── Run ───────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
