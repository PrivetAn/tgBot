import telebot
from telebot import types
bot = telebot.TeleBot('5681988120:AAGILSBUeQ1vR5g_OAh_sUQ9yBcyo30PfCE')

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