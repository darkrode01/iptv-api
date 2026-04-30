from flask import Flask, request, jsonify, Response, redirect
import time

app = Flask(__name__)

ACCESS_KEY = "abc123"
SYSTEM_ON = True

# ===== STREAM =====
STREAMS = [
    {"name": "CH1", "url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8", "group": "Digital TV", "sub": "TV1"},
    {"name": "CH2", "url": "https://test-streams.mux.dev/test_001/stream.m3u8", "group": "Digital TV", "sub": "TV2"},
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

# ===== REDIRECT (DUFREE STYLE) =====
def redirect_browser():
    ua = request.headers.get("User-Agent", "").lower()
    accept = request.headers.get("Accept", "").lower()
    sec_fetch = request.headers.get("Sec-Fetch-Dest", "").lower()

    # ✅ allow player
    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return None

    # ✅ allow unknown clients (กันพลาด)
    if not accept:
        return None

    # 🔥 browser detection
    if "text/html" in accept or sec_fetch == "document":
        return redirect("https://google.com")

    return None


# ================= ROOT =================
@app.route("/")
def root():
    if not SYSTEM_ON:
        return "SYSTEM OFF", 403

    key = request.args.get("key")
    if key != ACCESS_KEY:
        return "Unauthorized", 403

    ua = request.headers.get("User-Agent", "").lower()
    accept = request.headers.get("Accept", "").lower()

    base = request.host_url.rstrip("/")

    # ================= ✅ WISEPLAY =================
    if any(x in ua for x in ["wiseplay", "vlc", "exo", "iptv"]):
        return jsonify({
            "name": "🅳🆄🅵🆁🅴🅴",
            "author": "Zank",
            "image": "https://cdn.dufreeapi.uk/dufreedd.png",
            "imageScale": "center",
            "url": f"{base}/enter?key={ACCESS_KEY}",
            "groups": [
                {
                    "name": "✨ เข้าสู่ระบบ",
                    "image": "https://cdn.dufreeapi.uk/dufree.gif",
                    "imageScale": "center",
                    "url": f"{base}/enter?key={ACCESS_KEY}",
                    "import": False
                }
            ]
        })

    # ================= 🔥 BROWSER =================
    if "text/html" in accept:
        return f"""
        <html>
        <head>
            <title>DUFREE</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {{
                    background:#000;
                    color:#fff;
                    text-align:center;
                    font-family:sans-serif;
                }}
                .box {{
                    margin-top:100px;
                }}
                img {{
                    width:120px;
                    border-radius:20px;
                }}
                .btn {{
                    display:inline-block;
                    margin-top:20px;
                    padding:12px 20px;
                    background:#ff0055;
                    color:#fff;
                    border-radius:10px;
                    text-decoration:none;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <img src="https://cdn.dufreeapi.uk/dufreedd.png"><br>
                <h2>DUFREE IPTV</h2>
                <p>กำลังโหลด...</p>
                <a class="btn" href="https://google.com">เข้าสู่ระบบ</a>
            </div>

            <script>
                setTimeout(() => {{
                    window.location.href = "https://google.com";
                }}, 1500);
            </script>
        </body>
        </html>
        """

    # ================= API FALLBACK =================
    return jsonify({
        "name": "API",
        "status": "OK"
    })

# ================= ENTER =================
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


# ================= GROUP =================
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


# ================= PLAYLIST =================
@app.route("/playlist")
def playlist():
    if not SYSTEM_ON:
        return "SYSTEM OFF", 403

    key = request.args.get("key")
    sub = request.args.get("sub")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    # ❗ playlist ไม่ redirect เด็ดขาด
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
