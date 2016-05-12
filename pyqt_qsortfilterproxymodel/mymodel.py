from PyQt5.QtCore import pyqtProperty, pyqtSignal, QObject, QAbstractListModel, Qt, QModelIndex, QVariant

class MyItem(QObject):

    nameChanged = pyqtSignal()

    def __init__(self, name, parent=None):
        QObject.__init__(self, parent)
        self._name = name

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name


class MyModel(QAbstractListModel):
    ObjectRole = Qt.UserRole + 1 # We always want a way to access the underlying object
    NameRole = Qt.UserRole + 2
    _roles = {
        NameRole: "name",
        ObjectRole: "object",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = [MyItem('one'), MyItem('two'), MyItem('three')]
        self._column_count = 1

    def roleNames(self):
        _roles = super().roleNames()
        _roles.update(self._roles)
        return _roles

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        try:
            item = self._items[index.row()]
        except IndexError:
            return QVariant()

        if   role == self.NameRole:
            return item.name
        elif role == self.ObjectRole:
            return item

        return QVariant()

