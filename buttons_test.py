import time
import telebot
import config

bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет")

@bot.message_handler(content_types=['text'])
def getUserText(message):
    bot.send_message(message.from_user.id, message.text)

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     print(message)
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
