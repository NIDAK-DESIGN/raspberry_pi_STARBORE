# -*- coding: cp1252 -*-
import ConfigParser
import re
from basicFuncs import *


class ControlFile:

    # Configuration control file
    config = ConfigParser.RawConfigParser()
    config.optionxform = str

    # Number of Y values
    DEFAULT_FILENAME = "control"
    DEFAULT_EXTENSION = "tap"
    DEFAULT_DIRECTORY = "/cncNetwork/"
    YROW_COUNT = 12
    YCOLUMN_COUNT = 2
    YREFERENCE_STUB = "agujero_n"
    DEPTH_STD = 1
    DEPTH_DEEP = 2
    GLUE_STUB = "glue_code"
    PTGLUE_STUB = "Ptglue"
    PTINSERT_STUB = "Ptinsert"
    OFFSETGLUE_STUB = "offsetGlue"
    OFFSETINSERT_STUB = "offsetInsert"
    YREFERENCE_SECTION = "Y References"
    YGLUE_SECTION = "Glue References"
    YPLUG_SECTION = "Plug References"
    YDEPTH_SECTION = "Depth References"
    GENERAL_SECTION = "General"
    KEY_FILE_START_CODE = "FileStartCode"
    KEY_FILE_SWITCH_CODE = "FileSwitchCode"
    KEY_FILE_CHANGE_CODE = "FileChangeCode"
    KEY_FILE_FINNISH_CODE = "FileFinnishCode"
    KEY_FILE_ACTION_CODE = "FileActionCode"
    KEY_FILE_GLUE_CODE = "FileGlueCode"
    KEY_FILE_PLUG_CODE = "FilePlugCode"
    KEY_FILE_STD_DEPTH = "FileStdDepth"
    KEY_FILE_DEEP_DEPTH = "FileDeepDepth"
    KEY_PUT_GLUE = "PutGlue"
    KEY_CLONE = "Clone"
    KEY_PLUG = "Plug"
    KEY_PT_GLUE = "PTGlue"
    KEY_PT_INSERT = "PTInsert"
    KEY_OFFSET_GLUE = "OffsetGlue"
    KEY_OFFSET_INSERT = "OffsetInsert"
    KEY_DISABLE_PLUG = "DisablePlug"

    def __init__(self):

        self.lastSavedTAPFile = ""
        # Valores de referencia de eje Y
        self.yReferences = []
        self.yReferencesPlug = []
        self.yReferencesGlue = []
        self.yReferencesDepth = []
        self.putGlue = False
        self.clone = False
        self.plug = False
        self.pTGlue = 0
        self.pTInsert = 0
        self.offsetGlue = 0
        self.offsetInsert = 0
        self.disablePlug = False

        self.reset = False

        # Inicializar los valores de referencia de eje Y

        for i in range(0, self.YROW_COUNT):
            emptyRowR = []
            for i in range(0, self.YCOLUMN_COUNT):
                emptyRowR.append(0)

            self.yReferences.append(emptyRowR)

            emptyRowP = []
            for i in range(0, self.YCOLUMN_COUNT):
                emptyRowP.append(False)
            self.yReferencesPlug.append(emptyRowP)

            emptyRowD = []
            for i in range(0, self.YCOLUMN_COUNT):
                emptyRowD.append(self.DEPTH_STD)
            self.yReferencesDepth.append(emptyRowD)

        self.startCodeFile = ""
        self.finnishCodeFile = ""
        self.actionCodeFile = ""
        self.glueCodeFile = ""
        self.plugCodeFile = ""
        self.switchXCodeFile = ""
        self.changeSCodeFile = ""
        self.stdDepthCodeFile = ""
        self.deepDepthCodeFile = ""


    #
    # readFile( self)
    #
    # Read configuration of control sequence from config file
    #
    def readFile(self):

        self.config.read("etc/control.cfg")

        print("Start: Read etc/control.cfg")

        for name, value in self.config.items(self.YREFERENCE_SECTION):
            ndx = int(name[2:]) - 1
            column = self.columnVal(name[1:2])

            self.yReferences[ndx][column] = float(value)

        for name, value in self.config.items(self.YGLUE_SECTION):
            ndx = int(name[2:]) - 1
            self.yReferencesGlue[ndx] = (value.upper() in ["TRUE", "T", "YES", "Y"])

        for name, value in self.config.items(self.YPLUG_SECTION):
            ndx = int(name[2:]) - 1
            column = self.columnVal(name[1:2])

            self.yReferencesPlug[ndx][column] = value.upper() in ["TRUE", "T", "YES", "Y"]

        for name, value in self.config.items(self.YDEPTH_SECTION):
            ndx = int(name[2:]) - 1
            column = self.columnVal(name[1:2])

            self.yReferencesDepth[ndx][column] = int(value)

        if (self.config.has_section(self.GENERAL_SECTION)):

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_START_CODE)):
                self.startCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_START_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_START_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_SWITCH_CODE)):
                self.switchXCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_SWITCH_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_SWITCH_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_CHANGE_CODE)):
                self.changeSCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_CHANGE_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_CHANGE_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_FINNISH_CODE)):
                self.finnishCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_FINNISH_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_FINNISH_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_ACTION_CODE)):
                self.actionCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_ACTION_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_ACTION_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_GLUE_CODE)):
                self.glueCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_GLUE_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_GLUE_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_PLUG_CODE)):
                self.plugCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_PLUG_CODE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_PLUG_CODE, "")

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_STD_DEPTH)):
                self.stdDepthCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_STD_DEPTH)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_STD_DEPTH, self.stdDepthCodeFile)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_FILE_DEEP_DEPTH)):
                self.deepDepthCodeFile = self.config.get(self.GENERAL_SECTION, self.KEY_FILE_DEEP_DEPTH)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_FILE_DEEP_DEPTH, self.deepDepthCodeFile)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_PUT_GLUE)):
                self.putGlue = self.config.getboolean(self.GENERAL_SECTION, self.KEY_PUT_GLUE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_PUT_GLUE, self.putGlue)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_CLONE)):
                self.clone = self.config.getboolean(self.GENERAL_SECTION, self.KEY_CLONE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_CLONE, self.clone)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_PLUG)):
                self.plug = self.config.getboolean(self.GENERAL_SECTION, self.KEY_PLUG)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_PLUG, self.plug)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_PT_GLUE)):
                self.pTGlue = self.config.getfloat(self.GENERAL_SECTION, self.KEY_PT_GLUE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_PT_GLUE, self.pTGlue)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_PT_INSERT)):
                self.pTInsert = self.config.getfloat(self.GENERAL_SECTION, self.KEY_PT_INSERT)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_PT_INSERT, self.pTInsert)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_OFFSET_GLUE)):
                self.offsetGlue = self.config.getfloat(self.GENERAL_SECTION, self.KEY_OFFSET_GLUE)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_OFFSET_GLUE, self.offsetGlue)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_OFFSET_INSERT)):
                self.offsetInsert = self.config.getfloat(self.GENERAL_SECTION, self.KEY_OFFSET_INSERT)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_OFFSET_INSERT, self.offsetInsert)

            if (self.config.has_option(self.GENERAL_SECTION, self.KEY_DISABLE_PLUG)):
                self.disablePlug = self.config.getboolean(self.GENERAL_SECTION, self.KEY_DISABLE_PLUG)
            else:
                self.config.set(self.GENERAL_SECTION, self.KEY_DISABLE_PLUG, self.disablePlug)

        else:
            self.config.add_section(self.GENERAL_SECTION)

        print("End: Read etc/control.cfg")

    def alternateCol(self, col):
        altCol = {
            1: 0,
            0: 1,
        }

        return altCol.get(col, -1)

    def alternateKeyCol(self, col):
        altCol = {
            1: 2,
            2: 1,
        }

        return altCol.get(col, -1)

    def columnVal(self, strColumn):
        result = 0
        if (strColumn is "A"):
            pass
            # result = 0
        elif (strColumn is "B"):
            result = 1

        return result

    def columnStr(self, valColumn):
        result = ""

        if (valColumn is 1):
            result = "A"
        elif (valColumn is 2):
            result = "B"

        return result

    #
    # writeFile( self)
    #
    # Write configuration of control sequence to config file
    #
    def writeFile(self):

        print("Begin: Write etc/control.cfg")

        with open("etc/control.cfg", "wb") as configfile:
            self.config.write(configfile)
            configfile.close()

        print("End: Write etc/control.cfg")

    #
    # setReferenceValue(self, ndx, value)
    #
    # Establecer (set) valor de una de las referencias del eje Y
    #
    def setReferenceValue(self, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1
        if ((rowNdx >= 0 and rowNdx <= self.YROW_COUNT) and (colNdx >= 0 and colNdx <= self.YCOLUMN_COUNT)):
            self.yReferences[rowNdx][colNdx] = value
            key = "Y" + self.columnStr(colNdx) + str(rowNdx).zfill(2)
            self.config.set(self.YREFERENCE_SECTION, key, value)

            if self.clone:
                altColNdx = self.alternateCol(colNdx)
                self.yReferences[rowNdx][altColNdx] = value
                key = "Y" + self.columnStr(altColNdx) + str(rowNdx).zfill(2)
                self.config.set(self.YREFERENCE_SECTION, key, value)

    #
    # getReferenceValue(self, ndx)
    #
    # Obtener (get) valor de una de las referencias del eje Y
    #
    def getReferenceValue(self, ndx, column):
        ndx -= 1
        column -= 1
        value = 0.0
        if ((ndx >= 0 and ndx <= self.YROW_COUNT) and (column >= 0 and column <= self.YCOLUMN_COUNT)):
            value = self.yReferences[ndx][column]
        return value

    def delReferenceValue(self, row, col):
        colNdx = col - 1
        for i in range(row - 1, self.YROW_COUNT - 1):
            self.yReferences[i][colNdx] = self.yReferences[i+1][colNdx]
        self.yReferences[self.YROW_COUNT - 1][colNdx] = 0

        if self.clone:
            altColNdx = self.alternateCol(colNdx)
            for i in range(row - 1, self.YROW_COUNT - 1):
                self.yReferences[i][altColNdx] = self.yReferences[i+1][altColNdx]
            self.yReferences[self.YROW_COUNT - 1][altColNdx] = 0

    def setAllReferenceValues(self, value):
        for i in range(0, self.YROW_COUNT):
            for j in range(0, self.YCOLUMN_COUNT):
                self.yReferences[i][j] = value

            # Guardar valor en Config
            key = "Y" + self.columnStr(j) + str(i+1).zfill(2)
            self.config.set(self.YREFERENCE_SECTION, key, value)

    def cloneReferenceValues(self):
        for i in range(0, self.YROW_COUNT):
            value = self.yReferences[i][0]
            self.yReferences[i][1] = value
            # Guardar valor en Config
            key = "Y" + self.columnStr(2) + str(i+1).zfill(2)
            self.config.set(self.YREFERENCE_SECTION, key, value)

    def isReferenceEditable(self, row, col):
        result = False

        # Si se estï¿½ clonando no se puede editar columna 1
        if self.clone and col == 1:
            return result

        rowNdx = row - 1
        colNdx = col - 1

        if (colNdx >= 0 and colNdx < self.YCOLUMN_COUNT):
            if (rowNdx == 0):
                result = True
            elif ((rowNdx > 0 and rowNdx < self.YROW_COUNT) and (self.yReferences[rowNdx - 1][colNdx] != 0)):
                result = True

        return result

    def validateReferenceValue(self, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1
        result = 0

        if ((rowNdx >= 0 and rowNdx < self.YROW_COUNT) and (colNdx >= 0 and colNdx < self.YCOLUMN_COUNT)):
            if (value == 0 and self.yReferences[rowNdx + 1][colNdx] != 0):
                result = 1
            elif (self.yReferences[rowNdx - 1][colNdx] > value):
                result = 2
            elif (value != 0 and self.yReferences[rowNdx + 1][colNdx] != 0 and self.yReferences[rowNdx + 1][colNdx] < value):
                result = 3
        return result

    def findInsertPosReference(self, col, value):
        colNdx = col - 1
        result  = 0

        for i in range(self.YROW_COUNT - 1, -1, -1):
            if (self.yReferences[i][colNdx] != 0 and self.yReferences[i][colNdx] < value):
                result = i + 1
                break

        return result

    def findReplacePosReference(self, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1
        result  = 0
        rowFound = False
        firstNonZero = -1

        for i in range(self.YROW_COUNT - 1, -1, -1):
            if (self.yReferences[i][colNdx] != 0):
                if (firstNonZero == -1):
                    firstNonZero = i

                if ( i != rowNdx and self.yReferences[i][colNdx] > value and self.yReferences[i - 1][colNdx] < value):
                    result = i - 1
                    rowFound = True
                    break

        if (not rowFound):
            result = firstNonZero

        return result

    def insertReferenceValue(self, pos, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1

        for i in range(rowNdx, pos, -1):
            self.yReferences[i][colNdx] = self.yReferences[i - 1][colNdx]
            self.yReferencesPlug[i][colNdx] = self.yReferencesPlug[i - 1][colNdx]

        self.yReferences[pos][colNdx] = value
        self.yReferencesPlug[pos][colNdx] = self.plug

        if (self.clone):
            altColNdx = self.alternateCol(colNdx)
            for i in range(rowNdx, pos, -1):
                self.yReferences[i][altColNdx] = self.yReferences[i - 1][altColNdx]
                self.yReferencesPlug[i][altColNdx] = self.yReferencesPlug[i - 1][altColNdx]

            self.yReferences[pos][altColNdx] = value
            self.yReferencesPlug[pos][altColNdx] = self.plug

    def replaceReferenceValue(self, pos, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1

        for i in range(rowNdx, pos):
            self.yReferences[i][colNdx] = self.yReferences[i + 1][colNdx]
            self.yReferencesPlug[i][colNdx] = self.yReferencesPlug[i + 1][colNdx]

        self.yReferences[pos][colNdx] = value
        self.yReferencesPlug[pos][colNdx] = self.plug

        if (self.clone):
            altColNdx = self.alternateCol(colNdx)

            for i in range(rowNdx, pos):
                self.yReferences[i][altColNdx] = self.yReferences[i + 1][altColNdx]
                self.yReferencesPlug[i][altColNdx] = self.yReferencesPlug[i + 1][altColNdx]

            self.yReferences[pos][altColNdx] = value
            self.yReferencesPlug[pos][altColNdx] = self.plug

    def getReferenceDepthValue(self, row, col):
        rowNdx = row - 1
        colNdx = col - 1
        value = 1
        if ((rowNdx >= 0 and rowNdx <= self.YROW_COUNT) and (colNdx >= 0 and colNdx <= self.YCOLUMN_COUNT)):
            value = self.yReferencesDepth[rowNdx][colNdx]
        return value

    def setReferenceDepthValue(self, row, col, value):
        rowNdx = row - 1
        colNdx = col - 1

        if ((rowNdx >= 0 and rowNdx <= self.YROW_COUNT) and (colNdx >= 0 and colNdx <= self.YCOLUMN_COUNT)):
            self.yReferencesDepth[rowNdx][colNdx] = value
            key = "Y" + self.columnStr(colNdx) + str(rowNdx).zfill(2)
            self.config.set(self.YDEPTH_SECTION, key, value)

            if self.clone:
                altColNdx = self.alternateCol(colNdx)
                self.yReferencesDepth[rowNdx][altColNdx] = value
                key = "Y" + self.columnStr(altColNdx) + str(rowNdx).zfill(2)
                self.config.set(self.YDEPTH_SECTION, key, value)

    def cloneReferenceDepthValues(self):
        for i in range(0, self.YROW_COUNT):
            value = self.yReferencesDepth[i][0]
            self.yReferencesDepth[i][1] = value
            # Guardar valor en Config
            key = "Y" + self.columnStr(2) + str(i+1).zfill(2)
            self.config.set(self.YDEPTH_SECTION, key, value)

    def switchReferenceDepthValue(self, row, col):
        rowNdx = row - 1
        colNdx = col - 1

        if ((rowNdx >= 0 and rowNdx <= self.YROW_COUNT) and (colNdx >= 0 and colNdx <= self.YCOLUMN_COUNT)):
            value = self.nextDepthValue(self.yReferencesDepth[rowNdx][colNdx])
            self.yReferencesDepth[rowNdx][colNdx] = value
            key = "Y" + self.columnStr(colNdx) + str(rowNdx).zfill(2)
            self.config.set(self.YDEPTH_SECTION, key, value)

            if self.clone:
                altColNdx = self.alternateCol(colNdx)
                self.yReferencesDepth[rowNdx][altColNdx] = value
                key = "Y" + self.columnStr(altColNdx) + str(rowNdx).zfill(2)
                self.config.set(self.YDEPTH_SECTION, key, value)

    def setAllReferenceDepthValues(self, value):
        for i in range(0, self.YROW_COUNT):
            for j in range(0, self.YCOLUMN_COUNT):
                self.yReferencesDepth[i][j] = value

            # Guardar valor en Config
            key = "Y" + self.columnStr(j) + str(i+1).zfill(5)
            self.config.set(self.YDEPTH_SECTION, key, value)

    def nextDepthValue(self, value):
        nextValue = {
            self.DEPTH_STD: self.DEPTH_DEEP,
            self.DEPTH_DEEP: self.DEPTH_STD
        }

        return nextValue.get(value, self.DEPTH_STD)

    def getPutGlueValue(self):
        return self.putGlue

    def setPutGlueValue(self, value):
        self.putGlue = value

    def switchPutGlueValue(self):
        self.putGlue = not self.putGlue
        self.config.set(self.GENERAL_SECTION, self.KEY_PUT_GLUE, self.putGlue)

    #
    # setReferenceValue(self, ndx, value)
    #
    # Establecer (set) valor de una de las referencias del eje Y
    #
    def setReferencePlugValue(self, ndx, column, value):
        i = ndx - 1
        j = column - 1
        if ((i >= 0 and i <= self.YROW_COUNT) and (j >= 0 and j <= self.YCOLUMN_COUNT)):
            self.yReferencesPlug[i][j] = value

            key = "Y" + self.columnStr(column) + str(ndx).zfill(2)
            self.config.set(self.YPLUG_SECTION, key, value)

    #
    # getReferencePlugValue(self, ndx)
    #
    # Obtener (get) valor de una de las referencias del eje Y
    #
    def getReferencePlugValue(self, ndx, column):
        ndx -= 1
        column -= 1
        value = False
        if ((ndx >= 0 and ndx <= self.YROW_COUNT) and (column >= 0 and column <= self.YCOLUMN_COUNT)):
            value = self.yReferencesPlug[ndx][column]
        return value

    def delReferencePlugValue(self, row, col):
        colNdx = col - 1
        for i in range(row - 1, self.YROW_COUNT - 1):
            self.yReferencesPlug[i][colNdx] = self.yReferencesPlug[i+1][colNdx]
        self.yReferencesPlug[self.YROW_COUNT - 1][colNdx] = 0

        if self.clone:
            altColNdx = self.alternateCol(colNdx)
            for i in range(row - 1, self.YROW_COUNT - 1):
                self.yReferencesPlug[i][altColNdx] = self.yReferencesPlug[i+1][altColNdx]
            self.yReferencesPlug[self.YROW_COUNT - 1][altColNdx] = 0

    def cloneReferencePlugValues(self):
        for i in range(0, self.YROW_COUNT):
            value = self.yReferencesPlug[i][0]
            self.yReferencesPlug[i][1] = value
            # Guardar valor en Config
            key = "Y" + self.columnStr(2) + str(i+1).zfill(2)
            self.config.set(self.YPLUG_SECTION, key, value)

    def switchReferencePlugValue(self, row, col):
        rowNdx = row - 1
        colNdx = col - 1
        if ((rowNdx >= 0 and rowNdx <= self.YROW_COUNT) and (colNdx >= 0 and colNdx <= self.YCOLUMN_COUNT)):
            value = not self.yReferencesPlug[rowNdx][colNdx]
            self.yReferencesPlug[rowNdx][colNdx] = value
            key = "Y" + self.columnStr(col) + str(row).zfill(2)
            self.config.set(self.YPLUG_SECTION, key, value)

            if self.clone:
                altColNdx = self.alternateCol(colNdx)
                altCol = self.alternateKeyCol(col)

                value = not self.yReferencesPlug[rowNdx][altColNdx]
                self.yReferencesPlug[rowNdx][altColNdx] = value
                key = "Y" + self.columnStr(altCol) + str(row).zfill(2)
                self.config.set(self.YPLUG_SECTION, key, value)

    def isAllReferencePlugValue(self):
        result = True
        for i in range(0, self.YROW_COUNT):
            for j in range(0, self.YCOLUMN_COUNT):
                if (not self.yReferencesPlug[i][j]):
                    result = False
                    break
        return result

    def setAllReferencePlugValues(self, value):
        self.plug = value

        for i in range(0, self.YROW_COUNT):
            for j in range(0, self.YCOLUMN_COUNT):
                self.yReferencesPlug[i][j] = value
                key = "Y" + self.columnStr(j) + str(i+1).zfill(2)
                self.config.set(self.YPLUG_SECTION, key, value)

    def getPTGlueValue(self):
        return self.pTGlue

    def setPTGlueValue(self, value):
        self.pTGlue = value
        self.config.set(self.GENERAL_SECTION, self.KEY_PT_GLUE, value)


    def getPTInsertValue(self):
        return self.pTInsert

    def setPTInsertValue(self, value):
        self.pTInsert = value
        self.config.set(self.GENERAL_SECTION, self.KEY_PT_INSERT, value)

    def getOffsetGlueValue(self):
        return self.offsetGlue

    def setOffsetGlueValue(self, value):
        self.offsetGlue = value
        self.config.set(self.GENERAL_SECTION, self.KEY_OFFSET_GLUE, value)

    def getOffsetInsertValue(self):
        return self.offsetInsert

    def setOffsetInsertValue(self, value):
        self.offsetInsert = value
        self.config.set(self.GENERAL_SECTION, self.KEY_OFFSET_INSERT, value)

    #NIDAK 20200910 Modificaciones al generador de
    #codígo
    def generateCodeFileEditor(self, filename=None, array=None, exitM1 = False, exitM2 = False):
        if (filename is None):
            filename = self.DEFAULT_FILENAME + "." + self.DEFAULT_EXTENSION

        # Abrir ficheros para generar fichero TAP
        # TODO: Volver a guardar dentro de directorio TAP
        if (not develPlatform() ):
            #filename = "/media/pi/" + self.DEFAULT_FILENAME + "." + self.DEFAULT_EXTENSION
            filename = self.DEFAULT_DIRECTORY + filename

        print("Begin: Write " + filename)
        fControl = open(filename, "w")

        # Transferir codigo Start a fichero TAP de control
        fStart = open(self.startCodeFile, "r")

        firstLine = ""
        for line in fStart:
            if firstLine == "":
                firstLine = line

            # Coloco el codigo de DX si hiciera falta
            if exitM1 and line.find("DX=") != -1:
                fControl.write(line)
                continue

            #Antes del M03 coloco el codigo de DX2
            if line.find("M03") != -1:
                if exitM2:
                    fControl.write(firstLine.replace('DX', 'DX2'))

            if line.find("DX=") == -1:
                fControl.write(line)
        fStart.close()

        count = len(array)
        for i in range(0, count):
            fControl.write("G01 Y" + str(array[i][0]) + " F20000\n")
            if array[i][2] == '1':
                fControl.write("M7\n")
                fControl.write("G04 " + array[i][1] + "\n")
                fControl.write("M9\n")
                #array[i][1]
            else :
                fControl.write("M20\n")
                if array[i][1] == 'P1':
                   fControl.write("G04 " + "P3" + "\n")
                else :
                    fControl.write("G04 " + "P5" + "\n")
                fControl.write("M21\n")

        fControl.write("M05")
        fControl.write("\n")
        fControl.write("G01 Y-10 F25000")

        fControl.close()
        self.lastSavedTAPFile = filename
        print("End: Write " + filename)

    #Final de generateCodeFileEditor

    def generateCodeFile(self, filename=None):

        if (filename is None):
            filename = self.DEFAULT_FILENAME + "." + self.DEFAULT_EXTENSION

        #try:
        # Abrir ficheros para generar fichero TAP
        # TODO: Volver a guardar dentro de directorio TAP
        if (not develPlatform() ):
            #filename = "/media/pi/" + self.DEFAULT_FILENAME + "." + self.DEFAULT_EXTENSION
            filename = self.DEFAULT_DIRECTORY + filename

        print("Begin: Write " + filename)

        fControl = open(filename, "w")

        # Recover and save action lines
        linesAction = []
        fAction = open(self.actionCodeFile, "r")
        for line in fAction:
            linesAction.append(line)
        fAction.close()

        # Recover and save glue lines
        linesGlue = []
        fGlue = open(self.glueCodeFile, "r")
        for line in fGlue:
            linesGlue.append(line)
        fGlue.close()

        # Recover and save plug lines
        linesPlug = []
        fPlug = open(self.plugCodeFile, "r")
        for line in fPlug:
            linesPlug.append(line)
        fPlug.close()

        # Recover and save Std Depth lines
        linesStdDepth = []
        fStdDepth = open(self.stdDepthCodeFile, "r")
        for line in fStdDepth:
            linesStdDepth.append(line)
        fStdDepth.close()

        # Recover and save Deep Depth lines
        linesDeepDepth = []
        fDeepDepth = open(self.deepDepthCodeFile, "r")
        for line in fDeepDepth:
            linesDeepDepth.append(line)
        fStdDepth.close()

        #
        # START:  generating TAP file
        #

        # Transferir codigo Start a fichero TAP de control
        fStart = open(self.startCodeFile, "r")
        for line in fStart:
            fControl.write(line)
        fStart.close()
        fControl.write("\n")

        # Store value of current Depth
        currentDepth = self.DEPTH_STD

        # Escribir codigo para cada referencia de YAn y Primera columna
        column = 0
        for i in range(0, self.YROW_COUNT):
            reference = self.yReferences[i][column]
            if reference == 0.0:
                break
            else:
                # If current depth is not Std, include MCode to switch to DEEP
                if self.yReferencesDepth[i][column] != currentDepth:
                    if currentDepth == self.DEPTH_STD:
                        for line in linesStdDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    else:
                        for line in linesDeepDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    currentDepth = self.yReferencesDepth[i][column]

                # Incorporar codigo de accion (agujeros)
                for line in linesAction:
                    codigo = self.parseCodeLine(line, reference)
                    fControl.write(codigo)

                # Incorporar codigo de Cola y Tarugo (si procede)
                if (self.yReferencesPlug[i][column]):

                    # Incorporar codigo de Tarugo (si procede)
                    for line in linesPlug:
                        print("Debug: linea")
                        print(len(line))
                        print(line)
                        if (line.strip() == self.GLUE_STUB):
                            if (self.putGlue):
                                # Incorporar codigo de Cola (si procede)
                                for line in linesGlue:
                                    codigo = self.parseCodeLine(line, reference)
                                    fControl.write(codigo)
                            # else: Se ignora la lï¿½nea
                        else:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)

        # Transferir codigo Switch X a fichero TAP de control
        fSwitch = open(self.switchXCodeFile, "r")
        for line in fSwitch:
            fControl.write(line)
        fSwitch.close()
        fControl.write("\n")

        # Escribir codigo para cada referencia de YAn y Segunda columna
        column = 1
        for i in range(self.YROW_COUNT - 1, -1, -1):
            reference = self.yReferences[i][column]
            if reference == 0.0:
                continue
            else:
                # If current depth is not Std, include MCode to switch to DEEP
                if self.yReferencesDepth[i][column] != currentDepth:
                    if currentDepth == self.DEPTH_STD:
                        for line in linesStdDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    else:
                        for line in linesDeepDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    currentDepth = self.yReferencesDepth[i][column]

                # Incorporar codigo de accion (agujeros)
                for line in linesAction:
                    codigo = self.parseCodeLine(line, reference)
                    fControl.write(codigo)

                # Incorporar codigo de Cola y Tarugo (si procede)
                if (self.yReferencesPlug[i][column]):

                    # Incorporar codigo de Tarugo
                    for line in linesPlug:
                        print("Debug: linea")
                        print(len(line))
                        print(line)
                        if (line.strip() == self.GLUE_STUB):
                            if (self.putGlue):
                                # Incorporar codigo de Cola
                                for line in linesGlue:
                                    codigo = self.parseCodeLine(line, reference)
                                    fControl.write(codigo)
                            # else: Se ignora la lï¿½nea
                        else:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)

        # Transferir codigo Change pieces a fichero TAP de control
        fChange = open(self.changeSCodeFile, "r")
        for line in fChange:
            fControl.write(line)
        fChange.close()
        fControl.write("\n")

        # Escribir codigo para cada referencia de YAn y Segunda columna
        column = 1
        for i in range(0, self.YROW_COUNT):
            reference = self.yReferences[i][column]
            if reference == 0.0:
                break
            else:
                # If current depth is not Std, include MCode to switch to DEEP
                if self.yReferencesDepth[i][column] != currentDepth:
                    if currentDepth == self.DEPTH_STD:
                        for line in linesStdDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    else:
                        for line in linesDeepDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    currentDepth = self.yReferencesDepth[i][column]

                # Incorporar codigo de accion (agujeros)
                for line in linesAction:
                    codigo = self.parseCodeLine(line, reference)
                    fControl.write(codigo)

                # Incorporar codigo de Cola y Tarugo (si procede)
                if (self.yReferencesPlug[i][column]):

                    # Incorporar codigo de Tarugo
                    for line in linesPlug:
                        print("Debug: linea")
                        print(len(line))
                        print(line)
                        if (line.strip() == self.GLUE_STUB):
                            if (self.putGlue):
                                # Incorporar codigo de Cola
                                for line in linesGlue:
                                    codigo = self.parseCodeLine(line, reference)
                                    fControl.write(codigo)
                            # else: Se ignora la lï¿½nea
                        else:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)

        # Transferir codigo Switch X a fichero TAP de control
        fSwitch = open(self.switchXCodeFile, "r")
        for line in fSwitch:
            fControl.write(line)
        fSwitch.close()
        fControl.write("\n")

        # Escribir codigo para cada referencia de YAn y Primera columna
        column = 0
        for i in range(self.YROW_COUNT -1, -1, -1):
            reference = self.yReferences[i][column]
            if reference == 0.0:
                continue
            else:
                # If current depth is not Std, include MCode to switch to DEEP
                if self.yReferencesDepth[i][column] != currentDepth:
                    if currentDepth == self.DEPTH_STD:
                        for line in linesStdDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    else:
                        for line in linesDeepDepth:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)
                    currentDepth = self.yReferencesDepth[i][column]

                # Incorporar codigo de accion (agujeros)
                for line in linesAction:
                    codigo = self.parseCodeLine(line, reference)
                    fControl.write(codigo)

                # Incorporar codigo de Cola y Tarugo (si procede)
                if (self.yReferencesPlug[i][column]):

                    # Incorporar codigo de Tarugo
                    for line in linesPlug:
                        print("Debug: linea")
                        print(len(line))
                        print(line)
                        if (line.strip() == self.GLUE_STUB):
                            if (self.putGlue):
                                # Incorporar codigo de Cola
                                for line in linesGlue:
                                    codigo = self.parseCodeLine(line, reference)
                                    fControl.write(codigo)
                            # else: Se ignora la lï¿½nea
                        else:
                            codigo = self.parseCodeLine(line, reference)
                            fControl.write(codigo)

        # Transferir codigo Finnish a fichero TAP de control
        fFinnish = open(self.finnishCodeFile, "r")
        for line in fFinnish:
            fControl.write(line)
        fFinnish.close()
        fControl.write("\n")


        fControl.close()
        self.lastSavedTAPFile = filename

        #except IOError:
            #print("Error ficheros")
            # userInfo = QMessageBox.question(self, "VERTIMAQ-CNC",
            #                             "<font color='#ffffff'>" + self.lang.tr("Error reading configuration file."),
            #                             QMessageBox.Ok)
        #return

        print("End: Write " + filename)

    def parseCodeLine(self, line, reference):

        # Reemplazar Offsets tanto de cola como de tarugo
        line = line.replace(self.OFFSETGLUE_STUB, str(self.offsetGlue))
        line = line.replace(self.OFFSETINSERT_STUB, str(self.offsetInsert))

        # Reemplazar referencias a posiciones Y
        prs = re.compile(self.YREFERENCE_STUB+'[+-]*[0-9]*\.*[0-9]*\s')
        finalReplace = False

        matches = prs.findall(line)
        for match in matches:

            print("Pattern = " + match)
            l = len(self.YREFERENCE_STUB) + 1

            if (len(match) == l):
                finalReplace = True
            else:
                delta = float(match[l:])
                dist = reference + delta;
                line = line.replace(match, str(dist)+" ")

                print("Delta = " + str(delta))

        if (finalReplace):
            line = line.replace(self.YREFERENCE_STUB, str(reference))

        # Reemplazar PTGlue y PTInsert
        line = line.replace(self.PTGLUE_STUB, str(self.pTGlue))
        line = line.replace(self.PTINSERT_STUB, str(self.pTInsert))

        return line



