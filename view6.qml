import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.6
import QtPositioning 5.6
import QtQuick.Window 2.15
import QtQuick.Layouts 1.3

RowLayout {
    id: row1
    anchors.fill: parent

    property var currentModelItem;

    ColumnLayout {
        spacing: 3
        id: column1
        Layout.fillHeight: true
        Layout.preferredWidth: 250

        Text {
            id: textVyber
            text: "vybrat:"
        }

        Row {
            Column {
                CheckBox {
                    id: checkCity
                    text: "města"
                    checked: true
                    Binding {
                            target: filt
                            property: "city"
                            value: checkCity.checkState
                    }
                }
            }
            Column {
                CheckBox {
                    id: checkVillage
                    text: "obce"
                    checked: true

                    Binding {
                            target: filt
                            property: "village"
                            value: checkVillage.checkState
                    }
                }
            }    
        }

        Text {
            id: text2
            text: "<br>počet obyvatel"
            leftPadding: 75   
        }

        RangeSlider {
            id: rangePopulation
            leftPadding: 20
            width: 250
            stepSize: 2000
            to: 1500000
            from: 1
            first.value: 0//filt.population_min    <-- zpusobuje binding loop
            second.value: 1500000//filt.population_max   <-- zpusobuje binding loop
            live: false

            Binding {
                            target: filt
                            property: "population_min"
                            value: rangePopulation.first.value
                    }
            Binding {
                            target: filt
                            property: "population_max"
                            value: rangePopulation.second.value
                    }
        }

        Column {
            spacing: 1        
            Row {
                spacing: 1
                Text {
                id: notationFrom
                text: "od:"
                leftPadding: 10           
                }
                TextInput {
                    id: textFrom
                    text: filt.population_min
                    leftPadding: 10    
                    overwriteMode: true

                    //onAccepted: filt.set_population_min(textFrom.text) 
                    Binding {
                        target: filt
                        property: "population_min"
                        value: textFrom.text
                    
                    }
                }
            }
            Row {
                spacing: 1
                Text {
                id: notationTo
                leftPadding: 10    
                text: "do:"
                }
                TextInput {
                    id: textTo
                    leftPadding: 10    
                    text: filt.population_max
                    overwriteMode: true
                    
                    Binding {
                        target: filt
                        property: "population_max"
                        value: textTo.text
                    }
                }
            }
        }

        ComboBox {
            id: comboKraj  
            height: 30
            width: 240
            displayText: "vyber kraj"
        }
        
        ComboBox {
            id: comboOkres
            //x: 5
            height: 30
            width: 240
            displayText: "vyber okres"
        }
        
        Button {
            id: button
            //x: 89
            height: 30
            text: "filtrovat"
        }

        ListView {
            id: browserCity
            focus: true
            //x: 5
            //y: 80
            Layout.preferredWidth: 250
            Layout.fillHeight: true
            Layout.topMargin: 50
            
            Component {
                id: browserCityDelegate
                Item {
                    height: childrenRect.height
                    width: parent.width
                    Text {
                        text: model.display + '<br>Rozloha: ' + model.area + ' km<sup>2</sup>' + '<br>Počet obyvatel: ' + model.population + '<br>'
                        textFormat: Text.RichText
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: browserCity.currentIndex = index
                        
                    }
                }
            }

            model: DelegateModel {
                id: browserCityDelegateModel
                model: browserCityModel
                delegate: browserCityDelegate
            }

            onCurrentItemChanged: currentModelItem = browserCityDelegateModel.items.get(browserCity.currentIndex).model 

            highlight: Rectangle {
                color: "lightsteelblue"
            }
        }
    }

    ColumnLayout {
        spacing: 3
        id: column2
        Layout.fillHeight: true
        Layout.fillWidth: true

    
        Plugin {
            id: osmPlugin
            name: "osm"
            PluginParameter {
                name: "osm.mapping.custom.host"
                value: "https://tiles.wmflabs.org/osm-no-labels/"
            }
        }

        Map {
            id: mapa
            height: parent.height
            width: parent.width

            plugin: osmPlugin
            activeMapType: supportedMapTypes[supportedMapTypes.length - 1]

            center: currentModelItem.location
            zoomLevel: 12

            Connections {
                target: browserCity
                onCurrentItemChanged: mapa.zoomLevel = 12 }

            MapItemView {
                model: browserCityModel
                delegate: MapQuickItem {
                        coordinate: model.location
                        sourceItem: Text {text: model.display}

                }
            }
        }
    }
}
