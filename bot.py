import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Kiara bot is alive!"

def run_bot():
    import asyncio
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

    async def start(update, context):
        await update.message.reply_text("Hey, I'm Kiara 💋")

    async def chat(update, context):
        text = update.message.text
        await update.message.reply_text(f"You said: {text}")

    application = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    application.run_polling()

threading.Thread(target=run_bot).start()
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

