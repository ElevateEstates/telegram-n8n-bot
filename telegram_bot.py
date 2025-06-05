from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TELEGRAM_TOKEN = "7283514392:AAE_Pc-aMHUTgokl1aFNjA2aM782NMGbg0Y"
N8N_WEBHOOK_URL = "https://elevateestates.app.n8n.cloud/webhook/1a1ba666-49f5-46d3-9891-8ee3eb816d4c/chat"

def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chat_id = update.message.chat_id  # Already added for Simple Memory
    try:
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message, "chat_id": chat_id}, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(f"n8n response: {data}")  # Debug logging
        agent_response = data.get("output", "Sorry, I couldn't process your request.")  # Changed 'response' to 'output'
    except requests.RequestException as e:
        agent_response = f"Error: {str(e)}"
    update.message.reply_text(agent_response)


def start(update: Update, context: CallbackContext) -> None:
    welcome_message = "Hi! I’m here to help with your shopping. I can list all items and their quantities in your inventory or add new items for you. Just let me know what you need—e.g., 'Show my inventory' or 'Add 2 soaps to Bathroom category.' What can I do for you today?"
    update.message.reply_text(welcome_message)

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()