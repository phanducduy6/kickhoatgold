import asyncio
import os
from threading import Thread

from flask import Flask
from telebot.async_telebot import AsyncTeleBot

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Set the TELEGRAM_BOT_TOKEN environment variable before starting the bot.")

bot = AsyncTeleBot(BOT_TOKEN)
app = Flask(__name__)


@app.get("/")
def health_check():
    return "Bot dang hoat dong!"


def run_web():
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, use_reloader=False)


def keep_alive():
    Thread(target=run_web, daemon=True).start()

@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await bot.reply_to(
        message,
        "Xin chào! Bot này chỉ cung cấp thông tin hỗ trợ Locket.\n"
        "Dùng /gold để xem cách đăng ký Locket Gold chính thức.",
    )

@bot.message_handler(commands=["gold"])
async def explain_official_subscription(message):
    await bot.reply_to(
        message,
        "Locket Gold cần được đăng ký qua ứng dụng Locket hoặc kênh thanh toán "
        "chính thức. Bot không thể kích hoạt, thay đổi hoặc xác minh gói thuê bao. "
        "Nếu bạn đã thanh toán nhưng chưa có quyền lợi, hãy liên hệ bộ phận hỗ trợ "
        "Locket hoặc cửa hàng nơi bạn mua.",
    )

async def main():
    await bot.polling()

if __name__ == "__main__":
    keep_alive()
    asyncio.run(main())