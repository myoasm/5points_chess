# --**-- coding: utf-8 --**--
# --**-- author: dingchao --**--
# --**-- chess_reco      --**--

import  numpy as np
#import  imutils
import  cv2
import math

def gethsv(event, x, y, flags, param):  # 获取鼠标点的hsv值
    if event == cv2.EVENT_LBUTTONDOWN:
        print(hsv[y, x])

def perfect_it(ranked_list):
    new_list = []
    def delete_some(ranked_list):
        for i  in range(len(ranked_list)):
            if i < len(ranked_list)-1 and ranked_list[i][1] <= ranked_list[i+1][1] + 3 and ranked_list[i][1] >= ranked_list[i+1][1] - 3:
                new_list.append(ranked_list[i])
            elif i > 1 and ranked_list[i][1] <= ranked_list[i-1][1] + 3 and ranked_list[i][1] >= ranked_list[i-1][1] - 3:
                new_list.append(ranked_list[i])
            else: pass
    def add_some(deleted_some):
        list_good = [[]for i in range(9)]
        y_list = []
        x_list = []
        y = 0
        for point in deleted_some:
            if not (y - 3 <= point[1] <=  y+3):
                y = point[1]
                y_list.append(point[1])
        for i  in range(9):
            for point in deleted_some:
                if (y_list[i]- 3 <= point[1] <=  y_list[i]+3):
                    list_good[i].append(point)
                else:pass
        print('list good',list_good)

        x = -1000
        min = 1000
        for i in range(9):
            if len(list_good[i]) == 9:
                pass
            else:
                list_x = list_good[i][:]
                for point in list_x:
                    if (point[0] - x) < min:
                        min = point[0] - x
                    else:pass
                    x = point[0]
                min = min + 1
                for









    delete_some(ranked_list)
    add_some(new_list)
    print(new_list)

def point_rank(points_list):
    points = points_list
    def compare(point1, point2):
        if point2[1]>= point1[1] +3:
            return  False
        elif point2[1]<= point1[1]-3 :
            return True
        elif point2[0] >= point1[0]:
            return False
        else:return True

    def points_rank(points_list): #采用霍尔老先生的快排
        if len(points_list) >= 2:
            mid = points_list[len(points_list) // 2]  # 选取基准值
            left, right = [], []  # 定义基准值左右两侧的列表
            points_list.remove(mid)  # 从原始数组中移除基准值
            for point in points_list:
                if compare(point, mid):#返回值为真，表示point点比mid大
                    right.append(point)
                else:
                    left.append(point)
            return points_rank(left) + [mid] + points_rank(right)
        else:
            return points_list
    new_lists = points_rank(points)
    print(new_lists)
    return new_lists



def get_good_line(binary,img):

    # print(~gray ==255 - gray.copy())

    rows, cols = binary.shape
    scale = 30
    # 识别横线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (cols // scale, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    # cv2.imshow("Eroded Image",eroded)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
    cv2.imshow("row", dilatedcol)

    # 识别竖线
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, rows // scale))
    eroded = cv2.erode(binary, kernel, iterations=1)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    cv2.imshow("col", dilatedrow)
    points_list = []

    # 标识交点
    bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
    cv2.imshow("points", bitwiseAnd)
    im2, points, blackhierarchy = cv2.findContours(bitwiseAnd.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for point in points:
        (x, y), radius = cv2.minEnclosingCircle(point)
        print(int(x), int(y))
        center = (int(x), int(y))
        points_list.append(center)
        radius = int(radius)
                # 绘制闭圆
        img = cv2.circle(img, center, radius, (0, 255, 0), 3)
        cv2.imshow('oo', img)
    # 标识表格
    print(">>>",len(points_list))
    points = point_rank(points_list)
    perfect_it(points)
    #print(ranked)
    merge = cv2.add(dilatedcol, dilatedrow)
    cv2.imshow("add Image", merge)

    key = cv2.waitKey(0)
    if key == 'q':
        return 0

def line_detect(bw_image, image):
    # rho 线段以像素为单位的距离精度，double类型的，推荐用1.0
    # theta 检测直线的角度，一般为np.pi/180
    # threshold 直线上点数阈值，超过才会判断为直线，这里设为20
    # minLineLength 直线长度的阈值，超过才会判断为直线，这里设为20
    # minLineGap 不同线段之间的距离阈值，超过则默认为是一条直线，这里设为20
    lines = cv2.HoughLinesP(bw_image, 1, np.pi/180, 20, minLineLength=40, maxLineGap=200)  # 霍夫变换检测直线
    for line in lines:
        line = line[0]
        #print(line)
        x_start, y_start, x_end, y_end = line
        if math.sqrt((x_end - x_start)**2 + (y_end - y_start)**2)> 300:
            cv2.line(image, (x_start, y_start), (x_end, y_end), (0, 255, 0), 1)

    cv2.imshow('', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    black_min = np.array([0, 0, 0])
    black_max = np.array([180, 110, 110])
    white_min = np.array([0, 0, 200])
    white_max = np.array([180, 50, 255])
    img = cv2.imread("C:/Users/myosam/Desktop/44.png")
    image = img.copy()
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    mask_balck = cv2.inRange(hsv, black_min, black_max)
    mask_white = cv2.inRange(hsv, white_min, white_max)
    thresh = cv2.threshold(gray, 40, 240, cv2.THRESH_BINARY)[1]
    cv2.imshow('mask_black',mask_balck)
    cv2.imshow('mask_white', mask_white)
    im,whitecontours, hierarchy = cv2.findContours(mask_white.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.imshow('lunkuo',im)
    im2,blackcontours,  blackhierarchy = cv2.findContours(mask_balck.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cv2.findContours(mask_white.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0]
    print(len(whitecontours))
    print(len(blackcontours))
    for cb in blackcontours:
        x, y, w, h = cv2.boundingRect(cb)
        if w > 20 and h > 20 :
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    for c in whitecontours:
        # 找到边界框的坐标
        x, y, w, h = cv2.boundingRect(c)
        if w >20 and h > 20 :

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary = cv2.adaptiveThreshold(~gray, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, -12)
    ret, bw_image = cv2.threshold(gray, 90, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(gray, 50, 150)
    get_good_line(binary,image)
    #line_detect(bw_image, image)


        # 找到最小区域
        # rect = cv2.minAreaRect(c)
        #
        # # 计算最小矩形的坐标
        # box = cv2.boxPoints(rect)
        #
        # # 坐标转换为整数
        # box = np.int0(box)
        #
        # # 绘制轮廓  最小矩形 blue
        # cv2.drawContours(img, [box], 0, (255, 255, 255), 1)
        #
        # # 计算闭圆中心店和和半径
        # (x, y), radius = cv2.minEnclosingCircle(c)
        # print(int(x), int(y))
        #
        # # 转换为整型
        # center = (int(x), int(y))
        # radius = int(radius)
        #
        # # 绘制闭圆
        # img = cv2.circle(img, center, radius, (0, 255, 0), 1)

   # cv2.drawContours(img, whitecontours, -1, (0, 0, 255), 1)
    cv2.imshow('contours', img)
   # print(cnts)
    # for c in cnts:
    #     # 获取中心点
    #     M = cv2.moments(c)
    #     print(M)
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    #     # 画出轮廓和中点
    #     cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    #     cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    #     cv2.putText(image, "center", (cX - 20, cY - 20),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #
    #     #显示图像
    #cv2.imshow("Image", img)
    cv2.setMouseCallback('contours', gethsv)
    #cv2.waitKey(0)
    #cv2.imshow("gray",thresh)
    cv2.waitKey(0)