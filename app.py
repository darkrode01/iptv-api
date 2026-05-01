from flask import Flask, request, jsonify, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"

# 🔥 แบ่งเป็น group + sub
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV 2"},
    {"name": "CH3", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV 3"},
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

    # ❌ ถ้าเป็น player → ห้าม redirect
    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    # 🔥 อย่างอื่นเด้งหมด
    return redirect("https://google.com")


# ================= ROOT =================
@app.route("/")
def root():
    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "403", 403

    r = redirect_browser()   # 🔥 เพิ่มบรรทัดนี้
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
        return "403", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")
    clean()

    return jsonify({
        "name": "DUFREE MENU",

        # 🔥 กลุ่มใหญ่เหมือนรูป
        "groups": [
            {
                "name": "📺 Digital TV",
                "url": f"{base}/group?g=Digital TV&key={ACCESS_KEY}",
                "image": "https://i.imgur.com/8Km9tLL.png"
            }
        ],

        "stations": [
            {
                "name": f"🌐 Online {len(online)} คน",
                "import": False
            }
        ]
    })


# ================= GROUP (แยก TV1/2/3) =================
@app.route("/group")
def group():
    key = request.args.get("key")
    g = request.args.get("g")

    if key != ACCESS_KEY:
        return "403", 403

    r = redirect_browser()
    if r:
        return r

    base = request.host_url.rstrip("/")

    # 🔥 ดึง sub group เช่น TV1 TV2
    subs = list(set([s["sub"] for s in STREAMS if s["group"] == g]))

    groups = []
    for sub in subs:
        groups.append({
            "name": sub,
            "url": f"{base}/channels?sub={sub}&key={ACCESS_KEY}"
        })

    return jsonify({
        "name": g,
        "groups": groups
    })


# ================= CHANNELS =================
@app.route("/channels")
def channels():
    key = request.args.get("key")
    sub = request.args.get("sub")

    if key != ACCESS_KEY:
        return "403", 403

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
    app.run(host="0.0.0.0", port=10000)
