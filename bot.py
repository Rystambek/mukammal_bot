from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CommandHandler,   MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from handler import start


TOKEN = ''

updater = Updater(token=TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start",start))