import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = int(os.environ.get("ADMIN_ID"))
BKASH_NUMBER = os.environ.get("BKASH_NUMBER")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"Welcome!\nSend payment to: {BKASH_NUMBER}\nAfter payment send your TxID."
    )

async def handle_txid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = update.message.text
    await update.message.reply_text("TxID received. Waiting for admin approval.")

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        msg = "\n".join([f"{uid}: {tx}" for uid, tx in users.items()])
        await update.message.reply_text("Pending Payments:\n" + msg)

app = ApplicationBuilder().token(os.environ.get("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_txid))
app.run_polling()
