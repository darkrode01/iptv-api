from flask import Flask, request, jsonify
import time, os

app = Flask(__name__)

ACCESS_KEY = "abc123"

STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 1"},
    {"name": "Sport 1", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "กีฬา", "sub": "Sport"},
]

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

# ===== HOME =====
@app.route("/home")
def home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    clean()
    base = request.host_url.rstrip("/")
    ts = int(time.time())

    return jsonify({
        "name": "DUFREE MENU",
        "groups": [
            # 🔄 ปุ่มรีเฟรช (ต้องมี import:false)
            {
                "name": "🔄 รีเฟรช",
                "url": f"{base}/home?key={ACCESS_KEY}&t={ts}",
                "import": False
            },
            {
                "name": "📺 Digital TV",
                "url": f"{base}/group?g=Digital TV&key={ACCESS_KEY}"
            },
            {
                "name": "🏀 กีฬา",
                "url": f"{base}/group?g=กีฬา&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {"name": f"🌐 Online {len(online)}", "import": False},
            {"name": f"🕒 {time.strftime('%H:%M:%S')}", "import": False}
        ]
    })

# ===== GROUP =====
@app.route("/group")
def group():
    key = request.args.get("key")
    g = request.args.get("g")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    base = request.host_url.rstrip("/")
    subs = list(set([s["sub"] for s in STREAMS if s["group"] == g]))

    return jsonify({
        "name": g,
        "groups": [
            {"name": sub, "url": f"{base}/channels?sub={sub}&key={ACCESS_KEY}"}
            for sub in subs
        ]
    })

# ===== CHANNELS =====
@app.route("/channels")
def channels():
    key = request.args.get("key")
    sub = request.args.get("sub")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    add()
    clean()

    return jsonify({
        "name": sub,
        "stations": [
            {"name": s["name"], "url": s["url"]}
            for s in STREAMS if s["sub"] == sub
        ]
    })

# ===== RUN =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
