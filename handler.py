from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from chanel_db import CHANEL

chanel = CHANEL('chanel_db.json')

def start(update:Update, context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    user_name = update.message.from_user.first_name
    print(chat_id,user_name)
    text = "⛔️ *Botdan to'liq foydalanish uchun* quyidagi kanallarga obuna bo'ling"
    chanel.starting(chat_id=chat_id, user_name=user_name)
    chanel.save()
    chanel_1 = chanel.get_channel()[0]
    chanel_2 = chanel.get_channel()[1]
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
        [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
        ],
    )
    bot.sendMessage(chat_id,text,reply_markup=keyboard,parse_mode="MarkdownV2")