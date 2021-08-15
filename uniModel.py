class uniModel:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.city = ''
        self.rank = 0
        self.uniar_score = 0
        self.points = 0
        self.article_count = 0
        self.project_count = 0
        self.book_count = 0
        self.studied_abroad = 0
        self.scientist_count = 0
        self.space_differrence = 0
        self.space = 0
        self.important_notes = ''
        self._public_overall_score = 0
        self._public_academic_ratio = 0
        self._factor_dict = {
            "article_count": 5,
            "book_count": 10,
            "project_count": 10
        }

    def fromJson(self, dict):
        varNames = [k for k in self.__dict__.keys() if not k.startswith("_")]
        for varName in varNames:
            if varName in dict.keys():
                self.__dict__[varName] = dict[varName]
        self.calculateScore()

    def searchMissing(self, dict):
        varNames = [k for k in self.__dict__.keys() if not k.startswith("_")]
        hasMissing = False
        for varName in varNames:
            if varName not in dict.keys():
                self.show()
                print('Missing value found for above record please fill:')
                self.__dict__[varName] = self._input(varName)
                hasMissing = True
        return hasMissing

    def toJson(self):
        dictMem = self.__dict__
        varNames = dictMem.keys()
        return {varName: dictMem[varName] for varName in varNames if not varName.startswith("_")}

    def show(self):
        rd = self.readableDict()
        for k in rd.keys():
            print(k + ':', rd[k])
        print('=' * 10)

    def readableDict(self):
        dictMem = self.__dict__
        varNames = self.__dict__.keys()
        dict = {}
        for varName in varNames:
            if not varName.startswith("_"):
                dict[varName.replace('_', ' ')] = dictMem[varName]
            elif "public" in varName:
                dict[varName.replace('_', ' ').replace(
                    "public", "")] = dictMem[varName]
        return dict

    def onlyLetterDict(self):
        dictMem = self.__dict__
        varNames = self.__dict__.keys()
        dict = {}
        for varName in varNames:
            if not varName.startswith("_"):
                dict[varName.replace('_', '')] = varName
            elif "public" in varName:
                dict[varName.replace('_', '').replace(
                    "public", "")] = varName
        return dict

    def inputFromUser(self):
        varNames = [k for k in self.__dict__.keys() if not k.startswith("_")]
        for varName in varNames:
            self.__dict__[varName] = self._input(varName)

    def _input(self, varName):
        var = self.__dict__[varName]
        if type(var) is int:
            return int(input(varName + ':'))
        elif type(var) is str:
            return input(varName + ':')

    # Custom functions section

    # @section
    def calculateScore(self):
        score = 0
        for factorName in self._factor_dict.keys():
            score += self.__dict__[
                factorName] * self._factor_dict[factorName]
        score += self.uniar_score
        self._public_overall_score = score
        self._public_academic_ratio = score / self.scientist_count
        # @endesction
