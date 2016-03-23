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
        currentIndex: getCurrentIndex(mymodel.items, mymodel.item)
        model: mymodel.items
        textRole: 'name'
    }
    Button {
        anchors.top: combo.bottom
        text: 'Add item'
        onClicked: mymodel.new_item()
    }

}
