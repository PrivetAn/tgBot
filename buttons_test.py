import time
import telebot
import config
from telebot import types
import pathlib
import dbEngine
import task
import matplotlib.pyplot as plt

bot = telebot.TeleBot(config.token)
currentTest = task.Test()
training = False

@bot.message_handler(commands=['start'])
def start(message):
    print("START")
    dbEngine.addUserToDB(message.from_user.id, message.from_user.username)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Пройти тестирование')
    btn2 = types.KeyboardButton('Тренироваться')
    btn3 = types.KeyboardButton('Статистика')
    btn4 = types.KeyboardButton('Теория')
    markup.add(btn1, btn2, btn3, btn4)
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
    elif get_message_bot == "статистика":
        resultValues = dbEngine.getUserResultFromDB(message.from_user.id)
        print("results = ", resultValues)

        #График сохраняется по указанному пути
        path = 'plot_results.png'
        getPlot(resultValues, path)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Пройти тестирование')
        btn2 = types.KeyboardButton('Тренироваться')
        btn3 = types.KeyboardButton('Статистика')
        markup.add(btn1, btn2, btn3)
        bot.send_photo(message.chat.id, photo=open(path, 'rb'))
        # send_mess = f"<b>Привет {message.from_user.first_name}</b>!\nВыбирай и нажимай кнопку!"
        # bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)
    elif get_message_bot == "теория":
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
                               "Выберите тип задания, по которому вы хотите изучить теорию:",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, printTheory)
def selectTrainTask(message):
    print(message.text)
    global currentTest
    global training
    training = True
    currentTest = dbEngine.readTaskFromDB(message.text)
    doTest(message, 0)

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

    textForSend = str("<b>Задание №" +
                      str(currentTest.questions[indexQuestion].type) + "</b>\n" +
                      correctMessage(currentTest.questions[indexQuestion].textQuestion))

    if currentTest.questions[indexQuestion].imagePath and not currentTest.questions[indexQuestion].filePath:
        bot.send_photo(message.chat.id,
                       open(str(pathlib.Path.cwd()) +
                            "\\resources\\images\\" +
                            currentTest.questions[indexQuestion].imagePath, 'rb'))
    elif currentTest.questions[indexQuestion].filePath and not currentTest.questions[indexQuestion].imagePath:
        bot.send_document(message.chat.id,
                          open(str(pathlib.Path.cwd()) +
                               "\\resources\\additionalFiles\\" +
                               currentTest.questions[indexQuestion].filePath, 'rb'),
                               None)
    msg = bot.send_message(message.chat.id,
                           textForSend,
                           parse_mode='html',
                           reply_markup=markup)
    indexQuestion = indexQuestion + 1
    if indexQuestion == len(currentTest.questions):
        if(training) : bot.register_next_step_handler(msg, start)
        else : bot.register_next_step_handler(msg, printResult)
    else:
        bot.register_next_step_handler(msg, doTest, indexQuestion)

def printResult(message):
    currentTest.questions[-1].usersAnswer = message.text.strip().lower()
    result = currentTest.calculateResultTest()

#   Запись результата в БД
    dbEngine.addUserResultToDB(message.from_user.id, result[1])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('Начать сначала'))
    msg = bot.send_message(message.chat.id, "Колличество ваших баллов = " +
                           str(result[0]) + " из " + str(len(currentTest.questions)) +
                           "\nЭто составляет " + str(result[1]) + "%", reply_markup=markup)
    bot.register_next_step_handler(msg, start)

def printTheory(message):
    print(message.text)

    theory = dbEngine.readTheoryFromDB(message.text)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton('В начало'))

    textForSend = str("<b>Задание №" +
                      str(theory.type) + "</b>\n" +
                      correctMessage(theory.textTheory))

    print("textForSend = ", textForSend)

    if theory.imagePath and not theory.filePath:
        print("theory.imagePath = ", theory.imagePath)
        bot.send_photo(message.chat.id,
                       open(str(pathlib.Path.cwd()) +
                            "\\resources\\images\\" +
                            theory.imagePath, 'rb'))
    elif theory.filePath and not theory.imagePath:
        print("theory.filePath = ", theory.filePath)
        bot.send_document(message.chat.id,
                          open(str(pathlib.Path.cwd()) +
                               "\\resources\\additionalFiles\\" +
                               theory.filePath, 'rb'),
                               None)
    elif theory.filePath and theory.imagePath:
        bot.send_photo(message.chat.id,
                       open(str(pathlib.Path.cwd()) +
                            "\\resources\\images\\" +
                            theory.imagePath, 'rb'))
        bot.send_document(message.chat.id,
                          open(str(pathlib.Path.cwd()) +
                               "\\resources\\additionalFiles\\" +
                               theory.filePath, 'rb'),
                               None)
    msg = bot.send_message(message.chat.id,
                           textForSend,
                           parse_mode='html',
                           reply_markup=markup)

    bot.register_next_step_handler(msg, start)

def getPlot(results, path):
    #   Отрисовка графика
    plt.figure(figsize=(12, 7))
    #   Отрисовка точек
    plt.scatter(results[0], results[1], lw=10)
    plt.plot(results[0], results[1], lw=5)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.xlabel('Дата', fontsize=20, fontweight="bold")
    plt.ylabel('% решенных заданий', fontsize=20, fontweight="bold")
    plt.title('Результаты', fontsize=25, fontweight="bold")
    plt.grid(True)
    # показываем график
    plt.savefig(path, dpi=100)

def correctMessage(text) -> str:
    print("text before correct = ", text)
    text = text.replace("<", "&lt")
    text = text.replace(">", "&gt")
    print("text after correct = ", text)

    # re.sub(r'/_/gi', '\\_', text)
    # re.sub(r'/-/gi', '\\-', text)
    # re.sub(r'/`/gi', '\\`', text)
    # re.sub(r'/</g', '\\<', text)
    # re.sub(r'/>/g', '\\>', text)
    # re.sub(r'/≤/g', '\\≤', text)
    return text

# Запускаем бота
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        time.sleep(15)