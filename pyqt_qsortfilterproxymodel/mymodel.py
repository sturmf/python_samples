from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QVariant, QByteArray, QSortFilterProxyModel, QAbstractItemModel, QAbstractListModel, QModelIndex, Qt, QRegExp


class SortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent):
        super().__init__(parent)

    @pyqtProperty(QAbstractItemModel)
    def source(self):
        return super().sourceModel()

    @source.setter
    def source(self, source):
        self.setSourceModel(source)

    @pyqtProperty(int)
    def sortOrder(self):
        return self._order

    @sortOrder.setter
    def sortOrder(self, order):
        self._order = order
        super().sort(0, order)

    @pyqtProperty(QByteArray)
    def sortRole(self):
        return self._roleNames().get(super().sortRole())

    @sortRole.setter
    def sortRole(self, role):
        super().setSortRole(self._roleKey(role))

    @pyqtProperty(QByteArray)
    def filterRole(self):
        return self._roleNames().get(super().filterRole())

    @filterRole.setter
    def filterRole(self, role):
        super().setFilterRole(self._roleKey(role))

    @pyqtProperty(str)
    def filterString(self):
        return super().filterRegExp().pattern()

    @filterString.setter
    def filterString(self, filter):
        super().setFilterRegExp(QRegExp(filter, super().filterCaseSensitivity(), self.filterSyntax))

    @pyqtProperty(int)
    def filterSyntax(self):
        return super().filterRegExp().patternSyntax()

    @filterSyntax.setter
    def filterSyntax(self, syntax):
        super().setFilterRegExp(QRegExp(self.filterString, super().filterCaseSensitivity(), syntax))

    def filterAcceptsRow(self, sourceRow, sourceParent):
        rx = super().filterRegExp()
        if not rx or rx.isEmpty():
            return True
        model = super().sourceModel()
        sourceIndex = model.index(sourceRow, 0, sourceParent)
        # skip invalid indexes
        if not sourceIndex.isValid():
            return True
        # If no filterRole is set, iterate through all keys
        if not self.filterRole or self.filterRole == "":
            roles = self._roleNames()
            for key, value in roles.items():
                data = model.data(sourceIndex, key)
                if rx.indexIn(data) != -1:
                    return True
            return False
        # Here we have a filterRole so only search in that
        data = model.data(sourceIndex, self._roleKey(self.filterRole))
        return rx.indexIn(data) != -1

    def _roleKey(self, role):
        roles = self.roleNames()
        for key, value in roles.items():
            if value == role:
                return key
        return -1

    def _roleNames(self):
        source = super().sourceModel()
        if source:
            return source.roleNames()
        return {}


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
        super().__init__(parent)
        self._items = [MyItem('one'), MyItem('two'), MyItem('three')]
        self._column_count = 1

    def roleNames(self):
        return self._roles

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        try:
            item = self._items[index.row()]
        except IndexError:
            return QVariant()

        if role == self.NameRole:
            return item.name

        return QVariant()
