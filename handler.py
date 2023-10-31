from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from chanel_db import CHANEL

chanel = CHANEL('chanel_db.json')

def start(update:Update, context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    user_name = update.message.chat.username
    
    try :
        admin = chanel.get_admin(chat_id)
        if admin == 'creator':
            text = 'Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing!'
            keybord = InlineKeyboardMarkup([
                [InlineKeyboardButton(text='🛍 Magazin', callback_data="view_product_data"),InlineKeyboardButton(text='📦 Savatcha', callback_data="viec_cart_data")],
                [InlineKeyboardButton(text="📞 Biz bilan Bog'lanish", callback_data="contact_us_data"),InlineKeyboardButton(text='📝 Biz haqimizda', callback_data="about_us_data")]
            ])
            bot.sendMessage(chat_id,text,reply_markup=keybord)

            text = 'Admin paneldan foydalana olasiz'
            admin=KeyboardButton('🔐 Admin')
            btn=ReplyKeyboardMarkup([[admin]],resize_keyboard=True)       
            bot.sendMessage(chat_id,text,reply_markup=btn)
            
            
        elif admin == 'member':
            text = "⛔️ *Botdan to'liq foydalanish uchun* quyidagi kanallarga obuna bo'ling"
            chanel_1 = chanel.get_channel()[0]
            chanel_2 = chanel.get_channel()[1]
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
                [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
                ],
            )
            bot.sendMessage(chat_id,text,reply_markup=keyboard,parse_mode="MarkdownV2")

    except KeyError:
        chanel.starting(chat_id=chat_id,user_name=user_name)
        chanel.save()
        admins = chanel.creator()
        total = chanel.get_users()

        for admin in admins:
            bot.send_message(chat_id=admin,text=f'🆕 Yangi Foydalanuvchi! \nUmumiy: [{len(total)}]\nIsmi: {update.message.chat.first_name}\nLinki: @{user_name}')
        text = "⛔️ *Botdan to'liq foydalanish uchun* quyidagi kanallarga obuna bo'ling"
        
        chanel_1 = chanel.get_channel()[0]
        chanel_2 = chanel.get_channel()[1]
        keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
                [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
                ],
            )
        bot.sendMessage(chat_id,text,reply_markup=keyboard,parse_mode="MarkdownV2")
