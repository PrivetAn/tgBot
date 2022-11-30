import sqlite3
import pathlib
import task


def readTestFromDB(testName):
    print("testName = ", testName)
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    paramstyle = sqlite3.paramstyle
    print("paramstyle = ", paramstyle)

    cursor.execute("SELECT * from questions WHERE name= ?", (testName,))

    records = cursor.fetchall()
    print("Всего строк:  ", len(records))
    print("Строки:  ", records)

    test = task.Test()
    for question in records :
        print(question)



readTestFromDB("Animals")
