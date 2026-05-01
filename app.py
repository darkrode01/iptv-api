from flask import Flask, request, jsonify, redirect
import time
import os

app = Flask(__name__)

ACCESS_KEY = "abc123"

# ===== STREAM =====
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV 2"},
    {"name": "CH3", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 3"},
]

# ===== ONLINE =====
online = {}
TIMEOUT = 30

def clean():
    now = time.time()
    for ip in list(online.keys()):
        if now - online[ip] > TIMEOUT:
            del online[ip]

def add():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    online[ip] = time.time()

# ===== REDIRECT =====
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()

    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    return redirect("https://google.com")

# ================= FAKE ROOT =================
@app.route("/")
def root():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "🅳🆄🅵🆁🅴🅴",
        "author": "Zank",
        "image": "https://cdn.dufreeapi.uk/dufree.gif",

        # 🔥 chain ไปตัวจริง
        "url": f"{base}/main/home?key={ACCESS_KEY}",

        "groups": [
            {
                "name": "👉 เข้าสู่ระบบ",
                "url": f"{base}/main/home?key={ACCESS_KEY}",
                "import": False
            }
        ]
    })

# ================= REAL HOME =================
@app.route("/main/home")
def main_home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    base = request.host_url.rstrip("/")
    clean()

    return jsonify({
        "name": "DUFREE MENU",
        "groups": [
            {
                "name": "📺 Digital TV",
                "url": f"{base}/main/group?g=Digital TV&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": f"🌐 Online {len(online)} คน",
                "import": False
            }
        ]
    })

# ================= GROUP =================
@app.route("/main/group")
def group():
    key = request.args.get("key")
    g = request.args.get("g")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    base = request.host_url.rstrip("/")

    subs = list(set([s["sub"] for s in STREAMS if s["group"] == g]))

    groups = []
    for sub in subs:
        groups.append({
            "name": sub,
            "url": f"{base}/main/channels?sub={sub}&key={ACCESS_KEY}"
        })

    return jsonify({
        "name": g,
        "groups": groups
    })

# ================= CHANNELS =================
@app.route("/main/channels")
def channels():
    key = request.args.get("key")
    sub = request.args.get("sub")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    add()
    clean()

    stations = []

    for s in STREAMS:
        if s["sub"] == sub:
            stations.append({
                "name": s["name"],
                "url": s["url"]
            })

    return jsonify({
        "name": sub,
        "stations": stations
    })

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
