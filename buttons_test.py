import time
import telebot
import config
import task
from telebot import types
import resources.tests.test
import pathlib

bot = telebot.TeleBot(config.token)

currentTest = task.Test()


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
    global currentTest
    if get_message_bot == "тест о животных":
        currentTest = resources.tests.test.animalTestNew
    elif get_message_bot == "тест на эрудицию":
        currentTest = resources.tests.test.ingenuityTestNew
    doTest(message, 0)


def doTest(message, indexQuestion):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    markup.add(types.KeyboardButton(currentTest.questions[indexQuestion].answers[0]),
               types.KeyboardButton(currentTest.questions[indexQuestion].answers[1]),
               types.KeyboardButton(currentTest.questions[indexQuestion].answers[2]))
    msg = None

    if (indexQuestion != 0):
        currentTest.questions[indexQuestion - 1].usersAnswer = message.text.strip().lower()

    if currentTest.questions[indexQuestion].imagePath:
        msg = bot.send_photo(message.chat.id,
                             open(str(pathlib.Path.cwd()) +
                                "\\resources\\images\\" +
                                currentTest.questions[indexQuestion].imagePath, 'rb'),
                             currentTest.questions[indexQuestion].textQuestion,
                             reply_markup=markup)
    elif currentTest.questions[indexQuestion].filePath:
        msg = bot.send_document(message.chat.id,
                                 open(str(pathlib.Path.cwd()) +
                                    "\\resources\\additionalFiles\\" +
                                    currentTest.questions[indexQuestion].filePath, 'rb'),
                                 None,
                                 currentTest.questions[indexQuestion].textQuestion,
                                 reply_markup=markup)
    else:
        msg = bot.send_message(message.chat.id,
                               currentTest.questions[indexQuestion].textQuestion,
                               reply_markup=markup)

    indexQuestion = indexQuestion + 1
    if indexQuestion == len(currentTest.questions):
        bot.register_next_step_handler(msg, printResult)
    else:
        bot.register_next_step_handler(msg, doTest, indexQuestion)


def printFile(message, indexQuestion, markup):
    print("PRINTFILE")
    msg = bot.send_document(message.chat.id,
                           open(str(pathlib.Path.cwd()) +
                                "\\resources\\additionalFiles\\" +
                                currentTest.questions[indexQuestion].filePath, 'rb'),
                           reply_markup=markup)
    indexQuestion = indexQuestion + 1
    if indexQuestion == len(currentTest.questions):
        bot.register_next_step_handler(msg, printResult)
    else:
        bot.register_next_step_handler(msg, doTest, indexQuestion)

def printResult(message):
    currentTest.questions[-1].usersAnswer = message.text.strip().lower()
    result = currentTest.calculateResultTest()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('Начать сначала'))
    msg = bot.send_message(message.chat.id, "Колличество ваших баллов = " +
                           str(result[0]) + " из " + str(len(currentTest.questions)) +
                           "\nЭто составляет " + str(result[1]) + "%", reply_markup=markup)
    bot.register_next_step_handler(msg, start)


# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)
