from flask import Flask, request, jsonify, redirect
import time
import os

app = Flask(__name__)

ACCESS_KEY = "abc123"

# --------- ข้อมูลช่อง ---------
STREAMS = [
    {"name": "CH 1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV"},
    {"name": "Sport 1", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "กีฬา"},
    {"name": "Cartoon", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "การ์ตูน"},
]

# --------- online ---------
online = {}
TIMEOUT = 30

def clean_online():
    now = time.time()
    for ip in list(online.keys()):
        if now - online[ip] > TIMEOUT:
            del online[ip]

def add_online():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    online[ip] = time.time()

# --------- redirect browser ---------
def maybe_redirect():
    ua = request.headers.get("User-Agent", "").lower()
    if "mozilla" in ua and all(x not in ua for x in ["wiseplay", "vlc", "iptv", "exo"]):
        return redirect("https://streaming-fast.com/")
    return None

# ================= ROOT =================
@app.route("/")
def root():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = maybe_redirect()
    if r:
        return r

    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "🅳🆄🅵🆁🅴🅴",
        "author": "Zank",
        "image": "https://i.imgur.com/8Km9tLL.png",
        "url": f"{base}/home?key={ACCESS_KEY}",
        "groups": [
            {
                "name": "👉 เข้าสู่ระบบ",
                "url": f"{base}/home?key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": "🚫 ห้ามขาย",
                "info": "ระบบใช้ฟรีเท่านั้น",
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

    r = maybe_redirect()
    if r:
        return r

    base = request.host_url.rstrip("/")
    clean_online()

    return jsonify({
        "name": "DUFREE MENU",
        "groups": [
            {"name": "📺 Digital TV", "url": f"{base}/group?name=Digital TV&key={ACCESS_KEY}"},
            {"name": "🏀 กีฬา", "url": f"{base}/group?name=กีฬา&key={ACCESS_KEY}"},
            {"name": "🎬 การ์ตูน", "url": f"{base}/group?name=การ์ตูน&key={ACCESS_KEY}"}
        ],
        "stations": [
            {
                "name": f"🌐 Online: {len(online)} คน",
                "import": False
            }
        ]
    })

# ================= GROUP =================
@app.route("/group")
def group():
    key = request.args.get("key")
    name = request.args.get("name")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = maybe_redirect()
    if r:
        return r

    stations = []

    for ch in STREAMS:
        if ch["group"] == name:
            stations.append({
                "name": ch["name"],
                "url": ch["url"]
            })

    return jsonify({
        "name": name,
        "stations": stations
    })

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)# --------- หน้า Welcome ---------
@app.route("/")
def welcome():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = maybe_redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "🅼🆈 IPTV",
        "author": "Zank",
        "groups": [
            {
                "name": "✨ เข้าสู่เมนูหลัก",
                "url": f"{base}/home?key={ACCESS_KEY}"
            }
        ]
    })

# --------- หน้า Home ---------
@app.route("/home")
def home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = maybe_redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")
    clean_online()

    return jsonify({
        "name": "DUFREE",
        "groups": [
            {"name": "📺 Digital TV", "url": f"{base}/playlist?group=Digital TV&key={ACCESS_KEY}"},
            {"name": "🏀 กีฬา", "url": f"{base}/playlist?group=กีฬา&key={ACCESS_KEY}"},
            {"name": "🎬 การ์ตูน", "url": f"{base}/playlist?group=การ์ตูน&key={ACCESS_KEY}"}
        ],
        "stations": [
            {"name": f"🌐 Online {len(online)} คน", "import": False}
        ]
    })

# --------- playlist ---------
@app.route("/playlist")
def playlist():
    key = request.args.get("key")
    group = request.args.get("group")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    add_online()
    clean_online()

    m3u = "#EXTM3U\n\n"

    for ch in STREAMS:
        if group and ch["group"] != group:
            continue

        m3u += f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n\n'

    return Response(m3u, mimetype="audio/x-mpegurl")

# --------- run ---------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
