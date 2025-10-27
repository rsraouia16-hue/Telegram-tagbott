from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

TOKEN = "8283617676:AAEZ5xdUqjTrDAPJWu1yXGGXE8ByH-plQvA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! أنا بوت المنشن، أضفني إلى مجموعة واكتب /tagall علشان أعمل منشن للجميع 🔔")

async def tag_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("هذا الأمر يعمل فقط داخل المجموعات 😅")
        return

    await update.message.reply_text("⏳ جاري عمل المنشن... استنى شوي 🔄")

    members = []
    try:
        async for member in context.bot.get_chat_members(chat.id):
            user = member.user
            if not user.is_bot:
                members.append(user)
    except Exception as e:
        await update.message.reply_text(f"⚠️ خطأ أثناء جلب الأعضاء: {e}")
        return

    usernames = [f"@{u.username}" if u.username else u.first_name for u in members]

    chunk_size = 30
    chunks = [usernames[i:i + chunk_size] for i in range(0, len(usernames), chunk_size)]

    count = 0
    for chunk in chunks:
        text = " ".join(chunk)
        await update.message.reply_text(text)
        count += len(chunk)
        await asyncio.sleep(2)

    await update.message.reply_text(f"✅ تم عمل منشن لعدد {count} عضو 🔔")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("tagall", tag_all))

print("✅ البوت شغال الآن...")
app.run_polling()