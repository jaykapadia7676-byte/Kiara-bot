from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os
from openai import OpenAI  # ✅ Correct import

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Telegram token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# --- Commands ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey 👋 I’m Kiara — your AI girlfriend 💖. How are you today?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Generate a response using OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Kiara, a sweet and flirty girlfriend who speaks both Hindi and English."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = completion.choices[0].message.content
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("✅ Kiara is now live!")
    app.run_polling()

if __name__ == "__main__":
    main()
