from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import typing
import sys
import json

VIEW_URL = "zaklad_8.qml"   # Advanced user interface
CITY_LIST_FILE = "cities_sort.geojson"

def choose_district(index):
    districts = [["Praha"],[ "České Budějovice",                            "Český Krumlov",                            "Jindřichův Hradec",                            "Písek",                            "Prachatice",                            "Strakonice",                            "Tábor"],        [ "Blansko",                                "Brno-město",                                "Brno-venkov",                                "Břeclav",                                "Hodonín",                                "Vyškov",                                "Znojmo"],[ "Cheb",                            "Karlovy Vary",                            "Sokolov"],[ "Havlíčkův Brod",                            "Jihlava",                            "Pelhřimov",                            "Třebíč",                            "Žďár nad Sázavou"],[ "Hradec Králové",                                "Jičín",                                "Náchod",                                "Rychnov nad Kněžnou",                                "Trutnov"],[ "Česká Lípa",                        "Jablonec nad Nisou",                        "Liberec",                        "Semily"],[ "Bruntál",                                "Frýdek-Místek",                                "Karviná",                                "Nový Jičín",                                "Opava",                                "Ostrava-město"],[ "Jeseník",                        "Olomouc",                        "Prostějov",                        "Přerov",                        "Šumperk"],[ "Chrudim",                            "Pardubice",                            "Svitavy",                            "Ústí nad Orlicí"],[ "Domažlice",                        "Klatovy",                        "Plzeň-jih",                        "Plzeň-město",                        "Plzeň-sever",                        "Rokycany",                        "Tachov"],[ "Benešov",                            "Beroun",                            "Kladno",                            "Kolín",                            "Kutná Hora",                            "Mělník",                            "Mladá Boleslav",                            "Nymburk",                            "Praha-východ",                            "Praha-západ",                            "Příbram",                            "Rakovník"],[ "Děčín",                        "Chomutov",                        "Litoměřice",                        "Louny",                        "Most",                        "Teplice",                        "Ústí nad Labem"],[ "Kroměříž",                        "Uherské Hradiště",                        "Vsetín",                        "Zlín"]]
    if int(index) == 0:
        merged = []
        for i in range(0,14):
                merged = merged + districts[i]
        merged.sort()
        merged.append("VŠE")
        return merged
    
    di = districts[int(index)-1]
    a = ['VŠE']
    dist = a + di
    return dist


class Filter(QObject):

    def __init__(self): # inicializace 
        QObject.__init__(self)
        self._city = True # private attributes
        self._village = True

        self._population_min = 0
        self._population_max  = 1270000

        self._area = "Zlínský kraj"
        self._districts = ["VŠE", "Kroměříž", "Uherské Hradiště", "Vsetín", "Zlín"]
        self._district = "Zlín"

    def set_city(self, new_val):
        if new_val != self._city:
            self._city = new_val
            self.city_changed.emit(self._city)
            print("Filter cities:", self._city) # print state to terminal

    def set_village(self, new_val):
        if new_val != self._village:
            self._village = new_val
            self.village_changed.emit(self._village)
            print("Filter villages:", self._village) # print state to terminal
    
    def set_population_min(self, new_val):
        if new_val != self._population_min:
            self._population_min = new_val
            self.population_min_changed.emit(self._population_min)
            print("Filter population min:", self._population_min) # print state to terminal

    def set_population_max(self, new_val):
        if new_val != self._population_max:
            self._population_max = new_val
            self.population_max_changed.emit(self._population_max)
            print("Filter population max:", self._population_max) # print state to terminal

    def set_area(self, new_val):
        if new_val != self._area:
            self._area = new_val
            self.area_changed.emit(self._area)
            print("Filter area:", self._area) # print state to terminal
            # set districts from choosen area, this strange way is choosen because of bug in comboboxes: https://forum.qt.io/topic/116304/example-of-a-model-for-use-with-qtquick-combobox-qml
            self.set_districts(choose_district(self.area))

    def set_districts(self, new_val):
        if new_val != self._districts:
            self._districts = new_val
            #self.district_changed.emit(self._districts)
            print("Filter districts:", self._districts) # print state to terminal
            ctxt.setContextProperty("dist", self._districts)

    def set_district(self, new_val):
        if new_val != self._district:
            self._district = new_val
            self.district_changed.emit(self._district)
            print("Filter final district:", self._district) # print state to terminal

    def get_city(self):
        return self._city

    def get_district(self):
        return self._districts

    def filterCities(self,city):
        # filtering cities/villages
        if self._city == True and city["properties"]["mesto"] == 1:
            pass
        elif self._village == True and city["properties"]["mesto"] == 0:
            pass
        else:
            return None

        # filter based on population
        if self.population_min <= city["properties"]["POCET_OBYV"] and self.population_max >= city["properties"]["POCET_OBYV"]:
            pass
        else:
            return None

        # filter based on district
        # more district selected:
        if self._district == "VŠE":
            if city["properties"]["NAZ_LAU1"] in self._districts:
                pass
            else:
                return None
        # one district is selected
        else:  
            if city["properties"]["NAZ_LAU1"] == self._district:
                pass
            else:
                return None
        # m = 10
        # return city, m
        return city
    
    # def zoom_kraje(m):
        # if m = 10
        # return m

    city_changed = Signal(bool)
    village_changed = Signal(bool)
    population_min_changed = Signal(int)
    population_max_changed = Signal(int)
    area_changed = Signal(str)
    district_changed = Signal(str)

    city = Property(bool, get_city, set_city, notify=city_changed)
    village = Property(bool, lambda self: self._village, set_village, notify=village_changed)
    population_min = Property(int, lambda self: self._population_min, set_population_min, notify=population_min_changed)
    population_max = Property(int, lambda self: self._population_max, set_population_max, notify=population_max_changed)
    area = Property(str, lambda self: self._area, set_area, notify=area_changed)
    district = Property(str, get_district, set_district, notify=district_changed)

class BrowserCityModel(QAbstractListModel):
        
    class Roles(Enum):
        """Enum with added custom roles"""
        LOCATION = QtCore.Qt.UserRole+0
        AREA = QtCore.Qt.UserRole+1
        POPULATION = QtCore.Qt.UserRole+2
        MESTO = QtCore.Qt.UserRole+3
    
    def __init__(self,filename=None):
        """Initialize and load list from given file"""
        QAbstractListModel.__init__(self)
        self.browser_city = [] # list with cities for showing in map
        if filename:
            self.load_from_json(filename)

    def load_from_json(self,filename):
        """Load list of cities from given file"""
        with open(filename,encoding="utf-8") as f:
            self.browser_city = json.load(f)
            self.browser_city = self.browser_city['features']
            # Create QGeoCoordinate from the original JSON location
            for c in self.browser_city:
                cor = c['geometry']['coordinates']
                lon, lat = cor[0], cor[1] # Get the part between brackets and split it on space
                c['geometry']['coordinates'] = QGeoCoordinate(float(lat),float(lon)) # Create QGeoCoordinate and overwrite original `location` entry
            self.full_city_list = self.browser_city[:] # full_city_list --> list, which stores all cities from input geojson all time, browser_city is for showing in map

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        """ Return number of cities in the list"""
        return len(self.browser_city)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        """ For given index and DisplayRole return name of the selected city"""
        # Return None if the index is not valid
        if not index.isValid():
            return None
        """print("##################################", self.browser_city)
        print(len(self.browser_city))"""
        # If the role is the DisplayRole, return name of the city
        if role == QtCore.Qt.DisplayRole:
            return self.browser_city[index.row()]['properties']['NAZ_OBEC']
        if role == self.Roles.POPULATION.value:
            return self.browser_city[index.row()]['properties']['POCET_OBYV']
        if role == self.Roles.AREA.value:
            r = self.browser_city[index.row()]['properties']['SHAPE_Area']
            r_round = round(r)
            return r_round
        if role == self.Roles.LOCATION.value:
            return self.browser_city[index.row()]['geometry']['coordinates']
        if role == self.Roles.MESTO.value:
            return self.browser_city[index.row()]['properties']['mesto']
            
    
    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.POPULATION.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        roles[self.Roles.MESTO.value] = QByteArray(b'mesto')
        return roles

    @Slot()
    def modifyList(self):       
        tmplist = [] # just temporary list for filtering
        # filtering starts now:
        for i in self.full_city_list:
            city_filter = self.filter.filterCities(i)
            if city_filter == None:
                pass
            else:
                tmplist.append(city_filter)
        # delete all rows from current browser_city list
        self.beginRemoveRows(self.index(0).parent(),0, len(self.browser_city)-1)
        self.browser_city = []
        self.endRemoveRows()
        # add filtered cities to borwser_city list
        self.beginInsertRows(self.index(0).parent(),0,len(tmplist)-1)
        self.browser_city = tmplist[:]
        self.endInsertRows()
        print("cities/villages count: ", len(self.browser_city))
        print("################# list modified #####################")

    filter = Filter()

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
browsercity_model = BrowserCityModel(CITY_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('browserCityModel',browsercity_model)
ctxt.setContextProperty("filt", browsercity_model.filter)

view.setSource(url)
view.show()
app.exec_()
