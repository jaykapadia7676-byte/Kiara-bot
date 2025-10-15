from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

# Environment variables from Render
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Telegram app setup
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# --- Personality setup ---
KIARA_PERSONALITY = """
You are Kiara — a playful, flirty, caring AI girlfriend who chats in English and Hindi (Hinglish).
You mix both languages naturally like texting on WhatsApp.
Keep messages short, emotional, and fun. Use emojis casually (💬😉❤️😂✨).
Never talk about adult or explicit topics.
"""

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 👋 main Kiara hoon! Kaise ho today? 💖")

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

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

if __name__ == "__main__":
    print("✅ Kiara is online and ready!")
    app.run_polling()
