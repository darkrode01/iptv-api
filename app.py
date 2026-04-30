from flask import Flask, request, Response

app = Flask(__name__)

ACCESS_KEY = "abc123"

@app.route("/")
def api():
    key = request.args.get("key")

    if key != ACCESS_KEY:
        return "Unauthorized", 403

    # ❗ ไม่ต้องเช็ค UA เลย (สำคัญ)
    
    m3u = """#EXTM3U

#EXTINF:-1 group-title="Demo", Test Channel
https://raw.githubusercontent.com/darkrode01/channel/refs/heads/main/hbo.m3u8

"""

    return Response(m3u, mimetype="audio/x-mpegurl")
