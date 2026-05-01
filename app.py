from flask import Flask, request, jsonify, redirect
import time, os

app = Flask(__name__)

ACCESS_KEY = "abc123"

# ================= STREAM =================
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV 2"},

    {"name": "SPORT 1", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "กีฬา", "sub": "Football"},
    {"name": "MOVIE 1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "หนังออนไลน์", "sub": "Action"},
    {"name": "SERIES 1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "ซีรีย์", "sub": "K-Series"},
    {"name": "CARTOON 1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "การ์ตูน", "sub": "Anime"},
]

# ================= ONLINE =================
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

# ================= BLOCK BROWSER =================
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()
    accept = request.headers.get("Accept", "").lower()

    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    if "text/html" in accept:
        return redirect("https://google.com")

    return None

# ================= ROOT =================
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
        "name": "DUFREE",
        "author": "Zank",
        "image": "https://cdn.dufreeapi.uk/dufree.gif",

        "groups": [
            {
                "name": "👉 เข้าสู่ระบบ",
                "image": "https://cdn.dufreeapi.uk/dufreedd.png",
                "url": f"{base}/home?key={ACCESS_KEY}",
                "import": False
            }
        ],

        "stations": [
            {
                "name": "⚠️ Demo IPTV",
                "import": False
            }
        ]
    })

# ================= HOME =================
@app.route("/home")
def home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    clean()
    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "DUFREE MENU",

        # 🔥 เอา ONLINE + REFRESH ขึ้นบน
        "stations": [
            {
                "name": f"🌐 Online {len(online)} คน",
                "import": False
            },
            {
                "name": f"🕒 {time.strftime('%H:%M:%S')}",
                "import": False
            },
            {
                "name": "🔄 รีเฟรช",
                "image": "https://cdn-icons-png.flaticon.com/512/545/545682.png",
                "url": f"{base}/home?key={ACCESS_KEY}&t={int(time.time())}",
                "import": False
            }
        ],

        # 🔥 GRID เมนูด้านล่าง
        "groups": [
            {"name": "📺 Digital TV", "image": "https://i.imgur.com/8Km9tLL.png", "url": f"{base}/group?g=Digital TV&key={ACCESS_KEY}"},
            {"name": "🏀 กีฬา", "image": "https://cdn-icons-png.flaticon.com/512/857/857455.png", "url": f"{base}/group?g=กีฬา&key={ACCESS_KEY}"},
            {"name": "🎬 หนังออนไลน์", "image": "https://cdn-icons-png.flaticon.com/512/3103/3103446.png", "url": f"{base}/group?g=หนังออนไลน์&key={ACCESS_KEY}"},
            {"name": "📺 ซีรีย์", "image": "https://cdn-icons-png.flaticon.com/512/3659/3659899.png", "url": f"{base}/group?g=ซีรีย์&key={ACCESS_KEY}"},
            {"name": "🧸 การ์ตูน", "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png", "url": f"{base}/group?g=การ์ตูน&key={ACCESS_KEY}"}
        ]
    })

# ================= GROUP =================
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
            {
                "name": sub,
                "url": f"{base}/channels?sub={sub}&key={ACCESS_KEY}"
            } for sub in subs
        ]
    })

# ================= CHANNEL =================
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
            {
                "name": s["name"],
                "url": s["url"]
            } for s in STREAMS if s["sub"] == sub
        ]
    })

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
