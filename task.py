class Question:
    def __init__(self, textQuestion = "", answers = [], key = -1, imagePath = "", filePath = ""):
        self.textQuestion = textQuestion
        self.answers = answers
        self.key = key
        self.imagePath = imagePath
        self.filePath = filePath

    textQuestion = ""
    answers = []
    key = -1
    imagePath = ""
    filePath = ""

class Test:
    def __init__(self, questions=[]):
        self.questions = questions

    questions = []

