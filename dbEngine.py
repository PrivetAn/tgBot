import sqlite3
import pathlib
import task


def readTestFromDB(testName):
    print("testName = ", testName)
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * from questions WHERE variant= ?", (testName,))
    records = cursor.fetchall()
    print("records = ", records)

    generatedTest = task.Test()
    generatedTest.clearQuestions()
    for tableQuestion in records :
        generatedTest.appendQuestion(task.Question(tableQuestion[ 2 ] if tableQuestion[ 2 ] else -1,
                                                   tableQuestion[ 3 ].replace("\\n", "\n"),
                                                   tableQuestion[ 4 ].split(';') if tableQuestion[ 4 ] else "",
                                                   tableQuestion[ 5 ],
                                                   tableQuestion[ 6 ],
                                                   tableQuestion[ 7 ]))

    return generatedTest

def addUserToDB(user_id = -1, user_name = ""):
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT user_id from users")
    for ids in cursor.fetchall():
        if user_id in ids:
            return

    cursor.execute('INSERT INTO users (user_id, user_name) VALUES (?, ?)', (user_id, user_name))
    connect.commit()
    print("Пользователь добавлен")

def addUserResultToDB(user_id=-1, result=-1):
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    # cursor.execute("SELECT user_id from statistic")

    cursor.execute('INSERT INTO statistic (user_id, result) VALUES (?, ?)', (user_id, result))
    connect.commit()
    print("Результат записан")


def getUserResultFromDB(user_id=-1):
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    results = []
    cursor.execute("SELECT * from statistic WHERE user_id= ?", (user_id,))
    for entry in cursor.fetchall():
        print("entry = ", entry)
        results.append([entry[ 2 ], entry[ 3 ]])
    return results





# readTestFromDB("variant_1")
# addUserToDB(12321414,"test")
