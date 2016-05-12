import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2
import MyModel 1.0
import MyItem 1.0
import SortFilterProxyModel 1.0

ApplicationWindow {

    id: window
    width: 800; height: 600
    color: "gray"

    toolBar: ToolBar {
        TextField {
            id: searchBox

            width: window.width / 3
            placeholderText: qsTr("Search...")
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
        }
    }

    MyModel {
        id: mymodel
    }

    TableView {
        id: tableView
        anchors.fill: parent
        model: SortFilterProxyModel {
            id: proxyModel
            source: mymodel

            sortOrder: tableView.sortIndicatorOrder
            sortCaseSensitivity: Qt.CaseInsensitive
            sortRole: tableView.getColumn(tableView.sortIndicatorColumn).role

            filterString: "*" + searchBox.text + "*"
            filterSyntax: SortFilterProxyModel.Wildcard
            filterCaseSensitivity: Qt.CaseInsensitive
            filterRole: tableView.getColumn(tableView.sortIndicatorColumn).role

        }
        sortIndicatorVisible: true

        TableViewColumn {
            role: "name"
            title: "Name"
        }
        onActivated: {
            console.log("Row clicked: " + model.item(row, 0, 'object').name)
        }
    }

}
