import os
import logging
import asyncio
import json
import requests # For making HTTP requests to the Gemini API

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- Configuration ---
# Get your Telegram Bot Token from BotFather
# It's highly recommended to use environment variables for security.
# Example: TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = "7097887916:AAE8b0W_OxMxbbra7xuVdbJ1BnxuKobg8x8" # <<< REPLACED WITH YOUR ACTUAL BOT TOKEN

# Gemini API configuration
# In the Canvas environment, leave apiKey as "" and it will be provided at runtime.
# If running outside Canvas, you would put your actual Gemini API key here.
GEMINI_API_KEY = "AIzaSyDScLlHp8JwDtcCjITNQPVZr4Aujkec6cU" # <<< REPLACED WITH YOUR ACTUAL GEMINI API KEY
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Logging Setup ---
# Enable logging to see what's happening in your bot
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- In-memory chat history (for simple context) ---
# In a real-world application, you might use a database for persistent history
# and per-user history. For this example, it's a simple dictionary.
chat_histories = {} # Stores chat history per chat_id: {chat_id: [{"role": "user", "parts": [...]}, ...]}

# --- Gemini API Call Function ---
async def call_gemini_api(prompt: str, chat_id: int) -> str:
    """
    Calls the Gemini API with the given prompt and returns the generated text.
    Maintains a simple in-memory chat history for context.
    """
    global chat_histories

    # Initialize chat history for the user if it doesn't exist
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    # Add the current user prompt to the history
    chat_histories[chat_id].append({"role": "user", "parts": [{"text": prompt}]})

    # Prepare the payload for the Gemini API request
    payload = {
        "contents": chat_histories[chat_id]
    }

    # Add API key to the URL
    api_url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"

    try:
        # Make the API call
        response = requests.post(api_url_with_key, headers={'Content-Type': 'application/json'}, json=payload)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()

        # Extract the text from the response
        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            gemini_response_text = result["candidates"][0]["content"]["parts"][0]["text"]
            # Add Gemini's response to the history
            chat_histories[chat_id].append({"role": "model", "parts": [{"text": gemini_response_text}]})
            return gemini_response_text
        else:
            logger.warning(f"Gemini API response structure unexpected: {result}")
            return "Sorry, I couldn't get a clear response from the AI."

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling Gemini API: {e}")
        return "Sorry, there was an error connecting to the AI. Please try again later."
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return "An unexpected error occurred while processing your request."

# --- Telegram Bot Handlers ---

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! I'm a Gemini-powered chatbot. "
        "Ask me anything, and I'll do my best to respond!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles incoming text messages and sends them to Gemini."""
    user_message = update.message.text
    chat_id = update.message.chat_id

    logger.info(f"User {update.effective_user.id} ({update.effective_user.full_name}) "
                f"in chat {chat_id} sent message: {user_message}")

    # Show a typing indicator while processing
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    # Call the Gemini API
    gemini_response = await call_gemini_api(user_message, chat_id)

    # Send the Gemini's response back to the user
    await update.message.reply_text(gemini_response)
    logger.info(f"Sent Gemini response to chat {chat_id}: {gemini_response[:50]}...") # Log first 50 chars

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("Oops! Something went wrong. Please try again.")

# --- Main function to run the bot ---
def main() -> None:
    """Starts the bot."""
    # Create the Application and pass your bot's token.
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Register error handler
    application.add_error_handler(error_handler)

    # Run the bot until you press Ctrl-C
    logger.info("Bot is starting to poll for updates...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("Bot stopped polling.")

if __name__ == "__main__":
    main()
