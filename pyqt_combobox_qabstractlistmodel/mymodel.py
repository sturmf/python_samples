from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QAbstractListModel, Qt, QModelIndex, QVariant


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
    _roles = {
        NameRole: b"name",
    }

    itemChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = [MyItem('one', self), MyItem('two', self), MyItem('three', self)]
        self._item = self._items[1]

    def roleNames(self):
        _roles = super().roleNames()
        _roles.update(self._roles)
        return _roles

    @pyqtSlot(result=int)
    @pyqtSlot(QModelIndex, result=int)
    def rowCount(self, parent=QModelIndex()):
        return len(self._items)


    @pyqtProperty(MyItem, notify=itemChanged)
    def item(self):
        return self._item

    @item.setter
    def item(self, item):
        print('trying to set item to %s' % item.name)
        if self._item != item:
            print('item changed to %s' % item.name)
            self._item = item
            self.itemChanged.emit()

    @pyqtSlot()
    def new_item(self):
        print('Append new item')
        super().beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._items.append(MyItem('new', self))
        super().endInsertRows()

    @pyqtSlot(int, result=MyItem)
    def get(self, row):
        print("\nIndex enter")
        item = self._items[row]
        print('item', item)
        print("Index end\n")
        return item

    @pyqtSlot(QModelIndex, result=QVariant)
    @pyqtSlot(QModelIndex, int, result=QVariant)
    def data(self, index, role=Qt.DisplayRole):
        try:
            item = self._items[index.row()]
        except IndexError:
            return QVariant()

        if role == self.NameRole:
            return item.name

        return QVariant()
