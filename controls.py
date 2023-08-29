'''

'''
from PySide.QtGui import QToolButton, QPixmap, QCheckBox, QLabel
from PySide.QtCore import *

class borderLessButton(QToolButton):
    def __init__(self, caption, icon, parent=None):
        super(borderLessButton, self).__init__(parent)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.icon = QPixmap(icon)
        self.setIcon(self.icon)
        self.setIconSize(self.icon.rect().size())

        self.setText(caption)
        
        self.setStyleSheet("QToolButton { background:#232234; color: #636270; font-weight:bold; font-size:12pt; border:none;}")


class borderLessLCButton(QToolButton):
    def __init__(self, caption, icon, parent=None):
        super(borderLessLCButton, self).__init__(parent)

        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIcon(icon)
        self.setIconSize(icon.rect().size())

        self.setText(caption)

        self.setStyleSheet(
            "QToolButton { background:#232234; color: #636270; font-weight:bold; font-size:12pt; border:none;}")


class stdCheckBox(QCheckBox):
    def __init__(self, caption, initValue, size=None, parent=None):
        super(stdCheckBox, self).__init__(parent, caption)

        self.checkedImg = self.stdCheckBoxImgChecked(size)
        self.uncheckedImg = self.stdCheckBoxImgUnchecked(size)

        self.setStyleSheet("QCheckBox::indicator:checked { image: url(" + self.checkedImg + ");} QCheckBox::indicator:unchecked { image: url("+self.uncheckedImg+");}")
        self.setChecked(initValue)


    def stdCheckBoxImgChecked(self, size):
        checked = {
            16: "img/checked-checkbox-16.png",
            24: "img/checked-checkbox-24.png",
            32: "img/checked-checkbox-32.png",
            48: "img/checked-checkbox-48.png"
        }

        return checked.get(size, "img/checked-checkbox-16.png")

    def stdCheckBoxImgUnchecked(self, size):
        unChecked = {
            16: "img/unchecked-checkbox-16.fw.png",
            24: "img/unchecked-checkbox-24.fw.png",
            32: "img/unchecked-checkbox-32.fw.png",
            48: "img/unchecked-checkbox-48.fw.png"
        }

        return unChecked.get(size, "img/unchecked-checkbox-16.fw.png")


class numberLabel(QLabel):

    def __init__(self, icaption, lblFrmt, numFormat="{0:+6.2f}", width=None, parent=None):
        self.numberFormat = numFormat

        if (lblFrmt is None):
            self.lblFormat = "QLabel { background-color:none; color: #ffffff; font-weight: bold; font-size:18pt;}"
        else:
            self.lblFormat = lblFrmt
        caption = self.numberFormat.format(icaption)
        super(numberLabel, self).__init__(caption)
        self.setStyleSheet(self.lblFormat)
        self.setAlignment(Qt.AlignRight)
        if width is not None:
            self.setFixedWidth(width)

    def formatText(self, number):
        formatedText = self.numberFormat.format(number)
        self.setText(formatedText)





