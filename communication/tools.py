#-------------------------------------------------------------------------------
 #!/usr/bin/env python
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------

import os
from math import cos, radians, sin
import numpy as np
from enum import Enum

class MOTORTYPE(Enum):
    STEP=0
    SERVO=1

class SENDTYPE(Enum):
    IDLE=0
    JOG=1
    HOLD=2
    CHECK=3

class VALUETYPE(Enum):
    @staticmethod
    def STRING(): return 0

    @staticmethod
    def VALUE(): return 1


class statstools:

    '''набор статических функций для расчета'''

    @staticmethod
    def get_photos_paths(shot, progress=None):
        sensor_paths=[]
        for f in os.listdir(shot):
            f_path=os.path.normpath(os.path.join(shot, f))
            if os.path.normpath(os.path.basename(os.path.splitext(f_path)[1]))=='.tiff' or os.path.normpath(os.path.basename(os.path.splitext(f_path)[1]))=='.jpg':
                sensor_paths.append(os.path.normpath(f_path))
        return sensor_paths

    @staticmethod
    def meanStdInList(List): #функция определения медианного среднего в списке
            median=np.median(List) #определяем медиану списка через numpy
            std=np.std(List) #определяем ср.кв. отклонение через numpy
            for num in List: # осекаем список от медианы по среднеквадратическому отклонению
                if num<=(median-std) or num>=(median+std):
                    List.pop(List.index(num)) # удаляем элементы списка не входящие в условие
            return np.mean(List) # возвращаем среднее значение форматированного списка через numpy

    @staticmethod
    def meanList(List): #функция оперделения среднего значения между максимальным и минимальным элементами списка
        return (np.max(np.asarray(List))+np.min(np.asarray(List)))/2

    @staticmethod
    def coordinatesByCircle(r, fi, count, rot=0, progress=None): #функция расчета координат по данным r-радиуса, fi-угла поворота (шага), count-количество точек, rot-смещение начального угла
        XList=[]
        YList=[]
        aList=[]
        for i in range(0,count):
            XList.append(r*cos(radians(fi*i-rot)))
            YList.append(r*sin(radians(fi*i-rot)))
            aList.append(fi*i-rot)
            if progress:
                progress(100*(i+1)/count)
        return XList, YList, aList #возвращаем списки для X, для Y и для угла поворота каждой точки

    @staticmethod
    def coordinatesForBlockCameras(cameras, r, fi, rot=0): #функция расчета координат по данным count-количество точек из длинны списка камер , r-радиуса, fi-угла поворота (шага), rot-смещение начального угла
        count=len(cameras)
        return statstools.coordinatesByCircle(r, fi, count, rot)

    @staticmethod
    def addCoordForCameras(cameras, XCoord, YCoord, ZCoord, angels): #функция присвоение координат привязки каждой камере из спсика камер (данные из списков X,Y,Z и списка угла поворота)
        for camera in cameras:
            c=cameras.index(camera)
            camera.reference.accuracy=PhotoScan.Vector( (0.1, 0.1, 0.1) ) #определяем точность положения для камеры при уравнивании
            camera.reference.location=PhotoScan.Vector( (XCoord[c], YCoord[c], ZCoord) ) #задаем координаты
            camera.reference.location_accuracy=PhotoScan.Vector( (0.1, 0.1, 0.1) ) #определяем точность положения для камеры при уравнивании
            camera.reference.rotation=PhotoScan.Vector( (360-angels[c], 0, 90) ) #определяем крен, тангаж и рыскание для камеры
            camera.reference.rotation_accuracy=PhotoScan.Vector( (5, 5, 5) ) #определяем точность крена, тангажа и рыскания при уравнивании

    @staticmethod
    def addCoordForMarkers(markers, XCoord, YCoord, ZCoord): #функция присвоение координат привязки каждой камере из спсика камер (данные из списков X,Y,Z и списка угла поворота)
        for marker in markers:
            m=markers.index(marker)
            marker.reference.location=PhotoScan.Vector( (XCoord[m], YCoord[m], ZCoord) ) #задаем координаты
            marker.reference.accuracy=PhotoScan.Vector( (0.005, 0.005, 0.005) ) #определяем точность положения для камеры при уравнивании
            marker.reference.enabled=True


    @staticmethod
    def closestPointFromModelToCamera(camera, progress=None): #функция расчета ближайшей точки от камеры до модели
        dist=1E10 #определяем начальную дистанцию как максимальную
        model=camera.chunk.model #определяем модель

        xWindow_start=int(camera.sensor.width/3) #определяем начало окна поиска на фотографии по x
        xWindow_end=camera.sensor.width-int(camera.sensor.width/3) #определяем конец окна поиска на фотографии по x
        xWindow_size=xWindow_end-xWindow_start #определяем размер окна поиска на фотографии по x

        yWindow_start=int(camera.sensor.height/3) #определяем начало окна поиска на фотографии по y
        yWindow_end=camera.sensor.height-int(camera.sensor.height/3) #определяем конец окна поиска на фотографии по y
        yWindow_size=yWindow_end-yWindow_start #определяем размер окна поиска на фотографии по y

        axis_count=10 #определяем количество замеров

        xstep=int(xWindow_size/axis_count) #определяем шаг выборки для замера
        ystep=int(yWindow_size/axis_count)

        xindex=0 #начальное положение для callback

        for x in range(xWindow_start, xWindow_end, xstep):
            yindex=0
            for y in range(yWindow_start, yWindow_end, ystep):
                point =  PhotoScan.Vector([x, y])
                point3D = model.pickPoint(camera.center, camera.transform.mulp(camera.sensor.calibration.unproject(point)))
                if point3D:
                    dist = min(dist, (camera.center - point3D).norm())
                    closestPoint=point3D
                yindex+=1
                if progress:
                    progress((xindex*axis_count+yindex)/(pow(axis_count,2)))
            xindex+=1
            if progress:
                progress((xindex*axis_count+yindex)/(pow(axis_count,2)))
        return closestPoint

    @staticmethod
    def distBetweenPoints3D(point1, point2): #функция расчета растояния между точками для удобства
        return (point1 - point2).norm()

    @staticmethod
    def closestCameraAndDirection(camera, cameraList, progress=None): # Определение ближайшей камеры, ее направления по ходу движения съемки (после или до начальной), и кооэфициент смещения
        dist=1E10 #определяем начальную дистанцию как максимальную
        for cam in cameraList:
            if cam!=camera:
                cdist=statstools.distBetweenPoints3D(camera.center,cam.center)
                if cdist<dist:
                    dist=cdist
                    closestCamera=cam
        distences=[]
        for c in range(1,len(cameraList)-1):
            distences.append((cameraList[c].center - cameraList[c+1].center).norm())
        meandist=np.asarray(distences).mean()

        i=cameraList.index(closestCamera)
        direction=dist/meandist
        lastCamDist=statstools.distBetweenPoints3D(camera.center,cameraList[i-1].center)

        if closestCamera!=cameraList[len(cameraList)-1]:
            nextCamDist=statstools.distBetweenPoints3D(camera.center,cameraList[i+1].center)
            if nextCamDist<lastCamDist:
                direction=-direction
        else:
            lastClosesDist=statstools.distBetweenPoints3D(closestCamera.center,cameraList[i-1].center)
            if lastCamDist-lastClosesDist>0:
                direction=-direction
        return closestCamera, direction
