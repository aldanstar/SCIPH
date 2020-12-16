from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QLabel

from res import resources, Image

class work_indicator(QWidget):
    def __init__(self, title):
        QWidget.__init__(self, parent=None)
        self.__title=title
        self.__title_sufix=""
        self.__status=False
        self.__conected_indicator=Image(resources.GREEN_INDICATOR)
        self.__ready_indicator=Image(resources.YELLOW_INDICATOR)
        self.__disconected_indicator=Image(resources.RED_INDICATOR)
        self.gui_init()
        self.update()

    def status(self):
        return self.__status

    def setStatus(self, value):
        self.__status=value
        self.update()

    def update(self):
        if not self.__status:
            self.__current_indicator = self.__disconected_indicator
        elif self.__status == True:
            self.__current_indicator = self.__conected_indicator
        else:
            self.__current_indicator = self.__ready_indicator

        self.__current_indicator = self.__current_indicator.scaled(16, 16, Qt.KeepAspectRatio)
        self.indicator.setPixmap(self.__current_indicator)

    def title(self):
        return self.__title

    def sufix(self):
        return self.__title_sufix

    def gui_init(self):
        layout=QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)
        self.setLayout(layout)

        label = QLabel(self)
        label.setText(u'{0}: {1}'.format(self.title(), self.sufix()))
        layout.addWidget(label)

        self.indicator= QLabel(self)
        layout.addWidget(self.indicator)
        self.update()