#-------------------------------------------------------------------------------
 #!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
import telnetlib
import re
import time
import socket
from communication import SENDTYPE, MOTORTYPE
from collections import OrderedDict
import threading
import time

class Axis:
    def __init__(self, name=None):
        self.name=name
        self.motor_type=MOTORTYPE.SERVO
        self.pos=9999.999

class grbl_interface:
    __axies__="XYZABC"

    def __init__(self, HOST= '192.168.0.75'):
        self.HOST = HOST
        self.connection = None
        self.cost = None
        self.status = False
        self.connaction_thread = None
        self.position_str = None
        self.fs = None
        self.step_axies = None

        self.axies=dict()
        for name in self.__axies__:
            self.axies[name]=Axis(name)

    def setHost(self, HOST):
        self.HOST = HOST

    def getStatus(self):
        return self.status

    def connect(self, check=True):
        self.connection = telnetlib.Telnet()
        self.status = False
        try:
            self.connection.open(self.HOST, 23, timeout = 0.5)
            self.status = self.check_conection()
            if self.status and check:
                self.connaction_thread = threading.Thread(target=self.__check_conection_worker)
                self.connaction_thread.setDaemon(True)
                self.connaction_thread.start()
        except socket.timeout:
            if self.connaction_thread: self.connaction_thread.join()
            # print('Not connected')

        return self.status

    def __check_conection_worker(self):
        time.sleep(5)
        while self.status:
            self.status = self.check_procces_conection()
            # print('status is {}'.format(self.status))
            time.sleep(20)

    def check_procces_conection(self):
        for i in range(0,3):
            self.connection.write(b'$I\r\n')
            data = self.connection.read_until(b':MAC=', timeout = 1).decode('utf-8')
            time.sleep(1)
            if data: break
        result = re.findall('(Connected:IP={})'.format(self.HOST),data.replace('\r\n',''))
        return False if len(result)==0 else True

    def check_conection(self):
        valid=b'Grbl \d\.((\d\D)|(\d)) \[\'\$\' for help\]'
        regex_idx=0

        while regex_idx!=-1:
            regex_idx, match, output = self.connection.expect([valid], timeout=1)
            if match:
                status = match.group().decode('utf-8')
                # print('CNC on {0} obtained msg: {1}'.format(self.HOST,status))
                return True
                break
            else:
                print('Disconected')
                return False




    def send_task(self, command, command_type):

        if not self.connection:
            print('GRBL is not connected')
            return

        if command_type==SENDTYPE.IDLE:
            task = '{0}\n'.format(command).encode()
        elif command_type==SENDTYPE.JOG:
            task = '$J=G91 G21 {0}\n'.format(command).encode()
        else:
            task = ''
            print(SENDTYPE.JOG, command_type)

        self.connection.write(task)


    def parse_motor_types(self):
        for symbol in self.step_axies.split(":")[1]:
            self.axies[symbol].motor_type=MOTORTYPE.STEP

    def getСost(self):
        self.connection.write(b'?\r\n')
        coord_valid=b'(\w*\|MPos:\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*\|FS:\d*,\d*\|Pn:XYZA)|(\w*\|MPos:\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*\|FS:\d*,\d*\|Pn:XYZA\|WCO:\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*,\d*\.\d*)'
        regex_idx=0

        while regex_idx!=-1:
            regex_idx, match, output = self.connection.expect([coord_valid], timeout=1)
            if match:
                self.cost, self.position_str, self.fs, self.step_axies = match.group().decode('utf-8').split("|")

##        self.parse_motor_types()
##
##        for ax in self.axies:
##            print(self.axies[ax].motor_type)

        return self.cost

    def get_position(self):
        self.get_status()
        valid=re.compile('\d*\.\d*')

        unnamed_positions=re.findall(valid, self.position_str, flags=0)

        for i in range(0,len(self.__axies__)):
            a_index=self.__axies__[i]
            self.axies[a_index].pos=unnamed_positions[i]



##        key2rank = lambda rank: (for rank, key in enumerate(self.__axies__))



        position=dict()

        for ax in self.axies:
            position[self.axies[ax].name]=float(self.axies[ax].pos)

##        position2=OrderedDict(sorted(position.items(), key=lambda t: key2rank(t[0])))

        print(position)


    def reset_alarm(self):
        time.sleep(1)
        self.connection.write(b'$X\r\n')

    def soft_reset(self):
        self.connection.write(bytes(18))

    def get_settings(self):
        self.connection.write(b'$$\r\n')
        valid = b'(\$\d*=\d*.\d)|(\$\d*=\d*)'
        regex_idx=0
        settings={}

        while regex_idx!=-1:
            regex_idx, match, output = self.connection.expect([valid], timeout=1)
            if match:
                bool_valid=re.compile(r"(^\$(4)$)|(^\$(5)$)|(^\$(6)$)|(^\$(13)$)|(^\$(20)$)|(^\$(21)$)|(^\$(22)$)|(^\$(32)$)")
                line = match.group().decode('utf-8').split("=")
                if "." in line[1]:
                    num=float(line[1])
                elif re.match(bool_valid, line[0], flags=0):
                    num=bool(int(line[1]))
                else:
                    num=int(line[1])
                settings[line[0]]=num

        sorted_settings=OrderedDict(sorted(settings.items(), key=lambda t: int(t[0].replace("$",""))))
        print(sorted_settings)

    def close(self):
        self.connection.close()



##__grbl_telnet=grbl_interface('192.168.0.100')
##__grbl_telnet_conected=__grbl_telnet.connect()
##
##if __grbl_telnet_conected:
##    __grbl_telnet.get_position()
##
##__grbl_telnet.close()



##def getStatus(data):
##    for d in data:
##        if "<Idle" in d:
##            return d
##
##def main():
##    telnet = telnetlib.Telnet(HOST,23,5)
####    telnet.write(b'$?\r\n')
####
####    data = ''
####    data = telnet.read_until(b'>')
####    st=re.split('\r\n',data.decode('utf-8'))
####
####    coord=dict()
####    data=re.findall('\d{,10}\.\d{3}',getStatus(st))
####    names=['X','Y','Z','A','B','C']
####    for name,d in zip(names,data):
####        coord.update([[name,float(d)]])
##    for i in range(0,200):
##        telnet.write(b'$J=G91 G21 F1000 X-1\n')
##        time.sleep(0.1)
####    print(coord['X'])
##
##if __name__ == '__main__':
##    main()
