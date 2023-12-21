""" Paivansoppa.py webscraping scripti
    Päivän menut lähiravintoloista
    -Anssi Henell"""


from bs4 import BeautifulSoup
import requests
from datetime import datetime
import subprocess


PAIVAT = ["maanantai", "tiistai", "keskiviikko",
        "torstai", "perjantai", "lauantai", "sunnuntai"]

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

osCommandString = "notepad.exe PäivänSafkat.txt"

TamanPaivanSafkat=[]

#Scrapee sivun sisällön netistä BeautifulSoupilla
def SivuGetti(osoite, *args):
    sivu=requests.get(osoite, verify=False)
    contents = sivu.text
    soup = BeautifulSoup(contents, "html.parser")
    lista=soup.find_all(args[0], class_= args[1])
    return lista

#"Raakatulostus" jokaisen ravintolan viikon menu omiin txt-tiedostoihin
def Tulostus(lista, ravintolan_nimi, alku, loppu):
    filu = open(f"C:\\Users\\03030131\\Work Folders\\{ravintolan_nimi}.txt", "w")
    printOn=False
    sisalto=lista[0].text.strip()
    sisaltotaulu=sisalto.split("\n")
    for rivi in sisaltotaulu:
        if alku in rivi:
            printOn=True
        
        if loppu in rivi:
            filu.write("---------------------------------------------------------------")
            printOn=False

        if printOn==True:
            rivi.strip()
            filu.write(f"{rivi}\n")

    filu.close()

#Viikonpäivät, tarvitaan tämän päivän menujen hakemisessa
def mikaPaiva():
    now=datetime.now().weekday()
    viikonpaiva=PAIVAT[now]
    huominen=PAIVAT[now+1]
    weekday=DAYS[now]
    tomorrow=DAYS[now+1]
    return viikonpaiva, weekday, huominen, tomorrow



#Avaa ravintolan koko viikon tiedoston, siistii siitä paljon turhaa tauhkaa pois ja lisää tämän päivän menusisällön TamanPaivanSafkat-listaan
def SiistimisScripu(ravintolan_nimi):
    siistittyFilu=[]
    LisaaTamanPaivanSafkoin=False
    TamanPaivanSafkat.append(f"\n{ravintolan_nimi.upper()}")
    with open(f"C:\\Users\\03030131\\Work Folders\\{ravintolan_nimi}.txt", "r") as data:
        Filu=data.read()
        siistittavaFilu=Filu.splitlines()

    for entry in siistittavaFilu:
       if (len(entry))!=0:
           siisti=str(entry.strip())          
           siistittyFilu.append(siisti)
    
    for rivi in siistittyFilu:
        if viikonpaiva in rivi or viikonpaiva.capitalize() in rivi:
            LisaaTamanPaivanSafkoin=True
        elif weekday in rivi or weekday.capitalize() in rivi:
            LisaaTamanPaivanSafkoin=True
        elif huominen in rivi or huominen.capitalize() in rivi:
            LisaaTamanPaivanSafkoin=False
        elif tomorrow in rivi or tomorrow.capitalize() in rivi:
            LisaaTamanPaivanSafkoin=False
        
        if LisaaTamanPaivanSafkoin==True:
            TamanPaivanSafkat.append(rivi)


            


#------------------TÄMÄ ON FACTORYN LOUNASLISTALLE-----------------------#
lista=SivuGetti("https://ravintolafactory.com/lounasravintolat/ravintolat/factory-hameentie/", "div", "list" )
Tulostus(lista, "Factory", "Maanantai", "Monday")

#-----------------------------TÄMÄ ON ONDAN LOUNASLISTALLE------------------------#
lista= SivuGetti("https://ravintolaonda.fi/", "div", "card is-radiusless pb-3")
Tulostus(lista, "Onda", "Monday", "Ravintola")

#-----------------------------TÄMÄ ON PIHKAN LOUNASLISTALLE-----------------------#
lista=SivuGetti("https://www.pihka.fi/pihka-lintulahti/", "div", "wp-block-noho-lunch-menus-lunch-week-view alignwide" )
Tulostus(lista, "Pihka", "maanantai", "Pihkan")
viikonpaiva, weekday, huominen, tomorrow=mikaPaiva()

SiistimisScripu("Factory")
SiistimisScripu("Pihka")
SiistimisScripu("Onda")

#Kirjoitetaan PäivänSafkat.txt -tiedostoon jokaisen raflan päivän ruoat
with open(f"C:\\Users\\03030131\\Work Folders\\PäivänSafkat.txt", "w") as paivanSafkat:
    for line in TamanPaivanSafkat:
        paivanSafkat.write(f"{line}\n")


#Tämä avaa PäivänSafkat.txt -tiedoston notepadillä. Kommentoi pois, jos et halua avata
subprocess.run([r"notepad.exe",r"C:\Users\03030131\Work Folders\PäivänSafkat.txt"])


#Tämä printtaa PäivänSafkat.txt -sisällön konsolitulosteena. Kommentit pois, jos haluat käyttäää
#with open(f"C:\\Users\\03030131\\Work Folders\\PäivänSafkat.txt", "r") as paivanSafkat:
#    file=paivanSafkat.read()
#    print(file)
