from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import typing
import sys
import json

VIEW_URL = "zaklad_3.qml"   # Advanced user interface
CITY_LIST_FILE = "cities.geojson"

class BrowserCityModel(QAbstractListModel):
        
    class Roles(Enum):
        """Enum with added custom roles"""
        LOCATION = QtCore.Qt.UserRole+0
        AREA = QtCore.Qt.UserRole+1
        POPULATION = QtCore.Qt.UserRole+2
    
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

            # Create QGeoCoordinate from the original JSON location
            for c in self.browser_city['features']:
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
            return self.browser_city['features'][index.row()]['properties']['NAZ_OBEC']
        if role == self.Roles.POPULATION.value:
            return self.browser_city['features'][index.row()]['properties']['POCET_OBYV']
        if role == self.Roles.AREA.value:
            return self.browser_city['features'][index.row()]['properties']['SHAPE_Area']
        if role == self.Roles.LOCATION.value:
            return self.browser_city['features'][index.row()]['geometry']['coordinates']
    
    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.POPULATION.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.LOCATION.value] = QByteArray(b'location')
        return roles


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
browsercity_model = BrowserCityModel(CITY_LIST_FILE)
ctxt = view.rootContext()
ctxt.setContextProperty('browserCityModel',browsercity_model)
view.setSource(url)
view.show()
app.exec_()
