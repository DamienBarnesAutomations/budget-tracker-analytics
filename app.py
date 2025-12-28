import os
import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.telegram_handler import start_command, handle_document

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")

def main():
    if not TOKEN:
        logger.error("No TELEGRAM_TOKEN found.")
        return

    logger.info("Initializing Telegram Bot...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    
    application.run_polling()

if __name__ == '__main__':
    main()