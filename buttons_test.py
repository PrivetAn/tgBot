import time
import telebot
import config
import task
from telebot import types
import resources.tests.test

bot = telebot.TeleBot(config.token)

test = {}
keys = []
questions = []
answers = []
currentTest = task.Test()

@bot.message_handler(commands=['start'])
def start(message):
    answers.clear()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Тест о животных')
    btn2 = types.KeyboardButton('Тест на эрудицию')
    markup.add(btn1, btn2)
    send_mess = f"<b>Привет {message.from_user.first_name}</b>!\nВыберай тест и нажимай кнопку!"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def getUserText(message):
    get_message_bot = message.text.strip().lower()
    global test
    global keys
    global questions
    global currentTest
    if get_message_bot == "тест о животных":
        test = resources.tests.test.animalTest
        questions = list(resources.tests.test.animalTest.keys())
        keys = list(resources.tests.test.animalTest_keys.values())
        currentTest = resources.tests.test.animalTestNew
    elif get_message_bot == "тест на эрудицию":
        test = resources.tests.test.ingenuityTest
        questions = list(resources.tests.test.ingenuityTest.keys())
        keys = list(resources.tests.test.ingenuityTest_keys.values())
        currentTest = resources.tests.test.ingenuityTestNew
    doTest(message, 0)

def doTest(message, indexQuestion) :
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    # markup.add(types.KeyboardButton(test[ questions[ indexQuestion ] ][ 0 ][ 0 ]),
    #            types.KeyboardButton(test[ questions[ indexQuestion ] ][ 0 ][ 1 ]),
    #            types.KeyboardButton(test[ questions[ indexQuestion ] ][ 0 ][ 2 ]))
    print(currentTest.questions[ indexQuestion ].textQuestion)
    markup.add(types.KeyboardButton(currentTest.questions[ indexQuestion ].answers[ 0 ]),
               types.KeyboardButton(currentTest.questions[ indexQuestion ].answers[ 1 ]),
               types.KeyboardButton(currentTest.questions[ indexQuestion ].answers[ 2 ]))
    # msg = bot.send_message(message.chat.id, questions[ indexQuestion ], reply_markup=markup)
    msg = bot.send_message(message.chat.id, currentTest.questions[ indexQuestion ].textQuestion, reply_markup=markup)
    if (indexQuestion != 0): answers.append(message.text.strip().lower())
    indexQuestion = indexQuestion + 1
    if indexQuestion == len(currentTest.questions) :
        bot.register_next_step_handler(msg, calculateTestResult)
    else : bot.register_next_step_handler(msg, doTest, indexQuestion)

def calculateTestResult(message) :
    answers.append(message.text.strip().lower())
    print("answers = ", answers)
    print("keys = ", keys)
    score = 0
    for i in range(len(answers)) :
        if answers[ i ].lower() == keys[ i ].lower() : score += 1
    print("score =", score)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('Начать сначала'))
    msg = bot.send_message(message.chat.id, "Колличество ваших баллов = " + str(score) + " из " + str(len(answers)) +
                           "\nЭто составляет " + str(round(score / len(answers) * 100, 2)) + "%", reply_markup=markup)
    bot.register_next_step_handler(msg, start)

# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
