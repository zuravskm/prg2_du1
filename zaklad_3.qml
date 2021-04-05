import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.6
import QtPositioning 5.6

Row{
    id: row1
    height: 600
    width: 800

    property var currentModelItem;

    Column{
        spacing: 3
        id: column1
        width: 350
        height: parent.height

        Text {
            id: textVyber
            x: 5
            y: 10
            text: "vybrat:"
        }

        Row {
            Column{
                CheckDelegate {
                    id: checkDelegateMesto
                    /* x: 5 */
                    text: "města"
                }
            }
            Column {
                CheckDelegate {
                    id: checkDelegateObce
                    /* x: 200 */
                    text: "obce"
                }
            }    
        }

        Text {
            id: text2
            x: 89
            y: 200
            text: "počet obyvatel"
        }

        RangeSlider {
            id: rangeSlider
            x: 5
            width: 240
            stepSize: 2000
            to: 1500000
            from: 1
            first.value: 1
            second.value: 1500000
        }

        Column {
            spacing: 1
            Text {
                id: textOd
                x: 5
                text: "od:"
            }
            /* TextEdit {
                id: textEditOd
                width: 210
                height: 15
                text: "0"
            } */

            Text {
                id: textDo
                x: 5
                text: "do:"
            }
            /* TextEdit {
                id: textEdit4
                width: textDo.width + 15
                text: "1500000"
            } */
        }

        ComboBox {
            id: comboKraj
            x: 5
            height: 30
            width: 240
            displayText: "vyber kraj"
        }
        
        ComboBox {
            id: comboOkres
            x: 5
            height: 30
            width: 240
            displayText: "vyber okres"
        }
        
        Button {
            id: button
            x: 89
            height: 30
            text: "filtrovat"
        }

        ListView {
            id: browserCity
            focus: true
            x: 5
            height: 200
            width: 240
            
            Component {
                id: browserCityDelegate
                Item {
                    height: childrenRect.height
                    width: parent.width
                    Text {
                        text: model.display + '<br>Rozloha:' + model.area + ' km<sup>2</sup>' + '<br>Počet obyvatel:' + model.population
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

    Column{
        spacing: 3
        id: column2
        width: 350
        height: parent.height

    
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
                target: column1
                onCurrentItemChanged: myMap.zoomLevel = 12 }

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