# -*- coding: cp1252 -*-
import sys
import time
from PySide.QtGui import *
from PySide.QtCore import *
from coms import CNC
from PySide.phonon import Phonon
from controls import borderLessButton
from maintDialogs import dlgInputTest, dlgOutputTest, dlgInfo, dlgTools
from tunningDialogs import dlgGralParams
from motorDialogs import dlgMotorTunning
from homeDialog import dlgHomeConfig
from jog import dlgJog
from basicFuncs import *
import threading
from basicDialogs import dlgInputNumber
from mainDialogs import *

def main():

    try:
        
        app = QApplication(sys.argv)
        pixmap = QPixmap("splash.png")
        splash = QSplashScreen(pixmap)
        
        if develPlatform() == True:
            splash.show()
            splash.move(50, 50)
        else:
            splash.showFullScreen()
            splash.move(0, 0)
        app.processEvents()

        time.sleep(2)

        # copdebug rev20170801 ahora no hay cnc
        cnc = CNC()
        cnc.readStatus()
        cnc.printStatus()
        uuid = cnc.getUUID()
        
        window = MainWindow(cnc)
        
        splash.finish(window)
        return app.exec_()

    #except NameError:
    #    print("Name error:", sys.exc_info()[1])

    except SystemExit:
        print("Closing window...")

    #except Exception:
    #    print(sys.exc_info()[1])

main()
