#-------------------------------------------------------------------------------
 #!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
import sys, os, re
import numpy as np
import pickle
from math import ceil

from PySide2.QtWidgets import QApplication,QDockWidget,QProgressBar
from PySide2.QtWidgets import QFileDialog, QWidget, QVBoxLayout
from PySide2.QtCore import Qt, QTranslator
from PySide2.QtGui import QPixmap, QIcon

from app import Project,tools, com_port, Settings
from communication import VALUETYPE, SENDTYPE
from gui.gui_structs import menu_item
from gui.status import work_indicator
from gui.gui_communication import grblDialog
from gui.additional import about_dialog
from gui.tree import Node, ProjectTree
from gui import MainDialog, JogWidget

# Многопоточные и многопроцессорные операции
from multiprocessing.dummy import Pool as ThreadPool
import threading

import time

from communication import GRBL

class Application:

    def __init__(self):
        self.title=u'Tracks detection'
        # Настройки
        self.settings = Settings()

    def application_init(self):


        '''Инициализация Qt приложения'''
        # Создание приложение
        self.qapp = QApplication(sys.argv)
        self.__app_working_status = True
        # Установка локлизатора
        translator = QTranslator(self.qapp)
        translator.load('lang/tr_ru', os.path.dirname(__file__))
        self.qapp.installTranslator(translator)

        self.mainDialog=MainDialog(self, self.title)
        self.mainDialog.closeApp.connect(self.__finalize_before_quit)

        self.controls={'step':['X','Y','Z','A'], 'servo':['B','C'], 'pins':{'P1':[],'P2':['UV','VIS']}}

        self.mainDialog.show()
        self.project_init()
        self.gui_init()
        self.communication_init()

        sys.exit(self.qapp.exec_())

    def __finalize_before_quit(self):
        self.__app_working_status = False
        if self.grbl.connection: self.grbl.connection.close()
        if self.communication_thread: self.communication_thread.join()
        self.qapp.exit()

    def retuenicon(self, name):
        return QIcon(
            QPixmap(os.path.normpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '', name + '.png'))))

    def project_init(self):
        self.project = Project('New')

    def async_sleep(self, sleep):
        for i in range(sleep):
            time.sleep(1)
            if not self.__app_working_status: break

    def __connection_worker(self):
        while self.__app_working_status:
            status=self.__current_conacion_procedure()
            if status: break
            if status:
                self.__current_conacion_procedure = self.grbl.getStatus
            else:
                self.__current_conacion_procedure = self.__auto_seach__
            self.async_sleep(5)
            self.cnc_indicator.setStatus(status)


    def communication_init(self):
        self.grbl = GRBL(HOST= self.settings.grblip)
        self.__current_conacion_procedure=self.__auto_seach__
        self.communication_thread = threading.Thread(target=self.__connection_worker)
        self.communication_thread.setDaemon(True)
        self.communication_thread.start()

    def gui_init(self):

        pref_menu=menu_item(u'Preferences')
        ref_menu=menu_item(u'Reference')
        gen_menu=menu_item(u'Device')

        gen_menu.addChildren(menu_item(u'GRBL', self.showGrblDialog))

        file_menu=menu_item(self.qapp.tr(u'File'))
        file_menu.addChildren(menu_item(u'New', self.newProject),
                              menu_item(u'Open', self.openProject),
                              menu_item(u'Import...', self.openFile),
                              menu_item(u'Save', self.saveProject),
                              menu_item(u'Exit', self.qapp.exit))

        pref_menu.addChildren(gen_menu, menu_item(u'Settings'))

        ref_menu.addChildren(menu_item(u'Help'),
                             menu_item(u'About', self.showAbout))

        self.mainDialog.addMenuItems(file_menu, pref_menu, ref_menu)

        self.cnc_indicator=work_indicator(u'CNC')
        self.mainDialog.addStatusObj(self.cnc_indicator)

        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(True)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.minimum = 1
        self.progressBar.maximum = 100
        self.mainDialog.addPermanentStatusObj(self.progressBar)

        '''Инициализациия таблицы содержания'''
        treeDock = QDockWidget(self.qapp.tr(u'Project tree'), self.mainDialog)
        treeDock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.mainDialog.addDockWidget(Qt.LeftDockWidgetArea, treeDock)

        self.mainnodes = [Node("Samples"), Node("Other")]
        self.project_tree = ProjectTree(self, self.mainnodes)
        self.project_tree.doubleClicked.connect(self.on_tree_clicked)
        treeDock.setWidget(self.project_tree)

        '''Инициализациия центра'''
        jog = JogWidget(app=self.qapp, axies = self.controls, pinAcions = self.pinAcions, motorActions=self.send_to_grbl)
        self.mainDialog.addToCenter(jog)
        jog.raise_()

    def send_to_grbl(self, text, send_type):
            if len(text):
                self.grbl.send_task(text, send_type)

    def pinAcions(self, status, pin):
        task = 'M62 {pin}'.format(pin=pin) if status else 'M63 {pin}'.format(pin=pin)
        self.grbl.send_task(task, SENDTYPE.IDLE)

    def setProgress(self, step, steps):
        value = step/float(len(steps))*100.
        indx = int(ceil(step-1))
        text = self.qapp.tr(steps[indx])
        self.progressBar.setFormat("{0} - {1}%".format(text,round(value,0)))
        self.progressBar.setValue(value)
        self.qapp.processEvents()

    def on_tree_clicked(self, index):
        item = self.project_tree.selectedIndexes()[0]
        if self.project.current_sample != item.model().itemFromIndex(index).obj:
            self.project.current_sample = item.model().itemFromIndex(index).obj
            self.refresh()

    def newProject(self):
        self.mainDialog.PreparedArea.clear()
        self.mainDialog.ThroughArea.clear()
        self.mainDialog.BacklightArea.clear()
        self.mainnodes = [Node("Samples"), Node("Other")]
        self.project_tree.setMainNodes(self.mainnodes)
        self.project = Project('TEMP')
        self.refresh()

    def openProject(self):

        fileName, _ = QFileDialog.getOpenFileName(self.mainDialog, self.qapp.tr("Load project"), ".\\", self.qapp.tr("Project file (*.tpr)"))

        infile = open(fileName, 'rb')
        self.project = pickle.load(infile)
        infile.close()

        self.mainDialog.PreparedArea.clear()
        self.mainDialog.ThroughArea.clear()
        self.mainDialog.BacklightArea.clear()
        self.mainnodes = [Node("Samples"), Node("Other")]
        self.project_tree.setMainNodes(self.mainnodes)
        self.refresh()


    def saveProject(self):
        fileName, _  = QFileDialog.getSaveFileName(self.mainDialog, self.qapp.tr("Save project"), ".\\", self.qapp.tr("Project file (*.tpr)"))
        outfile  = open(fileName, "wb")
        pickle.dump(self.project, outfile)
        outfile .close()


    def draw_tree(self):
        target = self.mainnodes[0]
        children = target.children()
        samples_in_tree=[]

        for sample in self.project.samples.get_sorted_by_id():
            if len(children)>0:
                samples_in_tree = [node.obj for node in children]
            if sample not in samples_in_tree:
                target.addChild(Node(sample))

        self.project_tree.refresh()


    def openFile(self):
        path_to_file, _ = QFileDialog.getOpenFileName(self.mainDialog, self.qapp.tr("Load Image"), self.qapp.tr(u".\example_imgs"), self.qapp.tr("Images (*.jpg)"))
        # path_to_file, _ = QFileDialog.getOpenFileName(self.mainDialog, self.app.tr("Load Image"), self.app.tr("~/Desktop/"), self.app.tr("Images (*.jpg)"))

        # Определяем тип файла на просвет или на подсветку
        tools.processing(path_to_file, self.project, self.separator, self.segmentation, self.counter, self.setProgress)
        self.refresh()

    def refresh(self):
        self.draw_tree()
        self.fill_table()
        self.updete_viewers()


    def fill_table(self):
        data = []
        sample = self.project.current_sample

        if not sample:
            data = [['', '', '']]
            self.mainDialog.tablemodel.setData(data)
            return

        for track in sample.tracks.get_sorted():
            data.append([str(track.id),str(track.count),str(track.area)])

        self.mainDialog.tablemodel.setData(data)
        self.mainDialog.table.resizeRowsToContents()
        self.mainDialog.table.resizeColumnsToContents()

        count = round(np.sum([track.count for track in sample.tracks.get_sorted_by_id()]),2)
        general_area = round(np.sum([track.area for track in sample.tracks.get_sorted_by_id()]),2)

        self.mainDialog.infolabel.setText('''
                        <p align="center">General tracks count<br>{tracks_count}</p>
                        <p align="center">General tracks area (%)<br>{general_area}</p>
                        '''.format(tracks_count=count, general_area=general_area))

    def draw_objects(self, viewer, sample):
        for track in sample.tracks.get_sorted():
            viewer.add_rect(track.left, track.rigth, track.top, track.bottom)
            viewer.add_Polygon(track.contour, track.left, track.top)
            text = 'Count: {tracks_count}\nArea (%): {general_area}'.format(tracks_count=track.count, general_area=track.area)

            viewer.add_Text(text, track.left, track.top)

    def updete_viewers(self):
        sample = self.project.current_sample

        if not sample:
            return

        self.mainDialog.ThroughArea.load_image(sample.through)
        self.mainDialog.BacklightArea.load_image(sample.backlight)
        self.mainDialog.PreparedArea.load_image(sample.prepared)

        self.draw_objects(self.mainDialog.ThroughArea, sample)
        self.draw_objects(self.mainDialog.BacklightArea, sample)
        self.draw_objects(self.mainDialog.PreparedArea, sample)


    def __connect_to_grbl__(self):
        '''Функция подключения к CNC сканера, которая передается в настройки станка'''
        status = self.grbl.connect()
        if not status: return
        self.cnc_indicator.setStatus(-1)
        self.grbl.reset_alarm()
        self.cnc_indicator.setStatus(status)
        return status

    def __check_ip__(self, ip):
        status = False
        test_grbl = GRBL(HOST=self.settings.grblip)
        test_grbl.setHost(ip)
        try:
            status = test_grbl.connect(check=False)
            test_grbl.connection.close()
        except OSError:
            pass
        return ip if status else None

    def __auto_seach__(self, property=None):
        '''Функция авто поиска IP станка
        property нужен, чтобы вернуть результат в inputField окна настроек
        '''
        if self.grbl.connection: self.grbl.connection.close()
        devices = [device for device in os.popen('arp -a')]
        ip_candidates = [re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", device)[0] for device in devices if len(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", device))!=0]
        if self.settings.grblip in ip_candidates:
            ip_candidates.remove(self.settings.grblip)
            ip_candidates.insert(0,self.settings.grblip)

        pool = ThreadPool(4)
        results = pool.map(self.__check_ip__, ip_candidates)
        index = np.where(results!=None)[0][0]
        if not results[index]:
            # print(self.qapp.tr('There is not  devices in current net'))
            return
        pool.close()
        pool.join()

        self.grbl.setHost(results[index])
        self.__connect_to_grbl__()

        if property: property.setText(results[index]) # property нужен, чтобы вернуть результат в inputField

        self.settings.grblip = results[index]
        self.settings.write()
        print(self.qapp.tr('Connected to') + ' {ip}'.format(ip=results[index]))
        return True

    def showAbout(self):
        about = about_dialog(self)
        about.open()


    def showGrblDialog(self):
        dialog = grblDialog(self, connection_func =self.__connect_to_grbl__, auto_seach_func = self.__auto_seach__)
        dialog.execute(self.settings)
