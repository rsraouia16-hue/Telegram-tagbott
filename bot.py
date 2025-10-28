from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import asyncio
import os
import json
from flask import Flask
from threading import Thread

TOKEN = os.getenv("TOKEN")
active_users_file = "user.json"

try:
    with open(active_users_file, "r") as f:
        active_users = json.load(f)
except:
    active_users = {}

async def save_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.message.from_user
    chat_id = update.message.chat.id
    if chat_id not in active_users:
        active_users[chat_id] = {}
    if not u.is_bot:
        active_users[chat_id][u.id] = u.first_name
        with open(active_users_file, "w") as f:
            json.dump(active_users, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً! أنا بوت المنشن، أضفني إلى مجموعة واكتب /tagall علشان أعمل منشن للجميع 🔔"
    )

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    if chat_id not in active_users or not active_users[chat_id]:
        await update.message.reply_text("❌ لا يوجد مستخدمين")
        return

    await update.message.reply_text("⏳ جاري عمل المنشن... استنى شوي 🔄")

    members = active_users[chat_id]
    chunk_size = 30
    chunks = [list(members.items())[i:i + chunk_size] for i in range(0, len(members), chunk_size)]

    count = 0
    for chunk in chunks:
        text = " ".join(f"[{name}](tg://user?id={uid})" for uid, name in chunk)
        await update.message.reply_text(text, parse_mode="Markdown")
        count += len(chunk)
        await asyncio.sleep(2)

    await update.message.reply_text(f"✅ تم عمل منشن لعدد {count} عضو 🔔")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tagall", tag_all))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_user))

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "بوت شغال"

Thread(target=lambda: flask_app.run(host="0.0.0.0", port=8000)).start()

app.run_polling()