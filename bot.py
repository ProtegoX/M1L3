import telebot # telebot lib
from config import token # importing token

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi, I am ChatMod bot")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: 
        chat_id = message.chat.id 
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 

        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "You can't ban and admin")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"user @{message.reply_to_message.from_user.username} was blocked.")
    else:
        bot.reply_to(message, "you must call the ban statement in reply to the message you want to ban.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if "https://" == message.text[:8]:
        
        chat_id = message.chat.id 
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
        if user_status != 'administrator' or user_status != 'creator':
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"user @{message.reply_to_message.from_user.username} was blocked.")
    
    else:    
        bot.reply_to(message, message.text) 

bot.infinity_polling(none_stop=True)
