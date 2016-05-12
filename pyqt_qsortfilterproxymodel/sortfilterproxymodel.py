from PyQt5.QtCore import pyqtProperty, pyqtSlot, QSortFilterProxyModel, Q_ENUMS, QAbstractItemModel, QByteArray, QRegExp, QObject

class SortFilterProxyModel(QSortFilterProxyModel):

    class FilterSyntax:
        RegExp, Wildcard, FixedString = range(3)

    Q_ENUMS(FilterSyntax)

    def __init__(self, parent):
        self._sortRole = None
        self._filterRole = None
        super().__init__(parent)

    @pyqtSlot(int, int, str, result=QObject)
    def item(self, row, column, role):
        proxyIndex = super().index(row, column)
        return super().data(proxyIndex, self._roleKey(role))


    @pyqtProperty(QAbstractItemModel)
    def source(self):
        return super().sourceModel()

    @source.setter
    def source(self, source):
        self.setSourceModel(source)
        # The sort and filter roles might have been set before the source itself
        # in that case we have to set them again
        if self._sortRole:
          self.sortRole = self._sortRole
        if self._filterRole:
          self.filterRole = self._filterRole

    @pyqtProperty(int)
    def sortOrder(self):
        return self._order

    @sortOrder.setter
    def sortOrder(self, order):
        self._order = order
        super().sort(0, order)

    @pyqtProperty(QByteArray)
    def sortRole(self):
        return self._sortRole

    @sortRole.setter
    def sortRole(self, role):
        self._sortRole = role
        super().setSortRole(self._roleKey(role))

    @pyqtProperty(QByteArray)
    def filterRole(self):
        return self._filterRole

    @filterRole.setter
    def filterRole(self, role):
        self._filterRole = role
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
            roles = self.roleNames()
            for key, value in roles.items():
                data = model.data(sourceIndex, key)
                if rx.indexIn(str(data)) != -1:
                    return True
            return False
        # Here we have a filterRole so only search in that
        data = model.data(sourceIndex, self._roleKey(self.filterRole))
        return rx.indexIn(str(data)) != -1

    def _roleKey(self, role):
        roles = self.roleNames()
        for key, value in roles.items():
            if value == role:
                return key
        return -1

    def roleNames(self):
        source = super().sourceModel()
        if source:
            return source.roleNames()
        return {}

