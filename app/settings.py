#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from PySide2.QtCore import QSettings


class Settings(QSettings):
    """Настройки приложения"""

    def __init__(self, parent=None):
        super().__init__("res/settings.ini", QSettings.IniFormat, parent)
        # Инвертировать отмывку
        self.full_screen = self.value('interface/fullscreen', 0)
        self.grblip = self.value('communication/grblip', '0:0:0:0')
        # print(self.full_screen)

    def write(self):
        """Сохраняет настройки"""
        # Инвертировать отмывку
        self.setValue('interface/fullscreen', self.full_screen)
        self.setValue('communication/grblip', self.grblip)
