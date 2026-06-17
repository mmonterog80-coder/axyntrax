import logging
logger = logging.getLogger(__name__)

def verify_webhook(request):
    return True

def process_instagram_update(update):
    pass

def send_instagram_message(chat_id, text):
    logger.info(f"Instagram message to {chat_id}: {text}")