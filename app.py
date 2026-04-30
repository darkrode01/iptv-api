from flask import Flask, request, jsonify, Response, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"

# ================= STREAM =================
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV1"},
    {"name": "CH3", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV2"},
]

online = {}
TIMEOUT = 30

# ================= ONLINE =================
def clean():
    now = time.time()
    for ip in list(online.keys()):
        if now - online[ip] > TIMEOUT:
            del online[ip]

def add():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    online[ip] = time.time()

# ================= REDIRECT =================
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()

    # ❗ อย่า redirect wiseplay
    if "mozilla" in ua and all(x not in ua for x in ["wiseplay", "vlc", "iptv", "exo"]):
        return redirect("https://google.com")

    return None


# ================= ROOT (หน้า DUFREE) =================
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
        "image": "https://cdn.dufreeapi.uk/dufreedd.png",
        "imageScale": "center",

        # 🔥 chain ต่อ
        "url": f"{base}/home?key={ACCESS_KEY}",

        "groups": [
            {
                "name": "✨ เข้าสู่ระบบ",
                "image": "https://cdn.dufreeapi.uk/dufree.gif",
                "imageScale": "center",
                "url": f"{base}/home?key={ACCESS_KEY}",
                "import": False
            }
        ],

        "stations": [
            {
                "name": "🚫 ห้ามขาย / ใช้ส่วนตัวเท่านั้น",
                "image": "https://media4.giphy.com/media/ky9nQzRcYaGhkwfH5i/200w.gif",
                "imageScale": "center",
                "info": "⚠️ ระบบนี้เพื่อความบันเทิงส่วนบุคคลเท่านั้น",
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
                "image": "https://i.imgur.com/8Km9tLL.png",
                "url": f"{base}/group?type=digital&key={ACCESS_KEY}"
            },
            {
                "name": "🏀 กีฬา",
                "image": "https://i.imgur.com/8Km9tLL.png",
                "url": f"{base}/group?type=sport&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": f"🌐 Online {len(online)} คน",
                "import": False
            }
        ]
    })


# ================= GROUP (TV1 TV2 แบบในรูป) =================
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
                "image": "https://i.imgur.com/1.png",
                "url": f"{base}/playlist?sub=TV1&key={ACCESS_KEY}"
            },
            {
                "name": "TV 2",
                "image": "https://i.imgur.com/2.png",
                "url": f"{base}/playlist?sub=TV2&key={ACCESS_KEY}"
            }
        ]
    })


# ================= PLAYLIST (M3U) =================
@app.route("/playlist")
def playlist():
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
