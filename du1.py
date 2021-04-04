from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import typing
import sys
import json

VIEW_URL = "du1_view.qml"
CITY_LIST_FILE = ".json" # doplnit

class BrowserCityModel(QAbstractListModel):
        
        class Roles(Enum):
        """Enum with added custom roles"""
        FROM = QtCore.Qt.UserRole+0
        TO = QtCore.Qt.UserRole+1
        LOCATION = QtCore.Qt.UserRole+2
        AREA = QtCore.Qt.UserRole+3
        POPULATION = QtCore.Qt.UserRole+4
    
    def __init__(self,filename=None):
        """Initialize and load list from given file"""
        QAbstractListModel.__init__(self)
        self.city_list = []
        if filename:
            self.load_from_json(filename)

    def load_from_json(self,filename):
        """Load list of cities from given file"""
        with open(filename,encoding="utf-8") as f:
            self.city_list = json.load(f)

            # Create QGeoCoordinate from the original JSON location
            for c in self.city_list:
                pos = c['location']
                lon,lat = pos.split("(")[1].split(")")[0].split(" ") # Get the part between brackets and split it on space
                c['location'] = QGeoCoordinate(float(lat),float(lon)) # Create QGeoCoordinate and overwrite original `location` entry

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        """ Return number of cities in the list"""
        return len(self.city_list)
    
    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
    """ For given index and role return information of the city"""
    # print(index.row(),role) # Print requested row and role for debugging
        if role == self.Roles.FROM.value: # On from role return population
            return self.city_list[index.row()]["population"]
        elif role == self.Roles.TO.value: # On from role return population
            return self.city_list[index.row()]["population"]
        elif role == QtCore.Qt.DisplayRole: # On DisplayRole return name
            return self.city_list[index.row()]["muniLabel"]
        elif role == self.Roles.LOCATION.value: # On location role return coordinates
            return self.city_list[index.row()]["location"]
        elif role == self.Roles.AREA.value: # On area role return area
            return self.city_list[index.row()]["area"]
        elif role == self.Roles.POPULATION.value: # On population role return population
            return self.city_list[index.row()]["population"]

    def roleNames(self) -> typing.Dict[int, QByteArray]:
        """Returns dict with role numbers and role names for default and custom roles together"""
        # Append custom roles to the default roles and give them names for a usage in the QML
        roles = super().roleNames()
        roles[self.Roles.FROM.value] = QByteArray(b'location')
        roles[self.Roles.TO.value] = QByteArray(b'location')
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.POPULATION.value] = QByteArray(b'population')
        print(roles)
        return roles




app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
browsercity_model = BrowserCityModel(CITY_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('browsercityModel',browsercity_model)
view.setSource(url)
view.show()
app.exec_()