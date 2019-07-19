# --**-- coding : utf-8 --**--
# --**-- author:dingchao --**--
# --**-- time :190717   --**--

import cv2  as cv
import numpy as np
import pygame
import pyrealsense2
import threading

#import pyrealsense2

class qipan_analyse:
    def __init__(self, pointlist):
        self.points = pointlist
    def analyse(self):
        for point in self.points:
            pass

class Recognize():
    def  __init__(self):
        self.vedio = cv.VideoCapture(0)
        self.white_min = np.array([0, 0, 150])
        self.white_max = np.array([180, 30,225])
        self.black_min = np.array([0, 0, 0])
        self.black_max = np.array([180, 255, 46])
        self.black_list = []
        self.white_list = []

    def get_rangeline(self):
        ret, frame = self.vedio.read()


    def get_position(self):
        while(1):
            def gethsv(event, x, y, flags, param):  # 获取鼠标点的hsv值
                if event == cv.EVENT_LBUTTONDOWN:
                    print(hsv[y, x])

            ret, frame = self.vedio.read()
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            white_mask = cv.inRange(hsv, self.white_min, self.white_max)
            black_mask = cv.inRange(hsv, self.black_min, self.black_max)
            cv.imshow("white", white_mask)
            im,whitecontours, hierarchy = cv.findContours(white_mask.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            im2,blackcontours, blackhierarchy = cv.findContours(black_mask.copy(), cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
            print(len(whitecontours))
            print(len(blackcontours))
            for cb in blackcontours:
                x, y, w, h = cv.boundingRect(cb)
                if w > 50 and h > 50 and w < 200 and h <200:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    tuple=  (int(x + w//2), int(y + h//2), 1)#标记黑色为1
                    self.black_list.append(tuple)
            for c in whitecontours:
                x, y, w, h = cv.boundingRect(c)
                if w > 50 and h > 50 and w < 200 and h <200:
                    cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    tuple = (int(x + w // 2), int(y + h // 2), 2)#标记白色为2
                    self.white_list.append(tuple)

            #cv.setMouseCallback("yuanshi",gethsv)
            print(self.white_list)
            cv.imshow('img', frame)
            key = cv.waitKey(20)
            if key == 27:
                break





if __name__ == "__main__":
    rec = Recognize()
    rec.get_position()


