# -------------------------------------------------------------------------------
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------------
from PySide2.QtWidgets import QGridLayout, QWidget,QVBoxLayout,QHBoxLayout,QPushButton, QLabel, QLineEdit, QGroupBox, QSlider, QGridLayout, QDockWidget, QMainWindow, QSpacerItem, QSizePolicy, QSizePolicy
from PySide2.QtCore import Qt, QSize, QRegExp
from PySide2.QtGui import QRegExpValidator
from communication import VALUETYPE, SENDTYPE
# from res.images.icons import retuenicon, JOG

from PySide2.QtCore import Signal
from collections import OrderedDict
from functools import partial
from res import Icon
from gui.BaseWidgets import Switch

class JogWidget(QWidget):
    def __init__ (self,  parent =None, app=None, axies = {}, pinAcions=None, motorActions=None, *args, **kwargs ):
        QWidget.__init__(self, parent, *args, **kwargs)
        self.app = app
        self._stepMotorAxies = axies['step']
        self._servoMotorAxies = axies['servo']
        self._controlPins = axies['pins']
        self.title = 'JOG'
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.__pinAcions=pinAcions
        self.__motorActions = motorActions
        self.gui_init()

    @property
    def stepMotorAxies(self):
        return self._stepMotorAxies

    @property
    def servoMotorAxies(self):
        return self._servoMotorAxies

    @property
    def controlPins(self):
        return self._controlPins

    def gui_init(self):
        control_group_layout = QVBoxLayout()
        control_group_widget = QWidget()
        control_group_widget.setLayout(control_group_layout)
        self.layout.addWidget(control_group_widget)

        rows=int(len(self._stepMotorAxies)/2)
        columns=rows+int(len(self._stepMotorAxies)%2)

        '''Добавляем шаговики'''
        steps_group=QGroupBox("{}".format(self.app.tr("Steppers")))
        steps_group.setContentsMargins(0, 0, 0, 0)
        steps_group.setStyleSheet("QGroupBox::title {"
            "text-align: left;"
            "font: bold 14px;"
            "})")
        steps_group_layout=QGridLayout()
        steps_group.setLayout(steps_group_layout)
        row = 0
        column = 0
        for i, step_axis in enumerate(self._stepMotorAxies):
            row=int(i/(rows))
            column = i-columns*row
            step_block = stepAxisWidget(step_axis, 1000, self.app, self)
            if self.__motorActions: step_block.changed.connect(self.__motorActions)
            steps_group_layout.addWidget(step_block,row,column, Qt.AlignCenter)
        # spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # steps_group_layout.addItem(spacer)
        control_group_layout.addWidget(steps_group)

        servo_group=QGroupBox("{}".format(self.app.tr("Servos")))
        servo_group.setContentsMargins(0, 0, 0, 0)
        servo_group.setStyleSheet("QGroupBox::title {"
            "text-align: left;"
            "font: bold 14px;"
            "})")

        servo_group_layout=QGridLayout()
        servo_group.setLayout(servo_group_layout)
        row = 0
        column = 0
        for i, servo_axis in enumerate(self._servoMotorAxies):
            row=int(i/(rows))
            column = i-columns*row
            servo_block = servoAxisWidget(servo_axis, 1000, self.app,  180, self)
            if self.__motorActions: servo_block.changed.connect(self.__motorActions)
            servo_group_layout.addWidget(servo_block,row,column, Qt.AlignCenter)
        control_group_layout.addWidget(servo_group)


        led_group=QGroupBox("{}".format(self.app.tr("LED")))
        led_group.setStyleSheet("QGroupBox::title {"
            "text-align: left;"
            "font: bold 14px;"
            "})")

        led_group_layout=QHBoxLayout()
        led_group.setLayout(led_group_layout)
        for pin, labels in self._controlPins.items():
            switch = LedSwitch(self, target=pin) if len(labels)==0 else LedSwitch(self, target=pin, leftText=labels[0], rightText=labels[1])
            if self.__pinAcions: switch.switched.connect(self.__pinAcions)
            led_group_layout.addWidget(switch)
        control_group_layout.addWidget(led_group)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        control_group_layout.addItem(spacer)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacer)


class LedSwitch(Switch):

    switched = Signal(bool, str)

    def __init__ ( self,  parent = None, target='P0', leftText='ON', rightText='OFF', *args, **kwargs ):
        Switch.__init__(self, parent, leftText, rightText, *args, **kwargs)
        self._target = target
        self.leftText=leftText
        self.rightText=rightText
        self.clicked.connect(self.click)

    def click(self, event):
        self.switched.emit(event, self._target)

class LongButton( QPushButton ):
    def __init__ ( self,  parent = None, name=None, *args, **kwargs ):
        QPushButton.__init__(self, parent, *args, **kwargs)

        self._state = 0
        self.name=name
        self.longpressed=0
        self.clicked.connect(self.longPress)

    def setDelay(self, delay):
        self.setAutoRepeat(True)
        self.setAutoRepeatInterval(delay)
        self.setAutoRepeatDelay(500)

    def longPress(self):
        if self.isDown():
            if self._state == 0:
                self._state = 1
            else:
                self.longpressed=1
        elif self._state == 1:
            self._state = 0
            self.longpressed=0
        else:
            pass

class slideBar(QWidget):

    changed = Signal(int)

    def __init__(self, label, maxpos=180, text=None, input_width=50, qtapp=None, parent = None, callback=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.__label=label
        self.__maxpos=maxpos
        self.input_width=input_width
        self.callback=callback
        self.__ipRegex=None

        self.__text=text

        self.gui_init()

    def gui_init(self):

        layout=QHBoxLayout()
        self.setLayout(layout)

        label=QLabel(self.__label, self)
        layout.addWidget(label)

        self.pos_sld = QSlider(Qt.Horizontal)
        self.pos_sld.setMaximum(self.__maxpos)
        self.pos_sld.setTickPosition(QSlider.TicksBothSides)
        self.pos_sld.valueChanged[int].connect(self.onValueChanged)
        self.pos_sld.setTickInterval(10)
        self.pos_sld.setSingleStep(1)
        layout.addWidget(self.pos_sld)

    def onValueChanged(self, value):
        self.changed.emit(value)

    def setValue(self, value):
        self.pos_sld.setValue(value)

class inputField(QWidget):
    def __init__(self, label, text=None, value_type=VALUETYPE.STRING,  ipRegex=None, input_width=50, parent = None, callback=None, runner=None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.__label=label
        self.input_width=input_width

        self.__ipRegex=ipRegex
        if value_type!=VALUETYPE.STRING:
            self.__text=str(text)
            if not self.__ipRegex:
                self.__ipRegex=QRegExp("^[1-9]\\d{,3}$")
        else:
            self.__text=text

        self.callback=callback
        self.__runner=runner

        self.gui_init()

    def gui_init(self):

        layout=QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        label=QLabel(self.__label, self)
        layout.addWidget(label,0,0,Qt.AlignCenter)

        self.__edit=QLineEdit(self.__text, self)
        self.__edit.setFixedWidth(self.input_width)
        if self.__ipRegex:
            ipValidator = QRegExpValidator(self.__ipRegex)
            self.__edit.setValidator(ipValidator)
        layout.addWidget(self.__edit,0,1,Qt.AlignCenter)

        self.__edit.textChanged.connect(self.__changed__)

        if self.callback:
            self.__edit.textEdited.connect(partial(self.callback))

        if self.__runner:
            run_but=QPushButton(self)
            run_but.setText(self.parent.qapp.tr("Run"))
            layout.addWidget(run_but,0,3,Qt.AlignCenter)

            run_but.pressed.connect(self.__runner__)

    def __runner__(self):
        self.__runner(self.__text)

    def __changed__(self, text):
        if not text:
            if self.__text!="-":
                self.__edit.setText(self.__text)
            else:
                self.__edit.setText("0")
        else:
            self.__text=text

    def getText(self):
        return self.__text

    def setText(self, text):
        self.__edit.setText(text)


class dirButtons(QWidget):
    def __init__(self, delay, parent = None, buttons_action = None):
        QWidget.__init__(self, parent)
        self.parent=parent
        self.__delay__=delay
        self.buttons_action=buttons_action
        self.__long_buttos__=[]

        move_buttons={-100:None,-10:None,-1:1,1:1,10:None,100:None}
        self.sorted_move_buttons=OrderedDict(sorted(move_buttons.items(), key=lambda t: t[0]))
        self.setMinimumHeight(32)
        self.setContentsMargins(0,0,0,0)

        self.gui_init()
        self.update_delay()

    def update_delay(self):
        for button in self.__long_buttos__:
            if callable(self.__delay__):
                button.setDelay(self.__delay__())
            else:
                button.setDelay(self.__delay__)

    def gui_init(self):

        self.setMaximumHeight(16)

        layout=QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setLayout(layout)

        for i,but in enumerate(self.sorted_move_buttons):

            if but==abs(but):
                pref='p'
            else:
                pref='m'

            def some():
                print('SOME')
            button = LongButton(self)
            button.released.connect(some)
            button.setStyleSheet("padding: 0px;")
            layout.addWidget(button, 0,i, Qt.AlignCenter)

            if self.sorted_move_buttons[but]:
                self.__long_buttos__.append(button)

            button.setIcon(Icon(r'jog\JOG{}{}_32'.format(pref,abs(but))))
            button.setIconSize(QSize(32,32))
            button.setFixedSize(QSize(32,32))
            button.setText("")
            button.pressed.connect(partial(self.buttons_action, but))


class servoAxisWidget(QWidget):

    changed = Signal(str, SENDTYPE)

    def __init__(self, label, speed=1000, qapp=None, maxpos=180, parent = None):
        QWidget.__init__(self, parent)
        self.setMaximumWidth(250)
        self.setMaximumHeight(100)
        self.setContentsMargins(0, 0, 0, 0)
        self.parent=parent
        self.__label=label
        self.__speed=speed
        self.__maxpos=maxpos
        self.__dir_value=1
        self.qapp = qapp
        self.__delay=self.__calc_delay__
        self.gui_init()

    def __calc_delay__(self):
        return  1000/(self.__speed/60)

    def gui_init(self):
        layout=QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        group=QGroupBox("{} {}".format(self.__label, self.qapp.tr("axis")), self)

        group.setStyleSheet("QGroupBox::title {"
            "text-align: left;"
            "font: bold 14px;"
            "})")

        layout.addWidget(group)

        group_layout=QVBoxLayout()
        group.setLayout(group_layout)

        self.pos_sld = slideBar(self.qapp.tr("Direction"), parent = self)
        self.pos_sld.changed.connect(self.servo_callback)
        group_layout.addWidget(self.pos_sld, self.__maxpos)

        other_options=QWidget()
        group_layout.addWidget(other_options)

        other_layout=QHBoxLayout()
        other_layout.setContentsMargins(0, 0, 0, 0)
        other_options.setLayout(other_layout)

        speed_field = inputField(self.qapp.tr("Speed"), self.__speed, value_type=VALUETYPE.VALUE, parent =self, callback=self.speed_changed)
        other_layout.addWidget(speed_field, Qt.AlignLeft)

        self.value_field = inputField(self.qapp.tr("Value"), self.__dir_value, value_type=VALUETYPE.VALUE, ipRegex=QRegExp("^((-[1-9]\\d{,3})|([1-9]\\d{,3}))|[0]$"), parent =self, runner=self.but_setter)
        other_options.layout().addWidget(self.value_field, Qt.AlignRight)


    def dir_value_changed(self, direct):
        self.__dir_value = int(direct)

    def speed_changed(self, speed):
        if speed:
            self.__speed=int(speed)
            self.dir_buttons.update_delay()

    def but_setter(self, value):
        self.pos_sld.setValue(int(value))
        self.servo_callback(value)

    def servo_callback(self, value):
        self.value_field.setText(str(value))
        print("F{2} {0}{1}".format(self.__label, value,self.__speed))
        self.changed.emit("F{0} {1}{2}".format(self.__speed, self.__label, value), SENDTYPE.IDLE)

class stepAxisWidget(QWidget):

    changed = Signal(str, SENDTYPE)

    def __init__(self, label, speed=1000, qapp=None, parent = None):
        QWidget.__init__(self, parent)
        self.setMaximumWidth(250)
        self.setMaximumHeight(100)
        self.setContentsMargins(0, 0, 0, 0)
        self.parent=parent
        self.__label=label
        self.__speed=speed
        self.__dir_value=1
        self.qapp= qapp
        self.__delay=self.__calc_delay__
        self.gui_init()

    def __calc_delay__(self):
        return  1000/(self.__speed/60)

    def gui_init(self):
        layout=QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        group=QGroupBox("{} {}".format(self.__label, self.qapp.tr("axis")), self)

        group.setStyleSheet("QGroupBox::title {"
            "text-align: left;"
            "font: bold 14px;"
            "})")

        layout.addWidget(group)

        group_layout=QVBoxLayout()
        group.setLayout(group_layout)

        self.dir_buttons=dirButtons(self.__delay, buttons_action=self.axis_callback)
        group_layout.addWidget(self.dir_buttons)

        other_options=QWidget()
        group_layout.addWidget(other_options)

        other_layout=QHBoxLayout()
        other_layout.setContentsMargins(0, 10, 0, 0)
        other_options.setLayout(other_layout)

        speed_field=inputField(self.qapp.tr("Speed"), self.__speed, value_type=VALUETYPE.VALUE, parent =self, callback=self.speed_changed)
        other_layout.addWidget(speed_field, Qt.AlignLeft)

        value_field=inputField(self.qapp.tr("Value"), self.__dir_value, value_type=VALUETYPE.VALUE, ipRegex=QRegExp("^((-[1-9]\\d{,3})|([1-9]\\d{,3}))|[0]$"), parent =self, runner=self.axis_callback)
        other_options.layout().addWidget(value_field, Qt.AlignRight)


    def dir_value_changed(self, direct):
        self.__dir_value = int(direct)

    def speed_changed(self, speed):
        if speed:
            self.__speed=int(speed)
            self.dir_buttons.update_delay()

    def axis_callback(self, dir_and_length):
        if int(dir_and_length):
            print("F{2} {0}{1}".format(self.__label, dir_and_length, self.__speed))
            self.changed.emit("F{2} {0}{1}".format(self.__label, dir_and_length ,self.__speed), SENDTYPE.JOG)