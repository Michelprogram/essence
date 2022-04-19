from requests import get
from zipfile import ZipFile
from bs4 import BeautifulSoup
from json import loads,dump
import time
from geopy import distance


class Essence:

    def __init__(self,carburant,longitude,latitude):
        self.doc_xml = ""
        self.carburant = carburant
        self.longitude = longitude
        self.latitude = latitude
        self.city = []

    def _decorator(function):
        def wrapper(self):
            self.__get_zip()
            self.__get_xml()
            self.__get_coordinate()
            self.__check_station()
            function(self)
        return wrapper

    def __get_zip(self):
        request = get("https://donnees.roulez-eco.fr/opendata/instantane")
        with open("Essence.zip","wb") as zipfile:
            zipfile.write(request.content)

    def __get_xml(self):
        with ZipFile("Essence.zip", mode="r") as zip:
            with zip.open("PrixCarburants_instantane.xml", mode="r") as xml:
                    self.soup_xml = BeautifulSoup(xml.read(),("lxml"))

    def __get_coordinate(self):

        url = "https://eu1.locationiq.com/v1/reverse.php"

        data = {
            "key":"/",
            "lat":self.longitude,
            "lon":self.latitude,
            "format":"json"
        }

        requete = get(url, params=data)
        reponse = loads(requete.text)

        try:
            self.city.append(reponse['address']['city'])
        except KeyError:
            try:
                self.city.append(reponse['address']['town'])
            except KeyError:
                self.city.append(reponse['address']['village'])

    def __check_station(self):
        if ( len(self.soup_xml.find_all("ville",string=self.city[0])) == 0) : self.__city_in_area()

    def __city_in_area(self):

        pdv = self.soup_xml.find_all("ville")
        flag = False
        area_km = 15

        while flag != True:

            for ville in pdv:
                latitude = float(ville.parent["latitude"])/100000
                longitude = float(ville.parent["longitude"])/100000

                if (self.__check_area(longitude,latitude,area_km)):
                    self.city.append(ville.get_text())
                    flag = True

            area_km += 5
            print(area_km)

        del self.city[0]

    def __check_area(self,longitude,latitude,compteur_distance):
        distance_between_point = distance.distance((self.longitude,self.latitude),(latitude,longitude)).km
        return True if (distance_between_point <= compteur_distance) else False

    @_decorator
    def find_station(self):
        with open("data.json","w",encoding="utf-8") as json_file:
            liste_station = []
            for i in range(len(self.city)):

                list_soup = self.soup_xml.find_all("ville",string=self.city[i])


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
