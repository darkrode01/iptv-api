from flask import Flask, request, Response, redirect

app = Flask(__name__)

ACCESS_KEY = "abc123"

@app.route("/")
def api():
    key = request.args.get("key")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    ua = request.headers.get("User-Agent", "").lower()

    # 🔥 อนุญาตเฉพาะ player เท่านั้น
    allow = ["wiseplay", "vlc", "iptv", "exo", "player"]

    if not any(a in ua for a in allow):
        return redirect("https://google.com")

    # 📺 playlist
    m3u = """#EXTM3U

#EXTINF:-1 group-title="Demo", Test Channel
https://raw.githubusercontent.com/darkrode01/channel/refs/heads/main/hbo.m3u8

"""

    return Response(m3u, mimetype="audio/x-mpegurl")

