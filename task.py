class Question:
    def __init__(self, textQuestion = "", answers = [], key = "", imagePath = "", filePath = ""):
        self.textQuestion = textQuestion
        self.answers = answers
        self.key = key
        self.imagePath = imagePath
        self.filePath = filePath

    textQuestion = ""
    answers = []
    key = ""
    usersAnswer = ""
    imagePath = ""
    filePath = ""

class Test:
    def __init__(self, questions=[]):
        self.questions = questions

    def appebdQuestion(self, question):
        self.questions.append(question)

    def calculateResultTest(self) :
        print("TEST::calculateResultTest")
        score = 0
        for q in self.questions :
            print(q.usersAnswer)
            # index = [ans.strip().lower() for ans in q.answers].index(q.usersAnswer.strip().lower())
            if q.usersAnswer.strip().lower() == q.key.strip().lower(): score = score + 1
        return [score, round(score / len(self.questions) * 100, 2)]

    questions = []


