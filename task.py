class Question:
    def __init__(self, type = -1,  textQuestion = "", answers = [],key = "", imagePath = "", filePath = ""):
        if(imagePath == None) : imagePath = ""
        if(filePath == None) : filePath = ""

        self.textQuestion = textQuestion
        self.answers = answers
        self.type = type
        self.key = key
        self.imagePath = imagePath
        self.filePath = filePath

    textQuestion = ""
    answers = []
    type = -1
    key = ""
    usersAnswer = ""
    imagePath = ""
    filePath = ""

class Test:
    def __init__(self, questions=[]):
        self.questions = questions

    def appendQuestion(self, question):
        self.questions.append(question)

    def clearQuestions(self):
        self.questions.clear()

    def calculateResultTest(self) :
        print("TEST::calculateResultTest")
        score = 0
        for q in self.questions :
            print(q.usersAnswer)
            if q.usersAnswer.strip().lower() == q.key.strip().lower(): score = score + 1
        return [score, round(score / len(self.questions) * 100, 2)]

    def calculateResultTrainingTest(self) :
        print("TEST::calculateResultTrainingTest")
        number = 1
        userAnswers = ""
        for q in self.questions :
            print(q.usersAnswer)
            userAnswers += str(number) + ") - "
            userAnswers += "правильно" if q.usersAnswer.strip().lower() == q.key.strip().lower() else "не правильно"
            userAnswers += '\n'
            number += 1

        print("resultStr = ", userAnswers)
        return userAnswers

    questions = []


