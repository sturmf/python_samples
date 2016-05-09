from PyQt5.QtCore import pyqtProperty, pyqtSlot, QSortFilterProxyModel, Q_ENUMS, QAbstractItemModel, QByteArray, QRegExp
from mymodel import MyItem

class SortFilterProxyModel(QSortFilterProxyModel):

    class FilterSyntax:
        RegExp, Wildcard, FixedString = range(3)

    Q_ENUMS(FilterSyntax)

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
        return self._sortRole
        #return self._roleNames().get(super().sortRole())

    @sortRole.setter
    def sortRole(self, role):
        self._sortRole = role
        super().setSortRole(self._roleKey(role))

    @pyqtProperty(QByteArray)
    def filterRole(self):
        return self._filterRole
        #return self._roleNames().get(super().filterRole())

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
            roles = self._roleNames()
            for key, value in roles.items():
                data = model.data(sourceIndex, key)
                if rx.indexIn(str(data)) != -1:
                    return True
            return False
        # Here we have a filterRole so only search in that
        data = model.data(sourceIndex, self._roleKey(self.filterRole))
        return rx.indexIn(str(data)) != -1

    def _roleKey(self, role):
        roles = self._roleNames()
        for key, value in roles.items():
            if value == role:
                return key
        return -1

    def _roleNames(self):
        source = super().sourceModel()
        if source:
            return source.roleNames()
        return {}

    @pyqtSlot(int, result=MyItem)
    def get(self, i):
        return self.source.get(i)
