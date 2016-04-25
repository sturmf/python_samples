from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSortFilterProxyModel, QAbstractItemModel, QAbstractListModel, QModelIndex, Qt


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent):
        super().__init__(parent)
        #self._m = MyModel(parent)
        #self.setSourceModel(self._m)

    @pyqtProperty(QAbstractItemModel)
    def source (self):
        return self._source

    @source.setter
    def source (self, source):
        self.setSourceModel(source)
        self._source = source


class MyItem(QObject):

    nameChanged = pyqtSignal()

    def __init__(self, name, parent=None):
        QObject.__init__(self, parent)
        self._name = name

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name


class MyModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    _roles = {NameRole: "name"}

    def __init__(self, parent=None):
        print("constructing")
        super().__init__(parent)
        self._items = [MyItem('one'), MyItem('two'), MyItem('three')]
        self._column_count = 1

    def roleNames(self):
        print("roleNames")
        return self._roles

    def rowCount(self, parent=QModelIndex()):
        print("rowCount", len(self._items))
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        print("in data")
        try:
            item = self._items[index.row()]
        except IndexError:
            return QVariant()

        if role == self.NameRole:
            return item.name

        return QVariant()
