from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CommandHandler,   MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from handler import start


TOKEN = '6787477123:AAHMi_hfGusB1EUQaAe7m-kYoBgLose9PZc'

updater = Updater(token=TOKEN)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start",start))
updater.start_polling()
updater.idle()