from requests_html import HTMLSession
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import threading
from datetime import datetime

class Dollar:
    def __init__(self, dollar=0):
        self._dollar = dollar

    # getter method
    def get_dollar(self):
        return self._dollar

    # setter method
    def set_dollar(self, x):
        self._dollar = x
dollarObject=Dollar()


# Authenticate
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)
#get input from user
rawtitle = str(input("Başlığı yazınız. Değişecek yere # koyunuz. Örnek: Bu araba sadece # tl: "))
DollarValueOfVideo = float(input("# yerine gelecek değeri dolar cinsinden yazınız:"))
print("")
print("Örnek video url: \"youtube.com/watch?v=XO2fhnG61\"")
print("Bu videonun ID'si: XO2fhnG61")
IDvideo = str(input("Lütfen kendi videonuzun ID'sini giriniz:"))


def calculateDollar(dollarEnteredByUser,newDollarFromWeb):
    currentValue=dollarEnteredByUser*newDollarFromWeb
    return currentValue

def updateDollar(): #bu fonksiyon 1 saatte bir çağırılıp dolar kurunun değişip değişmediğine bakacak. değiştiyse changeVideoTitle çağırılacak.
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    s = HTMLSession()
    url = 'https://www.google.com/search?q=dolar+ne+kadar'
    r = s.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'})
    temp = r.html.find('div.dDoNo.ikb4Bb.gsrt span.DFlfde.SwHCTb', first=True).text
    newDollarStr = temp.replace(",", ".")
    print("")
    print("Dolar değeri kontrol edildi saat şu anda = ", current_time)
    updatedValueOfVideo = calculateDollar(DollarValueOfVideo, float(newDollarStr))
    if(updatedValueOfVideo!=dollarObject.get_dollar()):

        print("Dolar şu anda: " + str(newDollarStr))
        dollarObject.set_dollar(updatedValueOfVideo)  #set the current dollar value
        newtitle = rawtitle.replace("#", str(dollarObject.get_dollar()))
        changeVideoTitle(IDvideo, newtitle,youtube)
        print("")
        print("Videonuzun başlığı başarıyla güncellendi")

    threading.Timer(300.0, updateDollar).start()
    print(updatedValueOfVideo)
    return updatedValueOfVideo

def changeVideoTitle(id,title,youtube):
    request = youtube.videos().update(
        part="snippet",  # ,status
        body={
            "id": id,
            "snippet": {
                "categoryId": 27,
                # "defaultLanguage": "en",
                "title": title
            },
        }
    )
    response = request.execute()
    print(response)

updateDollar()






