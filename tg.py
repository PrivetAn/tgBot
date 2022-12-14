import telebot
from telebot import types
bot = telebot.TeleBot('5681988120:AAGILSBUeQ1vR5g_OAh_sUQ9yBcyo30PfCE')

# Функция, обрабатывающая команду /start
# @bot.message_handler(commands=["start"])
# def start(m, res=False):
#     bot.send_message(m.chat.id, 'Привет, как тебя зовут?')
# # Получение сообщений от юзера
#     bot.message_handler(content_types=["text"])
#     bot.send_message(m.chat.id, 'Очень рад знакомству, ' + m.text)
#     bot.message_handler(commands=['button'])
# def button_message(message):
#     markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1=types.KeyboardButton("Кнопка")
#     markup.add(item1)
#     bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
# @bot.message_handler(content_types='text')
# def message_reply(message):
#     if message.text=="Кнопка":
#         bot.send_message(message.chat.id,"https://habr.com/ru/users/lubaznatel/")

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Создать', 'Посмотреть')
    bot.send_message(message.chat.id, 'Привет! Выбери действие:', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'создать':
        bot.send_message(message.chat.id, 'создавай')
    if message.text.lower() == 'посмотреть':
        bot.send_message(message.chat.id, 'смотри')

# Запускаем бота
bot.polling(none_stop=True, interval=0)