from flask import Flask, request, Response, redirect

app = Flask(__name__)

ACCESS_KEY = "abc123"

@app.route("/")
def api():
    key = request.args.get("key")

    # ❌ key ผิด
    if key != ACCESS_KEY:
        return "Unauthorized: Invalid Key", 403

    # 🔍 ตรวจว่าเป็น player ไหม
    ua = request.headers.get("User-Agent", "").lower()

    if not any(x in ua for x in ["wiseplay", "vlc", "iptv", "exo"]):
        return redirect("https://google.com")

    # 📺 playlist (ตัวอย่าง)
    m3u = """#EXTM3U

#EXTINF:-1 group-title="Demo", Test Channel
https://raw.githubusercontent.com/darkrode01/channel/refs/heads/main/hbo.m3u8

"""

    return Response(m3u, mimetype="audio/x-mpegurl")
