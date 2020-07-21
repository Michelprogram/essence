from requests import get
from zipfile import ZipFile
from bs4 import BeautifulSoup
from json import loads,dump
import time

class Essence:

    def __init__(self,carburant,longitude,latitude):
        self.doc_xml = ""
        self.carburant = carburant
        self.longitude = longitude
        self.latitude = latitude
        self.city = []
        self.code_postal = ""


    def __get_zip(self):
        request = get("https://donnees.roulez-eco.fr/opendata/instantane")
        with open("Essence.zip","wb") as zipfile:
            zipfile.write(request.content)

    def get_xml(self):
        with ZipFile("Essence.zip", mode="r") as zip:
            with zip.open("PrixCarburants_instantane.xml", mode="r") as xml:
                    self.doc_xml = xml.read()

    def get_coordinate(self):

        url = "https://eu1.locationiq.com/v1/reverse.php"

        data = {
            "key":"24c7cdf61bec27",
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
        finally:
            self.code_postal = reponse['address']['postcode']

    """
    def _decorator(function):
        def wrapper(self):
            self.__get_zip()
            self.__get_xml()
            self.__get_coordinate()
            function(self)
        return wrapper
    """

    def check_station_city(self):
        soup = BeautifulSoup(self.doc_xml,("lxml"))
        list_soup = soup.find_all("ville",string=self.city[0])

        if (len(list_soup) == 0):
            self.find_nearby_city()
        else:
            self.find_station()

    def find_nearby_city(self):
        url = "http://api.geonames.org/findNearbyPostalCodesJSON"

        data = {
            "lat":self.longitude,
            "lng":self.latitude,
            "country":"FR",
            "radius":"30",
            "username":"micheljardinier"
        }

        requete = get(url, params=data)
        reponse = loads(requete.text)

        self.city = [placeName["placeName"] for placeName in reponse["postalCodes"] ]


        self.check_station_nearby_city()

    def check_station_nearby_city(self):
        print(self.city)
        for i in range(len(self.city)):
            soup = BeautifulSoup(self.doc_xml,("lxml"))
            print(soup.find_all("ville",string=self.city[i]))

    #@_decorator
    def find_station(self):
        soup = BeautifulSoup(self.doc_xml,("lxml"))
        with open("data.json","w",encoding="utf-8") as json_file:

            for i in range(len(self.city)):
                liste_station = []
                list_soup = soup.find_all("ville",string=self.city[i])


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


t = Essence("Gazole", "47.5433394", "1.0321285")
t.get_xml()
t.get_coordinate()
t.check_station_city()
