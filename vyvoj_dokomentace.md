# Vývojová dokumentace
Následující skipt byl vytvořen v prostředí PySide2 a QtQuick. Jako mapový podklad slouží volně dostupné OpenStreetMap, které jsou nahrány do prostředí pythonu pomocí pluginu.

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

### 3. Filter
...


## Popis grafického rozhranní aplikace
Rozložení aplikace se skládá ze dvou hlavních sloupců. 

V levém sloupci se nachází možnosti pro filtrování - 2x CheckBox pro volbu města a obcí, RangeSlider a dvě textová pole pro volbu minimálního a maximálního počtu obyvatel, 2x ComboBox pro výběr kraje a okresu. Na konci výběru možnotí pro filtrování se nachází tlačítko *filtrovat*, které provádí nastavenou filtraci. Níže se nachází seznam, v němž jsou uvedeny vyfiltrované obce spolu se základními informacemi o nich (rozloha, počet obyvatel) a jsou barevně rozlišeny na města (červeným a tučným písmem) a obce.

Celý pravý sloupec zabírá mapa, která zobrazuje vyfiltrovaná města a obce (jsou stejně barevně odlišena jako v seznamu vlevo). Obce jsou vizualizovány bodem, jehož barva je také rozlišena pro obce a města. 

Rozměr mapy se automaticky přizpůsobuje velikosti okna.

## QML
### CheckBox
Oba dva CheckBoxy jsou metodou *checkState* propojeny s *property* pro filtrování. V této *property* jsou hodnoty CheckBoxů předány filtrovací funkci.

### RangeSlider
Zde je propojení s *property* realizováno metodami *first.value* a *second.value*. Opět jsou hodnoty předány filtrovací funkci. 

### Textová editovatelná pole
Pro zadávání minimálního a maximálního počtu obyvatel jsou zde vytvořena dvě editovatelná textová pole, která předávají filtrovací funkci vstupní hodnoty od uživatele do stejných proměnných jako RangeSlider. 

### ComboBox
První ComboBox obsahuje názvy krajů a druhý předpřipravený seznam okresů. Oba dva předávají vybranou hodnotu metodou *currentIndex* a *currentText* filtrovací funkci.  

### Button
Při kliknutí na tlačítko *filtrovat* je zavolaná funkce *modifyList()* na *browserCityModel*. ... 

### ListView
ListView zobrazuje seznam filtrovaných měst a obcí a k nim informace o jejich rozloze a počtu obyvatel. Hodnoty jsou předávány pomocí definovaných rolí. Barevné rozlišení měst a obcí zajišťuje hodnota role město, která testována v if podmínce: *(model.mesto == 1) ? colorCity : colorVillage*. Na stejném principu je realizováno i vytvoření tučného písma u měst. Položku v ListView je možné vybrat pomocí MouseArea. Při kliknutí je vybraná položka ještě zvýrazněna modrým obdélníkem v ListView a zároveň znázorněná na mapě. 

### Mapa
Mapa využívá plugin z OpenStreetMap pro zobrazení podkladu a je propojena s listView pomocí Connection. Pokud je ListView změněn, přiblíží nebo oddálí se na hodnotu 12. Dále jsou v mapě zobrazeny názvy obcí a bodový znak, které jsou vizualizovány pomocí MapItemView. 
