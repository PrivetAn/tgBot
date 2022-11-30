import sqlite3
import pathlib


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


readTestFromDB("Animals")
readTestFromDB("IngenuityTest")
