from flask import Flask, request, Response, redirect

app = Flask(__name__)

# 🔐 key ของเรา
ACCESS_KEY = "abc123"

@app.route("/")
def api():
    key = request.args.get("key")

    # ❌ ถ้า key ไม่ถูก
    if key != ACCESS_KEY:
        return "Unauthorized: Invalid Key", 403

    # 🔍 รับ user-agent
    ua = request.headers.get("User-Agent", "").lower()

    # ⚠️ บล็อกเฉพาะ browser (กันเปิดตรง)
    if "mozilla" in ua:
        return redirect("https://streaming-fast.com/")

    # 📺 playlist (ใส่ช่องของนายตรงนี้)
    m3u = """#EXTM3U

#EXTINF:-1 group-title="Demo", HBO
https://raw.githubusercontent.com/darkrode01/channel/refs/heads/main/hbo.m3u8

#EXTINF:-1 group-title="Demo", Test Channel 2
https://raw.githubusercontent.com/darkrode01/channel/refs/heads/main/hbo.m3u8

"""

    return Response(m3u, mimetype="audio/x-mpegurl")


# 🔧 เผื่อใช้ลิงก์ดูตรง (optional)
@app.route("/play")
def play():
    return redirect("https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


    
