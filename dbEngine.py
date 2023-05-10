import sqlite3
import pathlib
import task
import theory


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

def readTaskFromDB(taskNumber):
    print("testName = ", taskNumber)
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * from questions WHERE type_task= ?", (taskNumber,))
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

def readTheoryFromDB(taskNumber):
    print("testName = ", taskNumber)
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * from theory WHERE type_task= ?", (taskNumber,))
    records = cursor.fetchall()
    print("records = ", records)

    requiredTheory = records[ 0 ]

    return theory.Theory(requiredTheory[ 1 ] if requiredTheory[ 1 ] else -1,
                         requiredTheory[ 2 ].replace("\\n", "\n"),
                         requiredTheory[ 3 ],
                         requiredTheory[ 4 ])

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

    results = [[],[]]
    cursor.execute("SELECT * from statistic WHERE user_id= ?", (user_id,))
    for entry in cursor.fetchall():
        results[ 0 ].append(entry[ 2 ].split()[ 0 ])
        results[ 1 ].append(entry[ 3 ])
    print("results = ", results)
    return results
