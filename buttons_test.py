import time
import telebot
import config
from telebot import types
import pathlib
import dbEngine
import task

bot = telebot.TeleBot(config.token)
currentTest = task.Test()

# @bot.message_handler(commands=['start'])
# def start(message):
#     dbEngine.addUserToDB(message.from_user.id, message.from_user.username)
#
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
#     btn1 = types.KeyboardButton('Тест о животных')
#     btn2 = types.KeyboardButton('Тест на эрудицию')
#     markup.add(btn1, btn2)
#     send_mess = f"<b>Привет {message.from_user.first_name}</b>!\nВыбирай тест и нажимай кнопку!"
#     bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)
#
# @bot.message_handler(content_types=['text'])
# def getUserText(message):
#     get_message_bot = message.text.strip().lower()
#     global currentTest
#     if get_message_bot == "тест о животных":
#         currentTest = dbEngine.readTestFromDB("Animals_1")
#     elif get_message_bot == "тест на эрудицию":
#         currentTest = dbEngine.readTestFromDB("IngenuityTest_1")
#     doTest(message, 0)

@bot.message_handler(commands=['start'])
def start(message):
    dbEngine.addUserToDB(message.from_user.id, message.from_user.username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Пройти тестирование')
    btn2 = types.KeyboardButton('Тренироваться')
    markup.add(btn1, btn2)
    send_mess = f"<b>Привет {message.from_user.first_name}</b>!\nВыбирай и нажимай кнопку!"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def getUserText(message):
    get_message_bot = message.text.strip().lower()
    global currentTest
    if get_message_bot == "пройти тестирование":
        generateTest(message)
    elif get_message_bot == "тренироваться":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
        markup.add(types.KeyboardButton('1'), types.KeyboardButton('2'), types.KeyboardButton('3'),
                   types.KeyboardButton('4'), types.KeyboardButton('5'), types.KeyboardButton('6'),
                   types.KeyboardButton('7'), types.KeyboardButton('8'), types.KeyboardButton('9'),
                   types.KeyboardButton('10'), types.KeyboardButton('11'), types.KeyboardButton('12'),
                   types.KeyboardButton('13'), types.KeyboardButton('14'), types.KeyboardButton('15'),
                   types.KeyboardButton('16'), types.KeyboardButton('17'), types.KeyboardButton('18'),
                   types.KeyboardButton('19'), types.KeyboardButton('20'), types.KeyboardButton('21'),
                   types.KeyboardButton('22'), types.KeyboardButton('23'), types.KeyboardButton('24'),
                   types.KeyboardButton('25'), types.KeyboardButton('26'), types.KeyboardButton('27'))
        msg = bot.send_message(message.chat.id,
                               "Выберите типовое задание:",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, selectTrainTask)

def selectTrainTask(message):
    print(message.text)

def generateTest(message):
    print("generateTest ", message.text)
    global currentTest
    currentTest = dbEngine.readTestFromDB("variant_1")
    doTest(message, 0)

def doTest(message, indexQuestion):
    markup = None
    if currentTest.questions[indexQuestion].answers :
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=len(currentTest.questions[indexQuestion].answers))
        markup.add(types.KeyboardButton(currentTest.questions[indexQuestion].answers[0]),
                   types.KeyboardButton(currentTest.questions[indexQuestion].answers[1]),
                   types.KeyboardButton(currentTest.questions[indexQuestion].answers[2]))

    if (indexQuestion != 0):
        currentTest.questions[indexQuestion - 1].usersAnswer = message.text.strip().lower()

    if currentTest.questions[indexQuestion].imagePath and not currentTest.questions[indexQuestion].filePath:
        msg = bot.send_photo(message.chat.id,
                             open(str(pathlib.Path.cwd()) +
                                "\\resources\\images\\" +
                                currentTest.questions[indexQuestion].imagePath, 'rb'),
                             currentTest.questions[indexQuestion].textQuestion,
                             reply_markup=markup)
    elif currentTest.questions[indexQuestion].filePath and not currentTest.questions[indexQuestion].imagePath:
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