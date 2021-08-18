
from typing import Tuple
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep

import logging
from datetime import datetime as dt
from os import getcwd
from Python.Wifi import Wifi
from Python.Segment import Segment

ADSLMARGINCB = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[2]/ndm-selectbox2/div/div[2]/a/div'
VDSLMARGINCB = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[3]/ndm-selectbox2/div/div[2]/a/div'



def printTime():
    """Saat_Dakika_Gün_Ay şeklinde döner"""
    parser = dt.now()
    return parser.strftime("%H_%M_%d_%m")


logging.basicConfig(
    filename=fr"{getcwd()}\Log\log_{printTime()}.txt",
    format="%(asctime)s - %(levelname)s - %(message)s ",
    filemode="w",
    level=logging.DEBUG
)
logger = logging.getLogger()



class Keenetic:
    __isLogin = False

    def __init__(self,driverLoc,chromeProfileLoc,headless = False) -> None:
        self.driverLocation = driverLoc
        self.headless = headless
        self.chromeProfileLoc = chromeProfileLoc

    def openBrowser(self):
        """open chrome"""
        options = ChromeOptions()
        options.add_argument(f"user-data-dir={self.chromeProfileLoc}")
        options.add_argument("--log-level=3")
        options.headless = self.headless
        self.browser = Chrome(executable_path=self.driverLocation,options=options)
        self.browser.set_window_position(0,0)
        self.browser.set_window_size(1024,768)

    def loginPanel(self,username,password):
        """Login gateway panel"""
        self.browser.get('http://192.168.1.1/')
        self.__username = username
        self.__password = password
        sleep(2)
        usernameInput = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div/div/div/section/div[1]/div[1]/div/section[2]/form/div[1]/div/div[3]/div/div[1]/label[1]/input')
        passwordInput = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div/div/div/section/div[1]/div[1]/div/section[2]/form/div[2]/div/div[3]/div/div[1]/label[1]/input')
        usernameInput.send_keys(self.__username)
        passwordInput.send_keys(self.__password)
        sleep(0.1)
        loginButton = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div/div/div/section/div[1]/div[1]/div/section[2]/form/ndm-button/button')
        loginButton.click()
        sleep(2)
        if self.browser.current_url == 'http://192.168.1.1/dashboard':
            self.__isLogin = True

    def getSNRMargin(self) -> tuple():
        """Return vdslMargin, adslMargin as int. Login required."""
        if self.__isLogin:
            self.browser.get('http://192.168.1.1/controlPanel/dsl')
            sleep(3)
            ekHatAyarlariLabel = self.browser.find_element_by_xpath('//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[1]/a/span')
            ekHatAyarlariLabel.click()
            adslMarginCB = self.browser.find_element_by_xpath(ADSLMARGINCB)
            vdslMarginCB = self.browser.find_element_by_xpath(VDSLMARGINCB)
            self.__vdslSNRMargin = int(str(vdslMarginCB.get_attribute('title')).replace("(Varsayılan)","").replace("dB",""))
            self.__adslSNRMargin = int(str(adslMarginCB.get_attribute('title')).replace("(Varsayılan)","").replace("dB",""))
            return (self.__vdslSNRMargin, self.__adslSNRMargin)
        else:
            return (None,None)

    def changeSNRMargin(self,type = 0,value = 8):
        """Change SNR margin. type = 0 for VDSL, 1 for ADSL. value for ADSL -10/+10, for VDSL 0/+30"""
        if self.__isLogin:
            if self.browser.current_url != "http://192.168.1.1/controlPanel/dsl":
                self.browser.get("http://192.168.1.1/controlPanel/dsl")
                sleep(2)
            if type == 0:
                #VDSL
                if value <= 30 and value >= 0:
                    sleep(2)
                    ekhatAyarXPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[1]/a'
                    self.browser.find_element_by_xpath(ekhatAyarXPath).click()
                    sleep(0.1)
                    eskiSNRXPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[3]/ndm-selectbox2/div/div[2]/a/div/span[2]/span'
                    eskiMargin = (self.browser.find_element_by_xpath(eskiSNRXPath).text).replace('(Varsayılan)',"")
                    assagiOkxPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[3]/ndm-selectbox2/div/div[2]/a/i'
                    self.browser.find_element_by_xpath(assagiOkxPath).click()
                    sleep(0.1)
                    dbs = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[3]/ndm-selectbox2/div/div[2]/div/ul')
                    dbs = dbs.find_elements_by_css_selector("li")
                    tiklanacakDbs = None
                    for i in dbs:
                        tiklanacakDbsValue = i.get_attribute('data-ndm-option-value')
                        if tiklanacakDbsValue == str(value):
                            tiklanacakDbs = i
                    tiklanacakDbs.click()
                    self.__pressSave()
                    print(f"VDSL SNR Margin update succesful! Old Snr Margin {eskiMargin}, New Snr Margin {value} dB.")
            else:
                #ADSL
                if value <= 10 and value >= -10:
                    sleep(2)
                    ekhatAyarXPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[1]/a'
                    self.browser.find_element_by_xpath(ekhatAyarXPath).click()
                    eskiSNRXPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[2]/ndm-selectbox2/div/div[2]/a/div/span[2]/span'
                    eskiMargin = (self.browser.find_element_by_xpath(eskiSNRXPath).text).replace('(Varsayılan)',"")
                    sleep(0.1)
                    assagiOkxPath = '//*[@id="cp-main-container"]/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[2]/ndm-selectbox2/div/div[2]/a/i'
                    sleep(0.1)
                    self.browser.find_element_by_xpath(assagiOkxPath).click()
                    dbs = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div/div[2]/div/form/div[4]/ng-include/ndm-details/div/div[2]/fieldset/div[2]/ndm-selectbox2/div/div[2]/div/ul')
                    dbs = dbs.find_elements_by_css_selector("li")
                    tiklanacakDbs = None
                    for i in dbs:
                        tiklanacakDbsValue = i.get_attribute('data-ndm-option-value')
                        if tiklanacakDbsValue == str(value):
                            tiklanacakDbs = i
                    tiklanacakDbs.click()
                    self.__pressSave()
                    print(f"ADSL SNR Margin update succesful! Old Snr Margin {eskiMargin}, New Snr Margin {value} dB.")

    def __getSegment(self):
        if self.__isLogin:
            if self.browser.current_url != "http://192.168.1.1/dashboard":
                self.browser.get('http://192.168.1.1/dashboard')
                sleep(2)
            sleep(2)
            mainMenuAglar = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div')
            mainMenuAglar = mainMenuAglar.find_elements_by_css_selector("div")
            segmentlerBrowser = []
            self.segmentler = []
            for i in mainMenuAglar:
                iClass = i.get_attribute('class')
                if iClass == "d-main__card card_segment ng-scope":
                    segmentlerBrowser.append(i)
            divCount = 2
            for segment in segmentlerBrowser:
                segmentAdi = segment.find_element_by_css_selector("a").find_element_by_css_selector("span").text
                segmentUrl = f"http://192.168.1.1/controlPanel/segments/{segmentAdi}"
                self.segmentler.append(Segment(segmentAdi,divCount,segmentUrl))
                divCount+=1

    def __checkSegmentName(self,segmentAdi):
        control = False
        for i in self.segmentler:
            segmentName = i.getName()
            if segmentName == segmentAdi:
                control = True
        return control

    def getWifiDetail(self,segmentAdi):
        if self.__isLogin:
            self.__getSegment()
            if self.__checkSegmentName(segmentAdi):
                for i in self.segmentler:
                    if segmentAdi == i.getName():
                        mySegment = i
                segmentDiv = mySegment.getDivCount()
                if self.browser.current_url != "http://192.168.1.1/dashboard":
                    self.browser.get("http://192.168.1.1/dashboard")
                    sleep(2)
                sleep(2)
                wifiBant,channel = (self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/span').text).split(",")
                wifiName = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]').text
                checked = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]/input').get_attribute('checked')
                channel = int(channel.replace('Kanal',"").strip())
                if checked == "true":
                    checked = True
                else:
                    checked = False
                self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[2]/div/ndm-button/button').click()
                try:
                    password = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[{segmentDiv}]/span[2]').text
                except:
                    password = None

                self.browser.get(mySegment.getUrl())
                sleep(2)
                korumaYontem = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[2]/div/div[2]/div/div/a/div/span/div').text

                self.browser.find_element_by_xpath('//*[@id="cp-main-container"]/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[4]/a/span').click()
                sleep(2)
                ssidGizle = self.browser.find_element_by_xpath('//*[@id="hideSsid__2"]').get_attribute('value') 
                wps = self.browser.find_element_by_xpath('//*[@id="wps__2"]').get_attribute('value')
                ulke = self.browser.find_element_by_xpath('//*[@id="sb-10"]/a/div/span/div').text
                standart = self.browser.find_element_by_xpath('//*[@id="sb-13"]/a/div/span/div').text
                sinyalGucuSeviyesi = self.browser.find_element_by_xpath('//*[@id="sb-12"]/a/div/span/div').text 
                enUygunKanalSecimi = self.browser.find_element_by_xpath('//*[@id="sb-15"]/a/div/span/div').text
                cb2040 = self.browser.execute_script("console.log(document.getElementById('channelWidth__240').checked)")
                maxIletim = self.browser.find_element_by_xpath('//*[@id="txBurst__2"]').get_attribute('value')
                seciliOlan = "20/40"
                if cb2040 == "false":
                    seciliOlan = '20'
                if wps == "false":
                    wps=False
                else:
                    wps=True
                if ssidGizle =="false":
                    ssidGizle =  False
                else:
                    ssidGizle = True
                if maxIletim == "false":
                    maxIletim = False
                else:
                    maxIletim = True
                self.wifi = Wifi(checked,wifiName,password,channel,wifiBant,segmentAdi,korumaYontem,wps,ulke,standart,sinyalGucuSeviyesi,enUygunKanalSecimi,seciliOlan,maxIletim,ssidGizle,False)
                return self.wifi
            else:
                print("Segment name error")
        else:
            print("login error")
            
    def getWifiBasic(self,segmentAdi):
        if self.__isLogin:
            self.__getSegment()
            if self.__checkSegmentName(segmentAdi):
                for i in self.segmentler:
                    if segmentAdi == i.getName():
                        mySegment = i
                segmentDiv = mySegment.getDivCount()
                if self.browser.current_url != "http://192.168.1.1/dashboard":
                    self.browser.get("http://192.168.1.1/dashboard")
                    sleep(2)
                sleep(2)
                wifiBant,channel = (self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[2]/div[2]/span').text).split(",")
                wifiName = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[2]/div[1]').text
                checked = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[1]/div[1]/div/div[1]/input').get_attribute('checked')
                channel = int(channel.replace('Kanal',"").strip())
                if checked == "true":
                    checked = True
                else:
                    checked = False
                self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[{segmentDiv}]/div[2]/div[1]/div/div/div[2]/div/ndm-button/button').click()
                try:
                    password = self.browser.find_element_by_xpath(f'/html/body/ndm-layout/div/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]/div[2]/div[4]/div[{segmentDiv}]/span[2]').text
                except:
                    password = None
                self.wifi = Wifi(checked,wifiName,password,channel,wifiBant,mySegment,None,None,None,None,None,None,None,None,None,True)
                return self.wifi
            else:
                print("Segment name error")
        else:
            print("login error")

    def changeWifiName(self,segmentAdi,newWifiName):
        aktifWifi = self.getWifiBasic(segmentAdi)
        aktifWifiName = aktifWifi.getWifiName()
        aktifSegment = aktifWifi.getSegment()
        aktifUrl = aktifSegment.getUrl()
        self.browser.get(aktifUrl)
        sleep(2)
        agAdı = self.browser.find_element_by_xpath('//*[@id="cp-main-container"]/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[1]/div/div[2]/label[1]/input')
        agAdı.click()
        for _ in range(len(aktifWifiName)):
            agAdı.send_keys(Keys.BACK_SPACE)
        agAdı.send_keys(newWifiName)
        sleep(0.2)
        self.__pressSave()
        print(f"Succesfull! old wifi name: {aktifWifiName}, new wifi name: {newWifiName}")

    def changeWifiPassword(self,segmentAdi,newPassword):
        aktifWifi = self.getWifiBasic(segmentAdi)
        aktifWifiPass = aktifWifi.getPassword()
        aktifSegment = aktifWifi.getSegment()
        aktifUrl = aktifSegment.getUrl()
        self.browser.get(aktifUrl)
        sleep(2)
        agKorumasi = self.browser.find_element_by_xpath('//*[@id="sb-8"]/a/div/span/div').text
        if agKorumasi == "Güvenlik yok" or agKorumasi == "OWE":
            print("You can't change wifi password, first change network protection.")
            yn = input("Do you want me to do it? (y/Y or n/N): ")
            if yn == "y" or yn == "Y":
                self.changeWifiProtectionLevel(segmentAdi,5)


        else:
            agPassword = self.browser.find_element_by_xpath('//*[@id="cp-main-container"]/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[3]/div/div[2]/label[1]/input')
            agPassword.click()
            for _ in range(len(aktifWifiPass)):
                agPassword.send_keys(Keys.BACK_SPACE)
            agPassword.send_keys(newPassword)
            sleep(0.2)
            self.__pressSave()
            print(f"Succesfull! old wifi password: {aktifWifiPass}, new wifi password: {newPassword}")

    def changeWifiProtectionLevel(self,segmentAdi,protectionLevel):
        """Change wifi proction level, recommended level 5.\n
        0, No security\n1, WEP\n2, WPA-PSK\n3, WPA2-PSK\n4, WPA-PSK + WPA2-PSK\n5, WPA2-PSK + WPA3-PSK\n6, WPA3-PSK\n7, OWE\n"""
        protectionLevelDict = {
            0: "disable",
            1: "wep",
            2: "wpa",
            3: "wpa2",
            4: "wpa+wpa2",
            5: "wpa2+wpa3",
            6: "wpa3",
            7: "owe"
        }
        Front = {
            0: "No security",
            1: "WEP",
            2: "WPA-PSK",
            3: "WPA2-PSK",
            4: "WPA-PSK + WPA2-PSK",
            5: "WPA2-PSK + WPA3-PSK",
            6: "WPA3-PSK",
            7: "OWE"
        }
        aktifWifi = self.getWifiBasic(segmentAdi)
        aktifSegment = aktifWifi.getSegment()
        aktifUrl = aktifSegment.getUrl()
        self.browser.get(aktifUrl)
        sleep(3)
        protectionSide = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[2]/div/div[2]/div/div/a')
        oldProtectionLevel = protectionSide.text
        protectionSide.click()
        protectionLi = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[2]/div/div[2]/div/div/ul').find_elements_by_css_selector("li")
        tiklanacakObjke = None
        for i in protectionLi:
            protectionLevelBrowser = i.get_attribute('data-ndm-option-value')
            if protectionLevelBrowser == protectionLevelDict[protectionLevel]:
                tiklanacakObjke = i
        tiklanacakObjke.click()
        if (oldProtectionLevel == 'Güvenlik yok' or oldProtectionLevel == 'OWE' or oldProtectionLevel == 'WEP' ) and (Front[protectionLevel] != "WEP" or Front[protectionLevel] != "OWE" or Front[protectionLevel] != "Güvenlik yok"):
            passSide = self.browser.find_element_by_xpath('/html/body/ndm-layout/div/div[2]/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/form/fieldset/div[2]/div/div[2]/div[3]/fieldset/div[3]/div/div[2]/label[1]/input')
            passSide.click()
            wifiPass = input("New password for new security level: ")
            passSide.send_keys(wifiPass)
            self.__pressSave()
            print(f"Succesfull! old wifi protection level: {oldProtectionLevel}, new protection level: {Front[protectionLevel]}")
        elif (oldProtectionLevel != 'Güvenlik yok' or oldProtectionLevel != 'OWE'  or oldProtectionLevel != 'WEP') and Front[protectionLevel] != "WEP":
            self.__pressSave()
            print(f"Succesfull! old wifi protection level: {oldProtectionLevel}, new protection level: {Front[protectionLevel]}")
        elif (oldProtectionLevel == 'Güvenlik yok' or oldProtectionLevel == 'OWE' or oldProtectionLevel == 'WEP') and (Front[protectionLevel] == "OWE" or Front[protectionLevel] == "Güvenlik yok"):
            self.__pressSave()
            print(f"Succesfull! old wifi protection level: {oldProtectionLevel}, new protection level: {Front[protectionLevel]}")
        else:
            print("Şimdilik bunu yapamıyorum")
        
    def __pressSave(self):
        self.__clickXY(84,586)


    def __clickXY(self,x,y):
        action = ActionChains(self.browser)
        action.move_by_offset(x,y)
        action.click()
        action.perform()
        action.reset_actions()
