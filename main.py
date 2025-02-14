from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    ChatMemberHandler,
)

from deep_translator import GoogleTranslator,single_detection
import logging



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! I am a translation bot. Add me to your group or channel, "
        "and I will automatically translate Amharic messages to Afan Oromo and vice versa."
    )

async def handle_chat_member_update(update: Update, context: CallbackContext):
    if update.my_chat_member.new_chat_member.status == "member":
        chat_id = update.my_chat_member.chat.id
        chat_title = update.my_chat_member.chat.title
        logger.info(f"Bot added to group/channel: {chat_title} (ID: {chat_id})")
        await context.bot.send_message(
            chat_id=chat_id,
            text="Thanks for adding me! I will translate Amharic messages to Afan Oromo and vice versa.",
        )

async def translate(update: Update, context: CallbackContext):
    text = update.message.text
    
    try:
        lang = single_detection(text, api_key='f52e9f14002ed9aed98b85842e196132')
        if lang == 'am':
            translated_text_en = GoogleTranslator(source='am', target='en').translate(text)
            translated_text_om = GoogleTranslator(source='am', target='om').translate(text)
            translated_text = f"{text}\n\nAfan Oromo\n\n {translated_text_om}\n\nEnglish\n\n {translated_text_en}"
        elif lang == 'om':
            translated_text_am = GoogleTranslator(source='om', target='am').translate(text)
            translated_text_en = GoogleTranslator(source='om', target='en').translate(text)
            translated_text = f"{text}\n\nAmharic\n\n {translated_text_am}\n\nEnglish\n\n {translated_text_en}"
        elif lang == 'en':
            translated_text_am = GoogleTranslator(source='en', target='am').translate(text)
            translated_text_om = GoogleTranslator(source='en', target='om').translate(text)
            translated_text = f"{text}\n\nAmharic\n\n {translated_text_am}\n\nAfan Oromo\n\n {translated_text_om}"
        else:
            translated_text = "Unsupported language!"
        await update.message.delete()
        await context.bot.send_message(chat_id=update.message.chat_id, text=translated_text)
    except Exception as e:
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"An error occurred: {e}")


def main():
    TOKEN = "7831252672:AAHJ_JhJDajCVsO506jSSwleOo9NqTG4LRU"
    
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(ChatMemberHandler(handle_chat_member_update))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    application.run_polling()

if __name__ == "__main__":
    main()
