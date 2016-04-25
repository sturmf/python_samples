import QtQuick 2.2
import QtQuick.Layouts 1.1
import QtQuick.Controls 1.2
import QtQuick.Dialogs 1.2
import MyModel 1.0
import MyItem 1.0
import SortFilterProxyModel 1.0

ApplicationWindow {

    id: mainWindow
    width: 800; height: 600
    color: "gray"

    MyModel {
        id: mymodel
    }
	
    SortFilterProxyModel {
        id: proxyModel
        source: mymodel
        //sortCaseSensitivity: Qt.CaseInsensitive
    }

    TableView {
        id: tableView
        anchors.fill: parent
        model: proxyModel
        sortIndicatorVisible: true
        onSortIndicatorOrderChanged: model.sort(getColumn(sortIndicatorColumn).role, sortIndicatorOrder)
        onSortIndicatorColumnChanged: model.sort(getColumn(sortIndicatorColumn).role, sortIndicatorOrder)
        TableViewColumn {
            role: "name"
            title: "Name"
        }
    }

}
