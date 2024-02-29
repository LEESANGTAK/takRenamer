import os

from PySide2 import QtUiTools, QtCore, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import pymel.core as pm


def getMayaMainWindow():
    mayaMainWinPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mayaMainWinPtr), QtWidgets.QWidget)


class TakRenamerDialog(QtWidgets.QDialog):
    UI_FILES_PATH = os.path.join(os.path.dirname(__file__), 'widgets')
    INSTANCE = None

    @classmethod
    def delInstance(cls):
        if cls.INSTANCE:
            cls.INSTANCE.close()
            cls.INSTANCE.deleteLater()

    def __init__(self, takRenamer, parent=getMayaMainWindow()) :
        super(TakRenamerDialog, self).__init__(parent)

        self._ui = None
        self._takRenamer = takRenamer

        self.createWidgets()
        self.createLayouts()
        self.createConnections()
        self.setDefaultState()

    def createWidgets(self):
        loader = QtUiTools.QUiLoader()
        self._ui = loader.load(os.path.join(TakRenamerDialog.UI_FILES_PATH, 'main.ui'), parentWidget=None)

        self._ui.namesTableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

    def createLayouts(self):
        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setMargin(0)
        mainLayout.addWidget(self._ui)

    def createConnections(self):
        self._ui.namesTableWidget.customContextMenuRequested.connect(self.showPopupMenu)
        self._ui.newNameLineEdit.editingFinished.connect(self.setHashName)
        self._ui.prefixLineEdit.editingFinished.connect(self.addPrefix)
        self._ui.suffixLineEdit.editingFinished.connect(self.addSuffix)
        self._ui.replaceLineEdit.editingFinished.connect(self.searchReplace)
        self._ui.startNumSpinbox.valueChanged.connect(self.setHashStartNum)
        self._ui.endSuffixLineEdit.editingFinished.connect(self.setEndSuffix)
        self._ui.setEndSuffixChkbox.stateChanged.connect(self.setEndSuffixOption)
        self._ui.clearEndIntsChkbox.stateChanged.connect(self.clearEndInts)
        self._ui.applyButton.clicked.connect(self.apply)
        self._ui.cancelButton.clicked.connect(self.close)

    def setDefaultState(self):
        self.setWindowTitle('Tak Renamer')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setMinimumHeight(500)

    def showPopupMenu(self, pos):
        menu = QtWidgets.QMenu(self)
        menu.addAction('Load Selections', self.loadSelections)
        menu.exec_(self.mapToGlobal(pos))

    def loadSelections(self):
        sels = pm.selected()

        self._takRenamer.longOrigNames = sels
        self.addPrefix()
        self.addSuffix()
        self.setHashName()
        self.setHashStartNum()
        self.setEndSuffix()
        self.clearEndInts(self._ui.clearEndIntsChkbox.isChecked())
        self.searchReplace()

        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def fillNamesTableContents(self):
        self._ui.namesTableWidget.setRowCount(len(self._takRenamer.niceOrigNames))
        self._ui.namesTableWidget.setColumnCount(2)

        for i in range(len(self._takRenamer.longOrigNames)):
            oldNameItem = QtWidgets.QTableWidgetItem(self._takRenamer.niceOrigNames[i])
            newNameItem = QtWidgets.QTableWidgetItem(self._takRenamer.newNames[i])
            oldNameItem.setTextAlignment(QtCore.Qt.AlignHCenter)
            newNameItem.setTextAlignment(QtCore.Qt.AlignHCenter)

            self._ui.namesTableWidget.setItem(i, 0, oldNameItem)
            self._ui.namesTableWidget.setItem(i, 1, newNameItem)

    def refreshNamesTable(self):
        self._ui.namesTableWidget.clearContents()
        self.fillNamesTableContents()

    def addPrefix(self):
        prefix = self._ui.prefixLineEdit.text()
        self._takRenamer.prefix = prefix
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def addSuffix(self):
        suffix = self._ui.suffixLineEdit.text()
        self._takRenamer.suffix = suffix
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def setHashName(self):
        hashName = self._ui.newNameLineEdit.text()
        self._takRenamer.hashName = hashName
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def searchReplace(self):
        self._takRenamer.searchStr = self._ui.searchLineEdit.text()
        self._takRenamer.replaceStr = self._ui.replaceLineEdit.text()
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def setHashStartNum(self):
        self._takRenamer.hashStartNum = self._ui.startNumSpinbox.value()
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def clearEndInts(self, state):
        self._takRenamer.clearEndIntsFlag = bool(state)
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def setEndSuffix(self):
        self._takRenamer.endSuffix = self._ui.endSuffixLineEdit.text()
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def setEndSuffixOption(self, state):
        self._takRenamer.setEndSuffixFlag = bool(state)
        self._takRenamer.updateNames()
        self.refreshNamesTable()

    def apply(self):
        self.setFocus()
        self._takRenamer.apply()
        self._takRenamer.reset()
        # self.clear()
        self.refreshNamesTable()

    def clear(self):
        self._ui.prefixLineEdit.setText("")
        self._ui.suffixLineEdit.setText("")
        self._ui.newNameLineEdit.setText("")
        self._ui.searchLineEdit.setText("")
        self._ui.replaceLineEdit.setText("")
        self._ui.clearEndIntsChkbox.setChecked(False)
