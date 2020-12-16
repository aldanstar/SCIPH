# -------------------------------------------------------------------------------
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
from PySide2.QtWidgets import QDockWidget, QMainWindow, QAbstractButton, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PySide2.QtCore import QObject, QSize, QPointF, QPropertyAnimation, QEasingCurve, Property, Slot, Qt
from PySide2.QtGui import  QPainter, QPalette, QLinearGradient, QGradient, QColor, QFont, QFontMetrics
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator

class DockWidget(QDockWidget):
    def __init__ ( self, parent = None,  root = None, title=''):
        QDockWidget.__init__(self, parent)
        self.parent = parent
        self.root = root
        self.gui_init()
        self.setWindowTitle(title)

    def setTitle(self, title):
        self.setWindowTitle(title)

    def gui_init(self):

        self.layout=QHBoxLayout()
        self.MainWindow=QMainWindow()
        self.layout.addWidget(self.MainWindow)
        self.setLayout(self.layout)

        self.setAllowedAreas(Qt.LeftDockWidgetArea |
                           Qt.RightDockWidgetArea)

class inputWithButton(QWidget):
    def __init__(self, parent = None, RegEx = None, title='prop', label='button', button_func=None, iptype = False):
        QWidget.__init__(self, parent)
        self.__title = title
        self.__label = label
        self.__button_func = button_func

        if iptype: RegEx = '(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])'
        self.RegEx = QRegExp("^" + RegEx + "\\." + RegEx + "\\." + RegEx + "\\." + RegEx + "$") if iptype else RegEx
        self.gui_init()

    def gui_init(self):
        layout=QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        label = QLabel()
        label.setText(self.__title)

        ipValidator = QRegExpValidator(self.RegEx, self)

        self.__text=QLineEdit()
        if self.RegEx: self.__text.setValidator(ipValidator)

        button = QPushButton()
        button.setText(self.__label)

        button_func =  lambda : self.__button_func(self)
        button.pressed.connect(button_func)

        layout.addWidget(label)
        layout.addWidget(self.__text)
        layout.addWidget(button)

    @property
    def text(self):
        return self.__text.text()

    def setText(self, text):
        self.__text.setText(text)

class SwitchPrivate(QObject):
    def __init__(self, q, parent=None, leftText='ON', rightText='OFF'):
        QObject.__init__(self, parent=parent)
        self.leftText=leftText
        self.rightText=rightText
        self.mPointer = q
        self.mPosition = 0.0
        self.mGradient = QLinearGradient()
        self.mGradient.setSpread(QGradient.PadSpread)

        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'position')
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.InOutExpo)

        self.animation.finished.connect(self.mPointer.update)

    @Property(float)
    def position(self):
        return self.mPosition

    @position.setter
    def position(self, value):
        self.mPosition = value
        self.mPointer.update()

    def draw(self, painter):
        r = self.mPointer.rect()
        margin = r.height()/10
        shadow = self.mPointer.palette().color(QPalette.Dark)
        light = self.mPointer.palette().color(QPalette.Light)
        button = self.mPointer.palette().color(QPalette.Button)
        painter.setPen(Qt.NoPen)

        self.mGradient.setColorAt(0, shadow.darker(130))
        self.mGradient.setColorAt(1, light.darker(130))
        self.mGradient.setStart(0, r.height())
        self.mGradient.setFinalStop(0, 0)
        painter.setBrush(self.mGradient)
        painter.drawRoundedRect(r, r.height()/2, r.height()/2)

        self.mGradient.setColorAt(0, shadow.darker(140))
        self.mGradient.setColorAt(1, light.darker(160))
        self.mGradient.setStart(0, 0)
        self.mGradient.setFinalStop(0, r.height())
        painter.setBrush(self.mGradient)
        painter.drawRoundedRect(r.adjusted(margin, margin, -margin, -margin), r.height()/2, r.height()/2)

        self.mGradient.setColorAt(0, button.darker(130))
        self.mGradient.setColorAt(1, button)

        painter.setBrush(self.mGradient)

        x = r.height()/2.0 + self.mPosition*(r.width()-r.height())
        painter.drawEllipse(QPointF(x, r.height()/2), r.height()/2-margin, r.height()/2-margin)

        text = self.leftText if bool(self.mPosition) else self.rightText
        painter.setPen(QColor(255, 255, 255))
        font = QFont('Decorative', 10, QFont.Bold)
        fm = QFontMetrics(font)
        painter.setFont(font)
        textWidth = fm.width(text)
        textHeight = painter.font().pointSize()
        xpoint = r.width() - x - textWidth+10 if bool(self.mPosition) else r.width() - x-12
        painter.drawText(QPointF(xpoint, r.height() / 2 + textHeight / 2), text)

    @Slot(bool, name='animate')
    def animate(self, checked):
        self.animation.setDirection(QPropertyAnimation.Forward if checked else QPropertyAnimation.Backward)
        self.animation.start()


class Switch(QAbstractButton):
    def __init__(self, parent=None, leftText='ON', rightText='OFF'):
        QAbstractButton.__init__(self, parent=parent)
        self.dPtr = SwitchPrivate(self, leftText=leftText,rightText=rightText)
        self.setMaximumWidth(50)
        self.setCheckable(True)
        self.clicked.connect(self.dPtr.animate)

    def sizeHint(self):
        return QSize(50, 25)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.dPtr.draw(painter)

    def resizeEvent(self, event):
        self.update()

