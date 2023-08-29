from PySide.QtGui import QComboBox, QGroupBox, QRadioButton, QHBoxLayout, QButtonGroup
import platform
from lang import cLanguage

screenWidth = 800
screenHeight = 480

# Estilos comunes
lineEditStyle = "QLineEdit {background-color:#232234; color:white; height:20px; font-size:16pt;padding:3px;}\
												 QLineEdit:hover {border:2px solid white;}"

comboStyle = "QComboBox {   color: white; \
																		border: 1px solid white;    \
																		font-size: 14pt;        \
																		background-color:#232234;} \
											QComboBox QAbstractItemView {  \
																		color: white;  \
																		height: 30px;   \
																		background-color:#232234; \
																		padding: 3px;}  \
											QComboBox QAbstractItemView::item {   \
																		margin-top: 3px;    \
																		height: 40px;}"

labelStyle = "QLabel {color:white;font-size:14pt}"

radioStyle = "QRadioButton {color: white; font-size:14pt;} \
							QRadioButton::indicator::checked{ image: url(radioChecked.png); } \
							QRadioButton::indicator::unchecked{ image: url(radioUnchecked.png); } "

def develPlatform():
				# Primero veamos si estamos en linux o en windows
				if "Windows" in platform.platform():
						return True
				else:
						return False

def createHLCombo():
		combo = QComboBox()
		lang = cLanguage()
		combo.addItem(lang.tr("Active High"))
		combo.addItem(lang.tr("Active Low"))

		return combo

def createNIConfigGroup():
  lang = cLanguage()
				
  group = QGroupBox("")
  optionYes = QRadioButton(lang.tr("Normal"))
  optionYes.setStyleSheet(radioStyle)
  optionNo = QRadioButton(lang.tr("Inverted"))
  optionNo.setStyleSheet(radioStyle)
  box = QHBoxLayout()
  box.addWidget(optionYes)
  box.addWidget(optionNo)
  group.setLayout(box)

  return group

def createYesNoConfigGroup():
  lang = cLanguage()
				
  group = QGroupBox("")
  optionYes = QRadioButton(lang.tr("Yes"))
  optionYes.setStyleSheet(radioStyle)
  optionNo = QRadioButton(lang.tr("No"))
  optionNo.setStyleSheet(radioStyle)
  box = QHBoxLayout()
  box.addWidget(optionYes)
  box.addWidget(optionNo)
  group.setLayout(box)

  return group

def createIOConfigGroup1():
  lang = cLanguage()
				
  group = QButtonGroup()
  optionHigh = QRadioButton(lang.tr("Active High"))
  optionHigh.setStyleSheet(radioStyle)
  optionLow = QRadioButton(lang.tr("Active Low"))
  optionLow.setStyleSheet(radioStyle)
  optionDisabled = QRadioButton(lang.tr("Disabled"))
  optionDisabled.setStyleSheet(radioStyle)
  group.addButton( optionHigh )
  group.addButton( optionLow )
  group.addButton( optionDisabled )

  return group

def createIOConfigGroup():
  lang = cLanguage()
		
  group = QGroupBox("")
  optionHigh = QRadioButton(lang.tr("Active High"))
  optionHigh.setStyleSheet(radioStyle)
  optionHigh.setChecked( True )
  optionLow = QRadioButton(lang.tr("Active Low"))
  optionLow.setStyleSheet(radioStyle)
  optionDisabled = QRadioButton(lang.tr("Disabled"))
  optionDisabled.setStyleSheet(radioStyle)
  box = QHBoxLayout()
  box.addWidget(optionHigh)
  box.addWidget(optionLow)
  box.addWidget(optionDisabled)
  group.setLayout(box)

  return group

# rev20180315: Funciones de elctura de las claves
def getSettingsPassword():
  with open("cfg.txt") as f:
    cfg = f.readlines()

  for line in cfg:
    if "settingsPassword" in line:
      if "No" in line or "no" in line:
        return "No"
      else:
        return line.split(":")[1][0:4]

def getQuitPassword():
  with open("cfg.txt") as f:
    cfg = f.readlines()

  for line in cfg:
    if "quitPassword" in line:
      return line.split(":")[1][0:4]

def getGotoSpeed():
  with open("cfg.txt") as f:
    cfg = f.readlines()

  for line in cfg:
    if "gotoSpeed" in line:
      return line.split(":")[1][0:-1]

def getDefaultCyclesOn():
    with open("cfg.txt") as f:
        cfg = f.readlines()

    for line in cfg:
        if "CiclosOn" in line and "1" in line:
            return 1
        
    return 0
    
def getLimiteCiclos():
  with open("cfg.txt") as f:
    cfg = f.readlines()

  for line in cfg:
    if "LimiteCiclos" in line:
      return line.split(":")[1][0:-1]

def getFresaActiveLow():
  with open("cfg.txt") as f:
    cfg = f.readlines()

  for line in cfg:
    if "fresaActiveLow" in line:
      fields= line.split(":")
      if "No" in fields[1]:
        print("fresaActiveLow No")
        return 0
      else:
        print("fresaActiveLow Si")
        return 1
  
