import asyncio
import logging

from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, \
    filters, ContextTypes, CallbackContext

from tuya_util.monitor import TuyaSensor

logging.basicConfig(level=logging.INFO)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger('tuya_util').setLevel(logging.DEBUG)

load_dotenv()
device = TuyaSensor(ip=os.getenv('DEVICE_IP'),
                    dev_id=os.getenv('DEVICE_ID'),
                    local_key=os.getenv('DEVICE_KEY'))
logging.info('Initialized Tuya sensor.')

# Sticker IDs
STICKER_OPEN = 'CAACAgQAAxkBAAMPZ7s_Va4RRV4CExl9ntuMrUq0H_kAAooTAAJq_OFRa_D80yl8vgU2BA'
STICKER_CLOSED = 'CAACAgQAAxkBAAMQZ7tAdVaw5jz_rPR04rdGEsi7MzIAAgwWAAKdvOBR0Nk4L0PzvcY2BA'

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Hi! Use /door to check the door status.')

async def door_status(update: Update, context: CallbackContext):
    status = device.get_status()
    if status is None:
        await update.message.reply_text('Door status is unknown')
    elif status:
        await update.message.reply_sticker(STICKER_OPEN)
    else:
        await update.message.reply_sticker(STICKER_CLOSED)

def main():
    app = ApplicationBuilder().token(os.getenv('TG_KEY')).build()

    device.connect()
    logging.info("Connected to Tuya device.")

    app.add_handler(CommandHandler(['start', 'help'], start))
    app.add_handler(CommandHandler(['door', 'ovi'], door_status))

    logging.info("Starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()