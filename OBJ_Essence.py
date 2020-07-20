from requests import get
from zipfile import ZipFile
from bs4 import BeautifulSoup
from json import loads,dump
import time

class Essence:

    def __init__(self,carburant,longitude,latitude):
        self.doc_xml = ""
        self.longitude = longitude
        self.latitude = latitude
        self.city = ""
        self.carburant = carburant

    def __get_zip(self):
        request = get("https://donnees.roulez-eco.fr/opendata/instantane")
        with open("Essence.zip","wb") as zipfile:
            zipfile.write(request.content)

    def __get_xml(self):
        with ZipFile("Essence.zip", mode="r") as zip:
            with zip.open("PrixCarburants_instantane.xml", mode="r") as xml:
                    self.doc_xml = xml.read()


    def __get_coordinate(self):

        url = "https://eu1.locationiq.com/v1/reverse.php"

        data = {
            "key":"24c7cdf61bec27",
            "lat":self.longitude,
            "lon":self.latitude,
            "format":"json"
        }

        requete = get(url, params=data)
        try:
            self.city = reponse['address']['city']
        except KeyError:
            try:
                self.city = reponse['address']['town']
            except KeyError:
                self.city = reponse['address']['village']
        print(self.city)


    def _decorator(function):
        def wrapper(self):
            self.__get_zip()
            #self.__get_xml()
            self.__get_coordinate()
            function(self)
        return wrapper

    @_decorator
    def find_station(self):
        soup = BeautifulSoup(self.doc_xml,("lxml"))
        list_soup = soup.find_all("ville",string=self.city)

        with open("data.json","w",encoding="utf-8") as json_file:
            liste_station = []
            for ville in range(len(list_soup)):
                details_station = {}
                pdv = list_soup[ville].parent

                liste_gasoil = pdv.find_all("prix")

                if len([prix for prix in liste_gasoil if prix["nom"]==self.carburant]) >= 1:

                    details_station["id"] = pdv["id"]
                    details_station["latitude"] = float(pdv["latitude"])/100000
                    details_station["longitude"] = float(pdv["longitude"])/100000
                    details_station["ville"] = pdv.find("ville").get_text()
                    details_station["adresse"] = pdv.find("adresse").get_text()


                    liste_value = [valeur["valeur"] for valeur in liste_gasoil ]
                    liste_gasoil = [nom["nom"] for nom in liste_gasoil]
                    gasoil_dict = {liste_gasoil[i]:float(liste_value[i]) for i in range(len(liste_value))}

                    details_station["gasoil"] = gasoil_dict

                    liste_station.append(details_station)

            liste_station = sorted(liste_station,key=lambda station:station["gasoil"][self.carburant])
            dump(liste_station,json_file,indent=2)
