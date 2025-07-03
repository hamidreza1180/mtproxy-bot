import requests
import re
import time
import os
from telegram import Bot
from datetime import datetime

# 🔧 تنظیمات بات و کانال‌ها
BOT_TOKEN = "7911864165:AAFmbcevvrUcBzXDs5VkREfzVGbe9aMREmM"
CHANNEL = "@mtproxy1231"
SOURCES = [
    "https://t.me/ProxyMTProto",
    "https://t.me/Myporoxy",
    "https://t.me/ProxyMTProto_tel"
]
LAST_FILE = "last_sent.txt"
SPONSOR_FILE = "sponsors.txt"

# 🔌 اتصال به بات
bot = Bot(BOT_TOKEN)

# 📥 گرفتن اسپانسر از فایل
def get_sponsor():
    try:
        with open(SPONSOR_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
            if lines:
                return lines[0]  # فقط خط اول
    except:
        pass
    return "@mtproxy1231"

# 🔄 جایگزینی اسپانسر در لینک
def replace_sponsor(link):
    # حذف اسپانسر قبلی
    link = re.sub(r"&usercomment=Join\+@[\w\d_]+", "", link)
    sponsor = get_sponsor()
    return link + f"&usercomment=Join+{sponsor}"

# 🧠 خواندن آخرین لینک
def load_last():
    if os.path.exists(LAST_FILE):
        return open(LAST_FILE).read().strip()
    return ""

# 💾 ذخیره آخرین لینک
def save_last(link):
    with open(LAST_FILE, "w") as f:
        f.write(link)

# 🌐 استخراج لینک‌های پروکسی از کانال‌ها
def fetch_proxies():
    proxies = []
    for ch in SOURCES:
        try:
            html = requests.get(ch, timeout=10).text
            found = re.findall(r"https://t\.me/proxy\?server=[^\" \n&]+&port=[^\" \n&]+&secret=[^\" \n&]+(?:&usercomment=[^\" \n&]*)?", html)
            proxies += found
        except:
            continue
    return list(set(proxies))

# 🚀 اجرای اصلی
def main():
    print(f"[{datetime.now()}] شروع بررسی پروکسی‌ها")
    last = load_last()
    all_proxies = fetch_proxies()
    new_proxies = [p for p in all_proxies if p != last]

    if not new_proxies:
        print("⛔ هیچ پروکسی جدیدی پیدا نشد.")
        return

    selected = new_proxies[0]
    final_link = replace_sponsor(selected)
    bot.send_message(CHANNEL, f"🔗 {final_link}")
    save_last(selected)
    print("✅ لینک جدید ارسال شد:", final_link)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(15)  # اجرای دوباره هر ۱۵ ثانیه