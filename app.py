from flask import Flask, request, jsonify, Response, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"

# 🔥 เปิด/ปิดลิงก์
SYSTEM_ON = True

# 🔥 stream จริง (ซ่อน)
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV2"},
]

# ===== online =====
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

# ===== redirect =====
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()

    # ❗ allow wiseplay
    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    if "mozilla" in ua:
        return redirect("https://google.com")

    return None

# ================= ROOT (ชั้นที่ 1) =================
@app.route("/")
def root():
    if not SYSTEM_ON:
        return "SYSTEM OFF", 403

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
        "imageScale": "center",

        # 🔥 chain ไปชั้น 2
        "url": f"{base}/enter?key={ACCESS_KEY}",

        "groups": [
            {
                "name": "✨ เข้าสู่ระบบ",
                "image": "https://cdn.dufreeapi.uk/dufreedd.png",
                "url": f"{base}/enter?key={ACCESS_KEY}",
                "import": False
            }
        ]
    })

# ================= ENTER (ชั้นที่ 2) =================
@app.route("/enter")
def enter():
    if not SYSTEM_ON:
        return "SYSTEM OFF", 403

    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")
    clean()

    return jsonify({
        "name": "DUFREE MENU",
        "groups": [
            {
                "name": "📺 Digital TV",
                "url": f"{base}/group?g=Digital TV&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": f"🌐 Online {len(online)} คน",
                "import": False
            }
        ]
    })

# ================= GROUP (ชั้นที่ 3) =================
@app.route("/group")
def group():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "📺 Digital TV",
        "groups": [
            {
                "name": "TV 1",
                "url": f"{base}/playlist?sub=TV1&key={ACCESS_KEY}"
            },
            {
                "name": "TV 2",
                "url": f"{base}/playlist?sub=TV2&key={ACCESS_KEY}"
            }
        ]
    })

# ================= PLAYLIST (ตัวจริง) =================
@app.route("/playlist")
def playlist():
    if not SYSTEM_ON:
        return "SYSTEM OFF", 403

    key = request.args.get("key")
    sub = request.args.get("sub")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    add()
    clean()

    m3u = "#EXTM3U\n\n"

    for ch in STREAMS:
        if ch["sub"] != sub:
            continue

        m3u += f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n\n'

    return Response(m3u, mimetype="audio/x-mpegurl")

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
