#!/usr/bin/env python
# pylint: disable=unused-argument

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from dotenv import load_dotenv
from importlib import import_module
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from os import getenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await update.message.reply_text("Teste")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  pass

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  """ Verify if user was nominated """
  scrappers = import_module("scrapers")
  scrapper = getattr(scrappers, "Trt21Scrapper")
  verify_nomination = scrapper()
  was_verified = verify_nomination()
  message = "Deu ruim"

  if was_verified:
    message = "Deu bom"

  await update.message.reply_text(text=message)

def main() -> None:
  """ Start the bot """
  token = getenv('TELEGRAM_BOT_TOKEN')
  # Create the Application and pass it your bot's token
  application = Application.builder().token(token).build()

  # on different commands - answer in Telegram
  application.add_handler(CommandHandler("start", start))
  # application.add_handler(CommandHandler("ajuda", help))
  application.add_handler(CommandHandler("verificar", verify))

  # Run the bot until the user presses Ctrl-C
  application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
  load_dotenv()
  main()
