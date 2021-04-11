# Vývojová dokumentace
Následující skipt byl vytvořen v prostředí PySide2 a QtQuick. 

## Data sídel
Data jsou ve formátu *.geojson a jejich atributy využívané v této aplikaci jsou: souřadnice, počet obyvatel, rozloha, název obce, název administrativních jednotek a informace, zda se jedná o město.

## Implementované třídy a funkce
### 1. BrowserCityModel
Tento model načítá data ze souboru *.geojson a vytvoří seznam obcí s jejich souřadnicemi. Funkce load_from_json(self, filename) vrací seznam všech obcí ze vstupních dat.

V rámci této třídy je ještě vytvořena třída Roles, v níž jsou definované 4 role: LOCATION, AREA, POPULATION A MESTO. Funkce data(self, index:QtCore.QModelIndex, role:int=...) přiřazuje výše uvedeným rolím data z načteného geojson. V této části je také provedeno zaokrouhlení rozlohy na celé kilometry. Další funkce roleNames(self) definuje názvy rolí, které jsou následně využity v *.qml souboru. 

Slot...
Na konci této třídy je volána třída Filter().

### 2. Funkce choose_district(index)
V této funkci je definováno administrativní rozdělení dle okresů a jsou definovány možnosti pro flitrování podle jednotlivých územních jednotek, nebo dohromady. 

### 3. Filetr
...


## Popis grafického rozhranní aplikace
Rozložení aplikace se skládá ze dvou hlavních sloupců. 

V levém sloupci se nachází možnosti pro filtrování - 2x check button pro volbu města a obcí, RangeSlider a dvě textová pole pro volbu minimálního a maximálního počtu obyvatel, 2x ComboBox pro výběr kraje a okresu. Na konci výběru možnotí pro filtrování se nachází tlačítko filtrovat, které provádí nastavenou filtraci. 





