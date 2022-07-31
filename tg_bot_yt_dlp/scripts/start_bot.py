import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
)
from telegram.ext import ContextTypes, filters
import json
import requests
import os
import yt_dlp
from tg_bot_yt_dlp import genrss

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    URLS = ["https://www.youtube.com/watch?v=BaW_jenozKc"]

    ydl_opts = {
        "format": "m4a/bestaudio/best",
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(URLS)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=".join(result)"
    )


async def echo(update: Update, context: CallbackContext["ExtBot", dict, dict, dict]):
    TG_BOT_OUT_DIR = os.getenv("TG_BOT_OUT_DIR")
    TG_BOT_RELATIVE_MEDIA_DIR = "media"

    URLS = update.message.text
    YT_DLP_OPTIONS = {
        "format": "m4a/bestaudio/best",
        "outtmpl": f"{TG_BOT_OUT_DIR}/{TG_BOT_RELATIVE_MEDIA_DIR}/%(title)s.%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }
    with yt_dlp.YoutubeDL(YT_DLP_OPTIONS) as yt:
        error_code = yt.download(URLS)
    genrss.gen_zc(TG_BOT_RELATIVE_MEDIA_DIR, TG_BOT_OUT_DIR)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=error_code)


def main():
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "error")
    if TG_BOT_TOKEN == "error":
        print("Please set enviroment variable TG_BOT_TOKEN")
        return
    application = ApplicationBuilder().token(TG_BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    echo_handler = MessageHandler(filters.Entity("url"), echo)
    application.add_handler(echo_handler)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
