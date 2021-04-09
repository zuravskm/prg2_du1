from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import typing
import sys
import json

VIEW_URL = "Ukol1/view.qml"   # Advanced user interface
CITY_LIST_FILE = "Ukol1/cities.geojson"

   
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
        self.browser_city = []
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

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        """ Return number of cities in the list"""
        return len(self.browser_city)

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        """ For given index and DisplayRole return name of the selected city"""
        # Return None if the index is not valid
        if not index.isValid():
            return None
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
            m = self.browser_city[index.row()]['properties']['mesto']
            res = Filter.filter_obec(m)
            return res
    
    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.POPULATION.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        roles[self.Roles.MESTO.value] = QByteArray(b'mesto')
        return roles

class Filter(QObject):

    def __init__(self): # inicializace 
        QObject.__init__(self)
        self._city = True # private attributes
        self._village = True

        self._population_min = 0
        self._population_max  = 1500000

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

    def get_city(self):
        return self._city

    def get_village(self):
        return self._village
    
    def filter_obec(self, var): # m = self.browser_city[index.row()]['properties']['mesto']
        if self._city == True and self._village == True:
            pass
        elif self._city == True and self._village == False:
            if m.value == 1:
                res = m
            return res
        elif self.city == False and self._village == True:
            if m.value == 0:
                res = m
            return res
        else:
            res = 0
            return res

    city_changed = Signal(bool)
    village_changed = Signal(bool)
    population_min_changed = Signal(int)
    population_max_changed = Signal(int)
    city_village_choise = Signal()

    city = Property(bool, get_city, set_city, notify=city_changed)
    village = Property(bool, lambda self: self._village, set_village, notify=village_changed)
    population_min = Property(int, lambda self: self._population_min, set_population_min, notify=population_min_changed)
    population_max = Property(int, lambda self: self._population_max, set_population_max, notify=population_max_changed)

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
browsercity_model = BrowserCityModel(CITY_LIST_FILE)
filt = Filter()
ctxt = view.rootContext()
ctxt.setContextProperty('browserCityModel',browsercity_model)
ctxt.setContextProperty("filt", filt)

view.setSource(url)
view.show()
app.exec_()
