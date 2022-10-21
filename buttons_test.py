import time
import telebot
import config
from telebot import types
import resources.tests.test

bot = telebot.TeleBot(config.token)

questions = []
answers = []

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Тест о животных')
    btn2 = types.KeyboardButton('Тест на эрудицию')
    markup.add(btn1, btn2)
    send_mess = f"<b>Привет {message.from_user.first_name}</b>!\nВыберай тест и нажимай кнопку!"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def getUserText(message):
    get_message_bot = message.text.strip().lower()
    global questions
    if get_message_bot == "тест о животных":
        questions = list(resources.tests.test.animalTest.keys())
        doAnimalTest(message, 0)
    elif get_message_bot == "тест на эрудицию":
        # global questions
        questions = list(resources.tests.test.ingenuityTest.keys())
        doIngenuityTest(message, 0)

def doAnimalTest(message, indexQuestion) :
    print("doAnimalTest")
    print(questions[ indexQuestion ])
    print(resources.tests.test.animalTest[ questions[ indexQuestion ] ])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(types.KeyboardButton(resources.tests.test.animalTest[ questions[ indexQuestion ] ][ 0 ]),
               types.KeyboardButton(resources.tests.test.animalTest[ questions[ indexQuestion ] ][ 1 ]),
               types.KeyboardButton(resources.tests.test.animalTest[ questions[ indexQuestion ] ][ 2 ]))
    msg = bot.send_message(message.chat.id, questions[ indexQuestion ], reply_markup=markup)
    if (indexQuestion != 0): answers.append(message.text.strip().lower())
    indexQuestion = indexQuestion + 1
    if indexQuestion == len(questions) :
        bot.register_next_step_handler(msg, calculateTestResult)
    else : bot.register_next_step_handler(msg, doAnimalTest, indexQuestion)

def doIngenuityTest(message, indexQuestion) :
    print("doAnimalTest")
    print(questions[ indexQuestion ])
    print(resources.tests.test.animalTest[ questions[ indexQuestion ] ])
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    markup.add(types.KeyboardButton(resources.tests.test.ingenuityTest[ questions[ indexQuestion ] ][ 0 ]),
               types.KeyboardButton(resources.tests.test.ingenuityTest[ questions[ indexQuestion ] ][ 1 ]),
               types.KeyboardButton(resources.tests.test.ingenuityTest[ questions[ indexQuestion ] ][ 2 ]))
    msg = bot.send_message(message.chat.id, questions[ indexQuestion ], reply_markup=markup)
    if(indexQuestion != 0) : answers.append(message.text.strip().lower())
    indexQuestion = indexQuestion + 1
    if indexQuestion == len(questions) :
        bot.register_next_step_handler(msg, calculateTestResult)
    else : bot.register_next_step_handler(msg, doIngenuityTest, indexQuestion)

def calculateTestResult(message) :
    print("calculateTestResult")
    answers.append(message.text.strip().lower())
    print(answers)

# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
