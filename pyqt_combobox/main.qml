import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2
import MyModel 1.0
import MyItem 1.0

ApplicationWindow {

    function getCurrentIndex(list, element) {
        console.log('getCurrentIndex')
        if (list && element) {
            for (var i = 0; i < list.length; i++) {
                if (list[i].name === element.name) {
                    console.log('Found item at pos: ' + i)
                    return i
                }
            }
        }
        return -1
    }

    id: mainWindow
    width: 800; height: 600
    color: "gray"


    MyModel {
      id: mymodel
    }

    ComboBox {
        id: combo
        width: parent.width
        model: mymodel.items // order is important, must be before loading currentIndex
        currentIndex: getCurrentIndex(mymodel.items, mymodel.item)
        onCurrentIndexChanged: mymodel.item = model[currentIndex]
        textRole: 'name'
        Component.onCompleted: {
            combo.modelChanged.connect(modelUpdated)
        }
        function modelUpdated() {
            console.log('model updated')
        }

    }
    Button {
        anchors.top: combo.bottom
        text: 'Add item'
        onClicked: mymodel.new_item()
    }

}
