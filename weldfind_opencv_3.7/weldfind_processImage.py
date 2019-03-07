import cv2
import numpy as np

class ProcessImage():
    def __init__(self, cannyThreshold, imgPath, kernelSize=3,):
        self.img = cv2.imread(imgPath)
        self.cannyThreshold = cannyThreshold
        self.kernelSize = kernelSize

    def getContours(self):
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        detect_edges = cv2.GaussianBlur(img_gray, (3, 3), 0)
        detect_edges = cv2.Canny(detect_edges, self.cannyThreshold[0], 
                             self.cannyThreshold[1], apertureSize=self.kernelSize)
        contours = cv2.findContours(detect_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[1]      ##the number varies with the version of opencv

        return contours

    def myDrawContours(self):
        for cnt in self.getContours():
            cv2.drawContours(self.img, [cnt], -1, (0, 255, 0), 2)


    def drawCentrePoints(self, widthThreshold=90):
        cnts = self.getContours()
        #calculate the mean of X coordinates
        cXlist = []
        for cnt in cnts:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cX = int(M["m10"] / M["m00"])
            cXlist.append(cX)
        cXmean = sum(cXlist)/len(cXlist)
    
        for cnt in cnts:
            # compute the center of the contour
            M = cv2.moments(cnt)
            # avoid 
            if M["m00"]==0:
               continue
            cX = int(M["m10"] / M["m00"])
            if abs(cX-cXmean)>widthThreshold:    #discard centre point too far away from the predicted centerline
                continue
            cY = int(M["m01"] / M["m00"])
            cv2.circle(self.img, (cX, cY), 7, (0, 0, 0), -1)


    def drawCenterline(self):
        cnts = self.getContours()
        upres = []
        downres = []
        size = self.img.shape

        for cnt in cnts:
            rect = cv2.minAreaRect(cnt)
            if rect[0][1] > size[0]/2:
                downres.append(rect[0])
            else:
                upres.append(rect[0])
            #print("中心坐标：", rect[0])
            #print("宽度：", rect[1][0])
            #print("长度：", rect[1][1])
            #print("旋转角度：", rect[2])
            box = cv2.boxPoints(rect)  # cv.boxPoints(rect) for OpenCV 3.x 获取最小外接矩形的4个顶点
            box = np.int0(box)
            #print("四个顶点坐标为;", box)
            #draw_img = cv2.drawContours(img, [box], -1, (0, 0, 255), 3)	
        uplen = len(upres)
        downlen = len(downres)
        upx, upy, downx, downy = 0, 0, 0, 0
        for i in upres:
            upx += i[0]
            upy += i[1]
        ups = [int(upx/uplen), int(upy/uplen)]
        for i in downres:
            downx += i[0]
            downy += i[1]
        downs = [int(downx/downlen), int(downy/downlen)]
        cv2.circle(self.img, (ups[0], ups[1]), 10, (0,155,155), 4)
        cv2.circle(self.img, (downs[0], downs[1]), 10, (0,155,155), 4)
        cv2.line(self.img, (ups[0], 0), (downs[0], size[0]), (255,255,255), thickness=4)
        array = np.array([ups,downs])
        rec = cv2.minAreaRect(array)
        print(rec[2])   #旋转角度θ是水平轴（x轴）逆时针旋转，与碰到的矩形的第一条边的夹角。并且这个边的边长是width，另一条边边长是height。
                #也就是说，在这里，width与height不是按照长短来定义的。




