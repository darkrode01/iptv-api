from flask import Flask, request, Response, jsonify, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"

# --------- ข้อมูลช่อง ---------
STREAMS = [
    {"name": "Test Channel 1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV"},
    {"name": "Sport Channel", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "กีฬา"},
    {"name": "Cartoon", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "การ์ตูน"},
]

# --------- นับคนออนไลน์แบบง่าย ---------
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

# --------- เช็ค browser → redirect ---------
def maybe_redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()
    # ถ้าเป็น browser (มี mozilla) และไม่ใช่ player ที่พบบ่อย → redirect
    if "mozilla" in ua and all(x not in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return redirect("https://streaming-fast.com/")
    return None

# --------- STEP A: Welcome ---------
@app.route("/")
def welcome():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    # เด้ง browser
    r = maybe_redirect_browser()
    if r: return r

    base = request.host_url.rstrip("/")

    data = {
        "name": "🅼🆈 IPTV",
        "author": "Zank",
        "groups": [
            {
                "name": "✨ ยินดีต้อนรับเข้าสู่ระบบ",
                "image": "https://cdn.dufreeapi.uk/dufree.gif",
                "imageScale": "center",
                "url": f"{base}/home?key={ACCESS_KEY}",
                "import": False
            }
        ],
        "stations": [
            {
                "name": "🚫 ห้ามจำหน่าย",
                "info": "ใช้เพื่อความบันเทิงส่วนบุคคลเท่านั้น",
                "import": False
            }
        ]
    }
    return jsonify(data)

# --------- STEP B: Home ---------
@app.route("/home")
def home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    r = maybe_redirect_browser()
    if r: return r

    base = request.host_url.rstrip("/")
    clean_online()

    data = {
        "name": "DUFREE",
        "author": "Zank",
        "image": "https://i.imgur.com/8Km9tLL.png",
        "groups": [
            {"name": "📢 แจ้งข่าวสาร", "url": f"{base}/playlist?group=แจ้งข่าวสาร&key={ACCESS_KEY}"},
            {"name": "📺 Digital TV", "url": f"{base}/playlist?group=Digital TV&key={ACCESS_KEY}"},
            {"name": "🎓 การศึกษา", "url": f"{base}/playlist?group=การศึกษา&key={ACCESS_KEY}"},
            {"name": "🎧 วิทยุ", "url": f"{base}/playlist?group=วิทยุ&key={ACCESS_KEY}"},
            {"name": "🎬 การ์ตูน", "url": f"{base}/playlist?group=การ์ตูน&key={ACCESS_KEY}"},
            {"name": "🏀 กีฬา", "url": f"{base}/playlist?group=กีฬา&key={ACCESS_KEY}"}
        ],
        "stations": [
            {"name": f"🌐 Online {len(online)} คน", "import": False},
            {"name": "🔄 รีเฟรช", "url": f"{base}/home?key={ACCESS_KEY}", "import": False}
        ]
    }
    return jsonify(data)

# --------- STEP C: Playlist (M3U) ---------
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

# --------- optional: play proxy ---------
@app.route("/play")
def play():
    url = request.args.get("url")
    return redirect(url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)                "name": "🎬 การ์ตูน",
                "url": f"{base}/playlist?group=การ์ตูน&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": "🌐 Online",
                "info": "ระบบ IPTV Demo",
                "import": False
            }
        ]
    }

    return jsonify(data)            remove.append(ip)
    for ip in remove:
        del online[ip]

# 🔥 STEP 1: JSON menu (เหมือน DUFREE)
@app.route("/")
def main():
    key = request.args.get("key")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    base = request.host_url.rstrip("/")

    clean_online()

    data = {
        "name": "🅼🆈 IPTV",
        "author": "Zank",
        "url": f"{base}/playlist?key={ACCESS_KEY}",
        "image": "https://i.imgur.com/8Km9tLL.png",
        "groups": [
            {
                "name": "📺 Digital TV",
                "url": f"{base}/playlist?group=Digital TV&key={ACCESS_KEY}"
            },
            {
                "name": "🏀 กีฬา",
                "url": f"{base}/playlist?group=กีฬา&key={ACCESS_KEY}"
            },
            {
                "name": "🎬 การ์ตูน",
                "url": f"{base}/playlist?group=การ์ตูน&key={ACCESS_KEY}"
            }
        ],
        "stations": [
            {
                "name": f"🌐 Online: {len(online)} คน",
                "info": "ระบบ IPTV Demo",
                "import": False
            }
        ]
    }

    return jsonify(data)

# 🔥 STEP 2: M3U playlist
@app.route("/playlist")
def playlist():
    key = request.args.get("key")
    group_filter = request.args.get("group")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    online[ip] = time.time()

    m3u = "#EXTM3U\n\n"

    for ch in STREAMS:
        if group_filter and ch["group"] != group_filter:
            continue

        m3u += f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n'
        m3u += f'{ch["url"]}\n\n'

    return Response(m3u, mimetype="audio/x-mpegurl")

# 🔥 STEP 3: proxy stream (optional)
@app.route("/play")
def play():
    url = request.args.get("url")
    return redirect(url)

# 🔥 STEP 4: ดูคนออนไลน์ (optional)
@app.route("/online")
def get_online():
    clean_online()
    return {"count": len(online), "ips": list(online.keys())}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
