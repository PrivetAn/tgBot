import sqlite3
import pathlib
import task


def readTestFromDB(testName):
    print("testName = ", testName)
    connect = sqlite3.connect(str(pathlib.Path.cwd()) + "\\resources\\db\\tests.db")
    cursor = connect.cursor()
    print("Подключен к SQLite")

    cursor.execute("SELECT * from questions WHERE name= ?", (testName,))
    records = cursor.fetchall()

    generatedTest = task.Test()
    generatedTest.clearQuestions()
    for tableQuestion in records :
        generatedTest.appendQuestion(task.Question(tableQuestion[ 2 ],
                                          tableQuestion[ 3 ].split(';'),
                                          tableQuestion[ 4 ],
                                          tableQuestion[ 5 ],
                                          tableQuestion[ 6 ]))
    return generatedTest

# readTestFromDB("Animals")
