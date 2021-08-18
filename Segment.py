class Segment:
    def __init__(self,name,divCount,url) -> None:
        self.__name = name
        self.__divCount = divCount
        self.__url = url
    def getName(self):
        return self.__name
    def getDivCount(self):
        return self.__divCount
    def getUrl(self):
        return self.__url
    