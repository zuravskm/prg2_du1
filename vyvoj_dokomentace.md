# Vývojová dokumentace
Následující skript byl vytvořen v prostředí PySide2 a QtQuick. Jako mapový podklad slouží volně dostupné OpenStreetMap, které jsou nahrány do prostředí pythonu pomocí pluginu.

## 1. Data sídel
Data jsou ve formátu *.geojson a jejich atributy využívané v této aplikaci jsou: souřadnice, počet obyvatel, rozloha, název obce, název administrativních jednotek a informace, zda se jedná o město. Data (geometrie) pochází z open dat Wikidata, atributová data byla získána z databáze ArcČR 500.

## 2. Implementované třídy a funkce
### BrowserCityModel - dědí od QAbstractListModel
Tento model načítá data ze souboru *.geojson a vytvoří seznam obcí s jejich souřadnicemi. Funkce load_from_json(self, filename) vrací seznam všech obcí ze vstupních dat. Uchovává 2 důležité seznamy – browser_city, který obsahuje data určená k zobrazení (vyfiltrovaná data) a full_city_list, který obsahuje veškerá sídla načtená ze zdrojového geojsonu bez ohledu na aktuální nastavení filtrů. 

V rámci této třídy je ještě vytvořena třída Roles, v níž jsou definované 4 role: LOCATION, AREA, POPULATION A MESTO.  Metoda data(self, index:QtCore.QModelIndex, role:int=...) přiřazuje výše uvedeným rolím data z načteného geojson. V této části je také provedeno zaokrouhlení rozlohy na celé kilometry. Další metoda roleNames(self) definuje názvy rolí, které jsou následně využity v *.qml souboru. 

Podstatná je výkoná metoda modifyList alias Slot, která slouží pro vyfiltrování sídel, smazání a znovu načtení vyfiltrovaného seznamu do qml. V této metodě je zároveň z vyfiltrovaných dat počítáno těžiště se záměrem do tohoto těřiště umístit střed mapy a zabírat tak všechna vyfiltrovaná data. 
Nakonec je zde referenční atribut, kterým je třída propojen s třídou Filter(). 

### Filter - dědí od QObject
Třída Filter() uchovává nastavení veškerých filtrů definovaných uživatelem ve svých atributech. Jedná se o město/vesnici - true/false, max a min populaci, vybraný kraj a okres. Je zde jediná výkonná metoda filterCities(self, city), která zajišťuje samotné filtrování a vrací feature geojsonu pouze v případě, že tato feature "projde" přes všechny filtry. 

### Funkce choose_district(index)
V této funkci je definováno administrativní rozdělení dle okresů a jsou definovány možnosti pro flitrování podle jednotlivých územních jednotek, nebo dohromady. Okresy jsou uchovávány ve slovníku, jehož klíči jsou názvy krajů. Toto programátorsky neelegantní řešení bylo zvoleno jelikož v pythonu jsou problémy s propojováním python seznamů a tzv. comboboxů v qml viz. (https://forum.qt.io/topic/116304/example-of-a-model-for-use-with-qtquick-combobox-qml "QT fórum"). Možnosti v comboboxu pro výběr okresů jsou updatovány s pomocí nastavení context property ze setteru set_districts(self, new_val).




## 3. Popis grafického rozhranní aplikace
Rozložení aplikace se skládá ze dvou hlavních sloupců. 

V levém sloupci se nachází možnosti pro filtrování - 2x CheckBox pro volbu města a obcí, RangeSlider a dvě textová pole pro volbu minimálního a maximálního počtu obyvatel, 2x ComboBox pro výběr kraje a okresu. S pomocí bindingů jsou tyto komponenty propojeny s Properties třídy Filter(). Na konci výběru možností pro filtrování se nachází tlačítko *filtrovat*, které provádí nastavenou filtraci a je zapojeno do slotu modifyList().  Níže se nachází seznam, v němž jsou uvedeny vyfiltrované obce spolu se základními informacemi o nich (rozloha, počet obyvatel) a jsou barevně rozlišeny na města (červeným a tučným písmem) a obce.

Celý pravý sloupec zabírá mapa, která zobrazuje vyfiltrovaná města a obce (jsou stejně barevně odlišena jako v seznamu vlevo). Obce jsou vizualizovány bodem, jehož barva je také rozlišena pro obce a města. 

Rozměr mapy se automaticky přizpůsobuje velikosti okna.

## 4. QML
### CheckBox, RangeSlider
Jsou svázány s pomocí bindingu s příslušnými Properties třídy Filter(). 

### Textová editovatelná pole
Pro zadávání minimálního a maximálního počtu obyvatel jsou zde vytvořena dvě editovatelná textová pole, která předávají vstupní hodnoty od uživatele do stejných Property jako RangeSlider. 

### ComboBox
První ComboBox obsahuje názvy krajů a druhý předpřipravený seznam okresů. Oba dva předávají vybranou hodnotu (*currentIndex* a *currentText*).  

### Button
Při kliknutí na tlačítko *filtrovat* je zavolaná funkce - slot - *modifyList()* třídy *browserCityModel*. ... 

### ListView
ListView zobrazuje seznam filtrovaných měst a obcí a k nim informace o jejich rozloze a počtu obyvatel. Hodnoty jsou předávány pomocí definovaných rolí. Barevné rozlišení měst a obcí zajišťuje hodnota role město, která testována v if podmínce: *(model.mesto == 1) ? colorCity : colorVillage*. Na stejném principu je realizováno i vytvoření tučného písma u měst. Položku v ListView je možné vybrat pomocí MouseArea. Při kliknutí je vybraná položka ještě zvýrazněna modrým obdélníkem v ListView a zároveň znázorněná na mapě. 

### Mapa
Mapa využívá plugin z OpenStreetMap pro zobrazení podkladu a je propojena s listView pomocí Connection. Pokud je ListView změněn, přiblíží nebo oddálí se na hodnotu 12. Dále jsou v mapě zobrazeny názvy obcí a bodový znak, které jsou vizualizovány pomocí MapItemView. 
