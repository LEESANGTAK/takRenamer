from imp import reload

import pymel.core as pm

from . import takRenamer as tr; reload(tr)
from . import gui; reload(gui)


def showUI():
    gui.TakRenamerDialog.delInstance()

    takRenamerObj = tr.TakRenamer(pm.selected())
    gui.TakRenamerDialog.INSTANCE = gui.TakRenamerDialog(takRenamerObj)
    gui.TakRenamerDialog.INSTANCE.setEndSuffix()
    gui.TakRenamerDialog.INSTANCE.setHashStartNum()

    gui.TakRenamerDialog.INSTANCE.show()
    gui.TakRenamerDialog.INSTANCE.refreshNamesTable()
