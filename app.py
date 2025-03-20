import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("api_key")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Define Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from Gemini API
def get_gemini_response(user_message):
    try:
        response = model.generate_content(user_message)
        return response.text if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {str(e)}"

# Start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I am your chatbot. How can I assist you?")

# Message handler to reply with Gemini API response
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = get_gemini_response(user_message)
    await update.message.reply_text(response)

# Main function to set up bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
