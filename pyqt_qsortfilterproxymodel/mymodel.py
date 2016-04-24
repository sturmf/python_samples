from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject, QSortFilterProxyModel
from PyQt5.QtQml import QQmlListProperty, QQmlListReference


class SortFilterProxyModel(QSortFilterProxyModel):

    @pyqtProperty(QQmlListReference)
    def source (self):
        return self._source

    @source.setter
    def source (self, source):
        setSourceModel(source)
        self._source = source


class MyItem(QObject):

    nameChanged = pyqtSignal()

    def __init__(self, name, parent=None):
        QObject.__init__(self, parent)
        self._name = name

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name


class MyModel(QObject):

    itemsChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._items = [MyItem('one'), MyItem('two'), MyItem('three')]

    @pyqtProperty(QQmlListProperty, notify=itemsChanged)
    def items(self):
        print('Query for items')
        return QQmlListProperty(MyItem, self, self._items)

    @pyqtSlot()
    def new_item(self):
        print('Append new item')
        self._items.append(MyItem('new'))
        self.itemsChanged.emit()
