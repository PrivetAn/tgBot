class Theory:
    def __init__(self, type = -1,  textTheory = "", imagePath = "", filePath = ""):
        if(imagePath == None) : imagePath = ""
        if(filePath == None) : filePath = ""

        self.textTheory = textTheory
        self.type = type
        self.imagePath = imagePath
        self.filePath = filePath

    textTheory = ""
    type = -1
    imagePath = ""
    filePath = ""