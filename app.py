from flask import Flask, request, jsonify, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"

STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV"},
    {"name": "SPORT", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "กีฬา"},
    {"name": "CARTOON", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "การ์ตูน"},
]

online = {}
TIMEOUT = 30


# --------- online ----------
def clean():
    now = time.time()
    for ip in list(online.keys()):
        if now - online[ip] > TIMEOUT:
            del online[ip]

def add():
    ip = request.remote_addr
    online[ip] = time.time()


# --------- redirect ----------
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()
    accept = request.headers.get("Accept", "").lower()

    # ❌ ถ้าเป็น Wiseplay / Player → ห้าม redirect
    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    # ✅ ถ้าเป็น browser จริง → redirect
    if "text/html" in accept:
        return redirect("https://google.com")

    return None


# ================= ROOT =================
@app.route("/")
def root():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "403", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")

    return jsonify({
        "name": "🅳🆄🅵🆁🅴🅴",
        "author": "Zank",

        # 🔥 ใส่ตัวนี้เข้าไป
        "url": f"{base}/home?key={ACCESS_KEY}",

        "image": "https://i.imgur.com/8Km9tLL.png",

        "groups": [
            {
                "name": "👉 เข้าสู่ระบบ",
                "url": f"{base}/home?key={ACCESS_KEY}"
            }
        ]
    })



# ================= HOME =================
@app.route("/home")
def home():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "403", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")
    clean()

    return jsonify({
        "name": "DUFREE MENU",
        "groups": [
            {"name": "📺 Digital TV", "url": f"{base}/group?g=Digital TV&key={ACCESS_KEY}"},
            {"name": "🏀 กีฬา", "url": f"{base}/group?g=กีฬา&key={ACCESS_KEY}"},
            {"name": "🎬 การ์ตูน", "url": f"{base}/group?g=การ์ตูน&key={ACCESS_KEY}"}
        ],
        "stations": [
            {
                "name": f"🌐 Online: {len(online)}",
                "import": False
            }
        ]
    })


# ================= GROUP =================
@app.route("/group")
def group():
    key = request.args.get("key")
    g = request.args.get("g")

    if key != ACCESS_KEY:
        return "403", 403

    r = redirect_browser()
    if r:
        return r

    add()
    clean()

    stations = []

    for s in STREAMS:
        if s["group"] == g:
            stations.append({
                "name": s["name"],
                "url": s["url"]
            })

    return jsonify({
        "name": g,
        "stations": stations
    })
