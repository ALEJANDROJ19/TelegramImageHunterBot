"""
    A simple bot that hunt duplicate images in Telegram chats.
"""
import logging
from os import getenv, path, remove
from PIL import Image
import hashlib

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
picture_hash_list = []

HASH_FILE_PATH = "hash-images.txt"


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def picture(update, context):
    logger.info(update)

    if len(update.message.photo) > 1:
        file = update.message.photo[1].get_file()
        file_path = path.join(path.curdir, "photos", file.file_id + ".png")
        file.download(file_path)

        with open(file_path, mode="rb") as im:
            image = Image.open(im)
            image_bytes = image.tobytes()
            h = hashlib.sha3_256()
            h.update(image_bytes)
            image_hash = h.digest()
            if image_hash in picture_hash_list:
                logger.debug("duplicate found!")
                update.message.reply_text('Photo is duplicated!', quote=True)
            else:
                picture_hash_list.append(image_hash)
        remove(file_path)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def store_hashes():
    with open(HASH_FILE_PATH, mode="w") as file:
        file.write(str(picture_hash_list))


def load_hashes():
    global picture_hash_list
    if not path.exists(HASH_FILE_PATH):
        return
    with open(HASH_FILE_PATH, mode="r") as file:
        picture_hash_list = eval(file.read())


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    token = getenv("bot-token", "")
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.photo, picture))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    load_hashes()
    main()
    store_hashes()
