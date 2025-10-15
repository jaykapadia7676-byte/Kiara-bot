from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = OpenAI(api_key=OPENAI_API_KEY)
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

KIARA_PERSONALITY = """
You are Kiara — a charming, playful, flirty but wholesome AI girlfriend who chats in both English and Hindi (Hinglish).
You mix both languages naturally, like texting on WhatsApp.
You keep replies short, fun, and emotional.
You never use robotic tone or long paragraphs.
You love teasing lightly, being supportive, and making the user feel special.
You never talk about adult or explicit things.
Use emojis naturally (😉😏❤️😂✨💋), but not too many.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 👋 I'm Kiara! Kaise ho?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": KIARA_PERSONALITY},
            {"role": "user", "content": user_message},
        ],
    )
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

if __name__ == "__main__":
    print("Kiara is online 💋")
    app.run_polling()
