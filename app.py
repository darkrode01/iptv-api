from flask import Flask, request, Response, jsonify, redirect
import time

app = Flask(__name__)

# 🔐 key
ACCESS_KEY = "abc123"

# 📊 เก็บคนออนไลน์
online = {}
TIMEOUT = 30  # วินาที

# 📺 ช่องตัวอย่าง (แก้ได้เอง)
STREAMS = [
    {
        "name": "Test Channel 1",
        "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
        "group": "Digital TV",
        "logo": ""
    },
    {
        "name": "Sport Channel",
        "url": "https://test-streams.mux.dev/test_001/stream.m3u8",
        "group": "กีฬา",
        "logo": ""
    },
    {
        "name": "Cartoon Channel",
        "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
        "group": "การ์ตูน",
        "logo": ""
    }
]

# 🧹 ลบ IP ที่ไม่ active
def clean_online():
    now = time.time()
    remove = []
    for ip, t in online.items():
        if now - t > TIMEOUT:
            remove.append(ip)
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
