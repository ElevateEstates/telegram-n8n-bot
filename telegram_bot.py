import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from flask import Flask
from threading import Thread

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def keep_alive():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Telegram bot setup
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
N8N_WEBHOOK_URL = "https://elevateestates.app.n8n.cloud/webhook/1a1ba666-49f5-46d3-9891-8ee3eb816d4c/chat"

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Hi! I’m here to help with your shopping. I can list all items and their quantities in your inventory or add new items for you. "
        "Just let me know what you need—e.g., 'Show my inventory' or 'Add 2 soaps to Bathroom category.' What can I do for you today?"
    )

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id
    try:
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message, "chat_id": chat_id}, timeout=120)
        response.raise_for_status()
        data = response.json()
        print(f"n8n response: {data}")
        agent_response = data.get("output", "Sorry, I couldn't process your request.")
    except requests.RequestException as e:
        agent_response = f"Error: {str(e)}"
    await update.message.reply_text(agent_response)

def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    # Start Flask server in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    # Start Telegram bot
    main()
