#-------------------------------------------------------------------------------
 #!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------

from PySide2.QtWidgets import QDesktopWidget,QPushButton, QMainWindow, QTabWidget, QDockWidget, QWidget,QLabel
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QTableView
from PySide2.QtCore import Qt, Signal
from gui.gui_structs import menu_item, table_model, menu_bar
from gui.BaseWidgets import DockWidget

class MainDialog(QMainWindow):
    '''Главное диалоговое окно'''

    closeApp = Signal()

    def __init__(self, app, title):
        QMainWindow.__init__(self, parent=None)
        self.app = app
        self.setWindowTitle(title)
        self.setMinimumSize(500, 400)
        dw=QDesktopWidget()

        self.dockWidgets = []

        self.resize(dw.width()*0.7,dw.height()*0.3)

        # self.showFullScreen()
        self.gui_init()

    def addToCenter(self, widget, title='new'):
        title =  widget.title if widget.title else title
        newDockWidget = DockWidget(self, title=title)
        self.centerMainWindow.addDockWidget(Qt.LeftDockWidgetArea, newDockWidget)
        newDockWidget.setWidget(widget)
        if len(self.dockWidgets)>=1:
            self.centerMainWindow.tabifyDockWidget(self.dockWidgets[0],newDockWidget)
        self.dockWidgets.append(newDockWidget)

    def addStatusObj(self, obj):
        '''Добовление стркои статуса'''
        self.statusBar().addWidget(obj)

    def addPermanentStatusObj(self, obj):
        '''Добовление стркои статуса'''
        self.statusBar().addPermanentWidget(obj)

    def closeEvent(self, event):
        self.closeApp.emit()

    def addMenuItem(self, obj):
        newItem=self.menuBar().addItem(obj)

    def addMenuItems(self, *objs):
        for obj in objs:
            newItem=self.menuBar().addItem(obj)

    def gui_init(self):

        menubar=menu_bar(self)
        self.setMenuWidget(menubar)

        self.centerMainWindow=QMainWindow()
        self.centerMainWindow.setTabPosition(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea, QTabWidget.North)

        self.setCentralWidget(self.centerMainWindow)
