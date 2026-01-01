from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
BKASH = os.environ.get("BKASH_NUMBER")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = f"""
🔥 Welcome to AMIN Software 🔥

💳 bKash Payment Auto Receive

📌 Send Money: {BKASH}

পেমেন্ট পাঠানোর পর আপনার Transaction ID লিখে পাঠান।
"""
    await update.message.reply_text(msg)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tx = update.message.text

    admin_msg = f"""
🧾 New Payment Request

👤 User: {user.first_name}
🆔 User ID: {user.id}

📨 TXID: {tx}
"""
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg)
    await update.message.reply_text("✅ আপনার Transaction ID গ্রহণ করা হয়েছে। ধন্যবাদ।")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.run_polling()
