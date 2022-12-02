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


# readTestFromDB("variant_1")
# addUserToDB(12321414,"test")
