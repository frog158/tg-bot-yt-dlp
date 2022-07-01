import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
import json
import requests
import os


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=".join(result)"
    )


def main():
    TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN', 'error')
    if TG_BOT_TOKEN == 'error':
        print('Please set enviroment variable TG_BOT_TOKEN')
        return
    application = (
        ApplicationBuilder()
        .token(TG_BOT_TOKEN)
        .build()
    )

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
