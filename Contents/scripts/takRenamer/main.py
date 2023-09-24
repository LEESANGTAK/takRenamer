import imp
import pymel.core as pm

from . import takRenamer as tr
from . import gui
imp.reload(tr)

def showUI():
    gui.TakRenamerDialog.delInstance()

    takRenamerObj = tr.TakRenamer(pm.selected())
    gui.TakRenamerDialog.INSTANCE = gui.TakRenamerDialog(takRenamerObj)
    gui.TakRenamerDialog.INSTANCE.setEndSuffix()
    gui.TakRenamerDialog.INSTANCE.setHashStartNum()

    gui.TakRenamerDialog.INSTANCE.show()
    gui.TakRenamerDialog.INSTANCE.refreshNamesTable()
