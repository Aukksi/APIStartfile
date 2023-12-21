import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import subprocess


app = Flask(__name__)

def SivuGetti(osoite, *args):
    sivu=requests.get(osoite, verify=False)
    contents = sivu.text
    soup = BeautifulSoup(contents, "html.parser")
    lista=soup.find_all(args[0], class_= args[1])
    return lista

def Tulostus(lista, ravintolan_nimi, alku, loppu):
    printOn=False
    sisalto=lista[0].text.strip()
    sisaltotaulu=sisalto.split("\n")
    return sisaltotaulu


@app.route('/')
def index():
   #print('Moro')
  lista=SivuGetti("https://ravintolafactory.com/lounasravintolat/ravintolat/factory-hameentie/", "div", "list" )
  screippi=Tulostus(lista, "Factory", "Maanantai", "Monday")
  print(screippi)

#@app.route('/hello', methods=['GET'])
#def hello():
#  os.system(f'python {/paivansoppa.py}')

if __name__ == '__main__':
   app.run()

