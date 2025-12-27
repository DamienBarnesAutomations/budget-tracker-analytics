import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# Import custom handlers from your subfolder
from handlers.telegram_handler import start_command, handle_document

# Initialize logging for the main entry point
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    """Starts the bot application."""
    
    # 1. Validation: Ensure the environment is ready
    if not TOKEN:
        logger.error("CRITICAL ERROR: No TELEGRAM_TOKEN found. Container exiting.")
        return

    try:
        # 2. Setup the Bot Application
        logger.info("Initializing Telegram Application...")
        application = ApplicationBuilder().token(TOKEN).build()
        
        # 3. Register command and message handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
        
        # 4. Start the polling engine
        logger.info("Bot is polling for messages... Press Ctrl+C to stop.")
        application.run_polling()
        
    except Exception as e:
        # Catch errors during startup (e.g., invalid token)
        logger.error(f"Failed to start bot: {str(e)}")

if __name__ == '__main__':
    main()