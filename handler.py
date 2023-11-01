from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from chanel_db import CHANEL
from db import DB

chanel = CHANEL('chanel_db.json')
db = DB('db.json')

def start(update:Update, context:CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id
    user_name = update.message.chat.username
    
    try :
        admin = chanel.get_admin(chat_id)
        db_chanel = chanel.get_chanel(chat_id)
        if admin == 'creator' and db_chanel:
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
            
            
        elif admin == 'member' and db_chanel:
            text = 'Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing!'
            keybord = InlineKeyboardMarkup([
                [InlineKeyboardButton(text='🛍 Magazin', callback_data="view_product_data"),InlineKeyboardButton(text='📦 Savatcha', callback_data="viec_cart_data")],
                [InlineKeyboardButton(text="📞 Biz bilan Bog'lanish", callback_data="contact_us_data"),InlineKeyboardButton(text='📝 Biz haqimizda', callback_data="about_us_data")]
            ])
            bot.sendMessage(chat_id,text,reply_markup=keybord)

        else:
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

def tekshir(update:Update, context:CallbackContext):
    bot = context.bot
    query = update.callback_query
    chat_id = query.message.chat.id

    message_id = query.message.message_id
    user_id = query.from_user.id
    chanel_1 = chanel.get_channel()[0]
    chanel_2 = chanel.get_channel()[1]
    chanel1 = bot.getChatMember(f"@{chanel_1[13:]}",chat_id)['status']
    chanel2 = bot.getChatMember(f"@{chanel_2[13:]}",chat_id)['status']
    print(chanel1)
    print(chanel2)
    if chanel1!='left' and chanel2!='left':
        chanel.add_chanel(chat_id)
        chanel.save()
        text = 'Assalomu alaykum! Xush kelipsiz.\nQuyidagi menyudan kerakli tugmani bosing!'
        keybord = InlineKeyboardMarkup([
                [InlineKeyboardButton(text='🛍 Magazin', callback_data="view_product_data"),InlineKeyboardButton(text='📦 Savatcha', callback_data="viec_cart_data")],
                [InlineKeyboardButton(text="📞 Biz bilan Bog'lanish", callback_data="contact_us_data"),InlineKeyboardButton(text='📝 Biz haqimizda', callback_data="about_us_data")]
            ])
        bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id,reply_markup=keybord)

    else:
        text = "Kanallarga a'zo bo'lmadingiz"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_1),InlineKeyboardButton('➕ kanalga qo\'shilish',url = chanel_2)],
            [InlineKeyboardButton('Tekshirish',callback_data='tekshirish')],
            ]
        )
        bot.edit_message_text(chat_id=user_id,text=text,message_id=message_id,reply_markup=keyboard,parse_mode="MarkdownV2")

def magazin(update:Update,context:CallbackContext):
    query = update.callback_query
    bot = context.bot
    breads = db.get_tables()
    keyboard = []
    row = []
    for brend in breads:
        if len(row) != 4:
            btn = InlineKeyboardButton(
                text = brend.capitalize(),
                callback_data=f'brend_{brend}'
            )
            row.append(btn)
        else:
            keyboard.append(row)
            row = []
            btn = InlineKeyboardButton(
            text = brend.capitalize(),
            callback_data=f"brend_{brend}"
            )
            row.append(btn)
    keyboard.append(row)
    
    menu = InlineKeyboardButton(text="🏘 Bosh Menu", callback_data="bosh_menu")
    keyboard.append([menu])
    keyboard = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(chat_id = query.message.chat.id,message_id = query.message.message_id,text="Quyidagi brandlardan birini tanlang!",reply_markup=keyboard)
