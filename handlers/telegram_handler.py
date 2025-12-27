import os
import logging
from telegram import Update
from telegram.ext import ContextTypes

# Standard logging config to capture timestamps and severity levels
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets the user and provides instructions."""
    logger.info(f"User {update.effective_user.id} started the bot.")
    await update.message.reply_text(
        "👋 Hello! I'm your Budget Tracker Analytics bot.\n\n"
        "Send me an **CSV file (.csv)** to begin."
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main handler to validate, download, and save incoming files."""
    document = update.message.document
    file_name = document.file_name

    # 1. Validation: Ensure the file is actually CSV
    if not (file_name.endswith('.csv')):
        logger.warning(f"Invalid file type received: {file_name}")
        await update.message.reply_text("❌ Error: Please send a valid CSV file (.csv).")
        return

    try:
        # 2. Inform user and prepare directory
        await update.message.reply_text(f"📥 Received: {file_name}. Downloading...")
        
        download_dir = "downloads"
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
            logger.info("Created 'downloads' directory.")

        file_path = os.path.join(download_dir, file_name)

        # 3. Fetch file from Telegram servers
        logger.info(f"Downloading {file_name}...")
        tg_file = await context.bot.get_file(document.file_id)
        
        # 4. Save to the Docker volume path
        await tg_file.download_to_drive(file_path)
        
        logger.info(f"Successfully saved: {file_path}")
        await update.message.reply_text(f"✅ File saved successfully! Processing will begin.")
        
        return file_path

    except Exception as e:
        # 5. Catch network errors or permission issues
        logger.error(f"Error handling document: {str(e)}", exc_info=True)
        await update.message.reply_text("⚠️ An error occurred while downloading the file. Please try again.")
        return None