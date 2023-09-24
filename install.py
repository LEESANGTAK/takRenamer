"""
Author: Tak
Website: ta-note.com
Module Name: install.py
Description:
    Drag and drop module installer.
    Shelf button added in current shelf tab.
    "moduleName.mod" file created in "Documents\maya\modules" directory automatically.
"""

import os
import sys

import maya.cmds as cmds
import maya.mel as mel


MAYA_VERSION = int(cmds.about(version=True))
MODULE_NAME = 'takRenamer'
MODULE_VERSION = '1.0'
MODULE_PATH = os.path.dirname(__file__) + '/Contents'


def onMayaDroppedPythonFile(*args, **kwargs):
    modulesDir = getModulesDirectory()
    createModuleFile(modulesDir)
    addScriptPath()
    loadPlugins()
    addShelfButtons()

def getModulesDirectory():
    modulesDir = None

    mayaAppDir = cmds.internalVar(uad=True)
    modulesDir = os.path.join(mayaAppDir, 'modules')

    if not os.path.exists(modulesDir):
        os.mkdir(modulesDir)

    return modulesDir

def createModuleFile(modulesDir):
    moduleFileName = '{0}.mod'.format(MODULE_NAME)

    # Need to modify depend on module
    contents = '''
+ MAYAVERSION:2019 {moduleName} {moduleVersion} {modulePath}

+ MAYAVERSION:2020 {moduleName} {moduleVersion} {modulePath}

+ MAYAVERSION:2022 {moduleName} {moduleVersion} {modulePath}

+ MAYAVERSION:2024 {moduleName} {moduleVersion} {modulePath}
'''.format(moduleName=MODULE_NAME, moduleVersion=MODULE_VERSION, modulePath=MODULE_PATH)

    moduleFilePath = os.path.join(modulesDir, moduleFileName)
    with open(moduleFilePath, 'w') as f:
        f.write(contents)

def addScriptPath():
    scriptPath = MODULE_PATH + '/scripts'
    if not scriptPath in sys.path:
        sys.path.append(scriptPath)

def loadPlugins():
    pluginsPath = os.path.join(MODULE_PATH, 'plug-ins')
    if os.path.exists(pluginsPath):
        pluginFiles = os.listdir(pluginsPath)
        if pluginFiles:
            for pluginFile in pluginFiles:
                cmds.loadPlugin(os.path.join(pluginsPath, pluginFile))

def addShelfButtons():
    curShelf = getCurrentShelf()

    # Need to modify depend on module
    iconPath = 'quickRename.png'
    command = '''
from takRenamer import main;import imp;imp.reload(main);main.showUI()
'''
    cmds.shelfButton(
        command=command,
        annotation=MODULE_NAME,
        sourceType='Python',
        image=iconPath,
        image1=iconPath,
        parent=curShelf
    )

def getCurrentShelf():
    curShelf = None

    shelf = mel.eval('$gShelfTopLevel = $gShelfTopLevel')
    curShelf = cmds.tabLayout(shelf, query=True, selectTab=True)

    return curShelf
