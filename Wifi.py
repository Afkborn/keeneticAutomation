from Python.Segment import Segment


class Wifi:
    def __init__(self,isOnline,wifiName,password,channel,wifiBant,segment,korumaYontem,wps,ulke,standart,sinyalGucuSeviyesi,enUygunKanalSecimi,bantGenisligi,maxIletim,ssidgizle,isBasic) -> None:
        self.__isBasic = isBasic
        self.__isOnline = isOnline
        self.__wifiName = wifiName
        self.__password = password
        self.__channel = channel
        self.__wifiBant = wifiBant
        self.__segment = segment
        self.__korumaYontem = korumaYontem
        self.__wps=wps
        self.__ulke = ulke
        self.__standart=standart
        self.__sinyalGucuSeviyesi = sinyalGucuSeviyesi
        self.__enUygunKanalSecimi = enUygunKanalSecimi
        self.__bantGenisligi = bantGenisligi
        self.__maxIletim=maxIletim
        self.__ssidgizle = ssidgizle
    def getIsOnline(self) -> bool:
        return self.__isOnline
    def getWifiName(self) -> str:
        return self.__wifiName
    def getPassword(self) -> str:
        return self.__password
    def getChannel(self) -> int:
        return self.__channel
    def getWifiBant(self) -> str:
        return self.__wifiBant
    def getSegment(self) -> Segment:
        return self.__segment
    def getKorumaYontem(self) -> str:
        return self.__korumaYontem
    def getWPS(self) -> bool:
        return self.__wps
    def getUlke(self) ->str:
        return self.__ulke
    def getStandart(self) -> str:
        return self.__standart
    def getSinyalGucuSeviyesi(self) -> str:
        return self.__sinyalGucuSeviyesi
    def getEnUygunKanalSecimi(self) -> str:
        return self.__enUygunKanalSecimi
    def getBantGenisligi(self) -> str:
        return self.__bantGenisligi
    def getMaxIletim(self) -> bool:
        return self.__maxIletim
    def getSSIDGizle(self) -> bool:
        return self.__ssidgizle
    def printDetail(self):
        if self.__isBasic:
            detailMessage = f"Online: {self.__isOnline}\nName: {self.__wifiName}\nPassword: {self.__password}\nChannel: {self.__channel}\nWifi Bant: {self.__wifiBant}\nSegment Name: {self.__segmentAdi}\n"
        else:
            detailMessage = f"""Online: {self.__isOnline}\nName: {self.__wifiName}\nPassword: {self.__password}\nChannel: {self.__channel}\nWifi Bant: {self.__wifiBant}\nSegment Name: {self.__segmentAdi}\nProtection Level: {self.__korumaYontem}\nWPS: {self.__wps}\nCountry: {self.__ulke}\nStandart: {self.__standart}\nSignal Rate: {self.__sinyalGucuSeviyesi}\nChannel Selection: {self.__enUygunKanalSecimi}\nBandwidth: {self.__bantGenisligi}\nMax Transmission: {self.__maxIletim}\nHide SSID: {self.__ssidgizle}"""
        print(detailMessage)
    
  
