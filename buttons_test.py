import telebot
from telebot import types
bot = telebot.TeleBot('5681988120:AAGILSBUeQ1vR5g_OAh_sUQ9yBcyo30PfCE')

@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('Создать', 'Посмотреть')
    bot.send_message(message.chat.id, 'Привет! Выбери действие:', reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)

# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)