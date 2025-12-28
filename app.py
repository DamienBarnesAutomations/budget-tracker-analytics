import os
import logging
from threading import Thread
from flask import Flask
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from waitress import serve

# Import custom handlers from your subfolder
from handlers.telegram_handler import start_command, handle_document

# --- FLASK SERVER FOR RENDER HEALTH CHECK ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # This replaces app.run() and removes the Warning
    serve(app, host='0.0.0.0', port=port)
# --------------------------------------------

# Initialize logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    """Starts the bot application."""
    
    if not TOKEN:
        logger.error("CRITICAL ERROR: No TELEGRAM_TOKEN found. Container exiting.")
        return

    # 1. Start the Flask server in a background thread
    logger.info("Starting health check server...")
    Thread(target=run_flask, daemon=True).start()

    try:
        # 2. Setup the Bot Application
        logger.info("Initializing Telegram Application...")
        application = ApplicationBuilder().token(TOKEN).build()
        
        # 3. Register command and message handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        
        # 4. Start the polling engine
        logger.info("Bot is polling for messages...")
        application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {str(e)}")

if __name__ == '__main__':
    main()