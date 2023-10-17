import re

import pymel.core as pm


class TakRenamer(object):
    def __init__(self, longNames=[]):
        self._longOrigNames = longNames[:]
        self._niceOrigNames = [getShortName(name) for name in self._longOrigNames]
        self._newNames = []

        self._hashName = None
        self._prefix = None
        self._suffix = None
        self._searchStr = None
        self._replaceStr = None
        self._setEndSuffixFlag = False
        self._clearEndIntsFlag = False
        self._hashStartNum = None
        self._endSuffix = None

        self.updateNames()

    @property
    def longOrigNames(self):
        return self._longOrigNames

    @longOrigNames.setter
    def longOrigNames(self, vals):
        self._longOrigNames = vals

    @property
    def niceOrigNames(self):
        return self._niceOrigNames

    @property
    def newNames(self):
        return self._newNames

    @newNames.setter
    def newNames(self, vals):
        self._newNames = vals

    @property
    def hashName(self):
        return self._hashName

    @hashName.setter
    def hashName(self, val):
        self._hashName = val

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, val):
        self._prefix = val

    @property
    def suffix(self):
        return self._suffix

    @suffix.setter
    def suffix(self, val):
        self._suffix = val

    @property
    def searchStr(self):
        return self._searchStr

    @searchStr.setter
    def searchStr(self, val):
        self._searchStr = val

    @property
    def replaceStr(self):
        return self._replaceStr

    @replaceStr.setter
    def replaceStr(self, val):
        self._replaceStr = val

    @property
    def setEndSuffixFlag(self):
        return self._setEndSuffixFlag

    @setEndSuffixFlag.setter
    def setEndSuffixFlag(self, val):
        self._setEndSuffixFlag = val

    @property
    def clearEndIntsFlag(self):
        return self._clearEndIntsFlag

    @clearEndIntsFlag.setter
    def clearEndIntsFlag(self, val):
        self._clearEndIntsFlag = val

    @property
    def hashStartNum(self):
        return self._hashStartNum

    @hashStartNum.setter
    def hashStartNum(self, val):
        self._hashStartNum = val

    @property
    def endSuffix(self):
        return self._endSuffix

    @endSuffix.setter
    def endSuffix(self, text):
        self._endSuffix = text

    def updateNames(self):
        self._niceOrigNames = [getShortName(name) for name in self._longOrigNames]
        self._newNames = self._niceOrigNames[:]

        if self._searchStr:
            self.searchReplace()
        if self._clearEndIntsFlag:
            self.clearEndInts()
        if self._hashName:
            self.setHashNewName()
        if self._prefix:
            self.addPrefix()
        if self._suffix:
            self.addSuffix()
        if self._setEndSuffixFlag:
            self.setEndSuffix()

    def setHashNewName(self):
        searchResultHash = re.search(r'(.*?)(#+)(.*)', self._hashName)
        searchResultDollar = re.search(r'(.*?)(\$+)(.*)', self._hashName)

        if searchResultHash:
            forwardStr = searchResultHash.group(1)
            paddingCount = len(searchResultHash.group(2))
            backwardStr = searchResultHash.group(3)
        elif searchResultDollar:
            forwardStr = searchResultDollar.group(1)
            paddingCount = len(searchResultDollar.group(2))
            backwardStr = searchResultDollar.group(3)
        else:
            pm.warning('Given name has no "#" or "$" character.')
            return

        if searchResultHash:
            for i in range(len(self._niceOrigNames)):
                self._newNames[i] = forwardStr + str(i + self._hashStartNum).zfill(paddingCount) + backwardStr
        elif searchResultDollar:
            charList = []
            for i in range(paddingCount):
                charList.append('A')

            for i in range(len(self._niceOrigNames)):
                # Repeat end character from 'A' to 'Z'
                addNum = i%26
                endChar = chr(ord(charList[-1]) + addNum)

                if i != 0 and endChar == 'A':
                    charList[-2] = chr(ord(charList[-2]) + 1)

                resultStr = ''.join(charList[:-1]) + endChar
                self._newNames[i] = forwardStr + resultStr + backwardStr

        if self._setEndSuffixFlag:
            self.setEndSuffix()

    def addPrefix(self):
        for i in range(len(self._niceOrigNames)):
            self._newNames[i] = self._prefix + self._newNames[i]

    def addSuffix(self):
        for i in range(len(self._niceOrigNames)):
            self._newNames[i] = self._newNames[i] + self._suffix

    def searchReplace(self):
        for i in range(len(self._niceOrigNames)):
            self._newNames[i] = self._newNames[i].replace(self._searchStr, self._replaceStr)

    def clearEndInts(self):
        for i in range(len(self._niceOrigNames)):
            self._newNames[i] = re.sub(r'(.+\D+)\d+$', r'\1', self._newNames[i])

    def setEndSuffix(self):
        for i in range(len(self._niceOrigNames)):
            if not pm.listRelatives(self._longOrigNames[i], ad=True):
                searchObj = re.search(r'.+\D+(\d+)', self._newNames[i])
                if searchObj:
                    self._newNames[i] = self._newNames[i].replace(searchObj.group(1), self._endSuffix)

    def apply(self):
        pm.undoInfo(openChunk=True)
        for i in range(len(self._longOrigNames)):
            self._longOrigNames[i].rename(self._newNames[i])
        pm.undoInfo(closeChunk=True)

    def reset(self):
        self._longOrigNames = []
        self._hashName = None
        self._prefix = None
        self._suffix = None
        self._searchStr = None
        self._replaceStr = None
        self._clearEndIntsFlag = False
        self.updateNames()


def getShortName(longName):
    return longName.split('|')[-1]
