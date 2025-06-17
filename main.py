import requests
import time
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

# ==== CẤU HÌNH ====
COOKIE = "dán_cookie_facebook"
THREAD_ID = "id_box"
DELAY = 60  # Giây giữa mỗi lần gửi lại

headers = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": COOKIE
}

def get_fb_dtsg_and_uid():
    res = requests.get("https://m.facebook.com/messages", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    fb_dtsg = soup.find("input", {"name": "fb_dtsg"})["value"]
    jazoest = soup.find("input", {"name": "jazoest"})["value"]
    uid = COOKIE.split("c_user=")[1].split(";")[0]
    return fb_dtsg, jazoest, uid

def send_message(text, fb_dtsg, jazoest, uid):
    url = f"https://m.facebook.com/messages/send/?icm=1&refid=12"
    payload = {
        "fb_dtsg": fb_dtsg,
        "jazoest": jazoest,
        "body": text,
        "send": "Gửi",
        "tids": f"cid.c.{THREAD_ID}",
        "wwwupp": "C3",
        f"ids[{THREAD_ID}]": THREAD_ID
    }
    r = requests.post(url, headers=headers, data=payload)
    return "✅ Thành công" if "send_success" in r.text else "⚠️ Gửi xong"

def loop_send():
    fb_dtsg, jazoest, uid = get_fb_dtsg_and_uid()
    count = 1
    while True:
        with open("noidung.txt", "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content:
            print(f"🔁 [{count}] Gửi lại nội dung...")
            result = send_message(content, fb_dtsg, jazoest, uid)
            print(f"→ {result}")
        else:
            print("⚠️ File trống")
        count += 1
        time.sleep(DELAY)

# Web server để giữ cho Koyeb không tắt
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot đang chạy Koyeb"

Thread(target=loop_send).start()
app.run(host="0.0.0.0", port=8080)
