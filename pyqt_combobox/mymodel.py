from PyQt5.QtCore import pyqtProperty, pyqtSignal, pyqtSlot, QObject
from PyQt5.QtQml import QQmlListProperty


class MyItem(QObject):

    nameChanged = pyqtSignal()

    def __init__(self, name, parent=None):
        QObject.__init__(self, parent)
        self._name = name

    @pyqtProperty('QString', notify=nameChanged)
    def name(self):
        return self._name


class MyModel(QObject):

    itemChanged = pyqtSignal()
    itemsChanged = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self._items = [MyItem('one'), MyItem('two'), MyItem('three')]
        self._item = self._items[2]

    @pyqtProperty(MyItem, notify=itemChanged)
    def item(self):
        return self._item

    @pyqtProperty(QQmlListProperty, notify=itemsChanged)
    def items(self):
        print('Query for items')
        return QQmlListProperty(MyItem, self, self._items)

    @pyqtSlot()
    def new_item(self):
        print('Append new item')
        self._items.append(MyItem('new'))
        self.itemsChanged.emit()
