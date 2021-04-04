import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.6
import QtPositioning 5.6

Row{
    id: row1
    height: 500
    width: 800

    Column{
        spacing: 3
        id: column1
        width: 300
        height: parent.height

        Text {
            id: textVyber
            x: 5
            text: "vybrat:"
        }

        Row {
            CheckDelegate {
                id: checkDelegateMesto
                x: 5
                text: "města"
            }
            
            CheckDelegate {
                id: checkDelegateObce
                x: 200
                text: "obce"
            }
        }

        Text {
            id: text2
            x: 86
            y: 200
            text: "počet obyvatel"
        }

        RangeSlider {
            id: rangeSlider
            width: 234
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
            width: 234
            displayText: "vyber kraj"
        }
        
        ComboBox {
            id: comboOkres
            x: 5
            height: 30
            width: 234
            displayText: "vyber okres"
        }
        
        Button {
            id: button
            x: 86
            height: 30
            text: "filtrovat"
        }
    }

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
        zoomLevel: 12

/*         Connections {
            target: myRow
            onCurrentModelItemChanged: myMap.zoomLevel = 12 }*/

        plugin: osmPlugin
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1]

/*         MapItemView {
            model: cityListModel
            delegate: MapQuickItem {
                    coordinate: model.location
                    sourceItem: Text {text: model.display}

            } */
        }
}
