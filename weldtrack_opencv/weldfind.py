import cv2
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib
img = cv2.imread('p1.png')

cv2.imshow('?',img)
#cv2.waitKey()

#阈值化处理
lowThreshold = 90#视频中的例图就是为了确定合适的阈值？通过提取例图中特定区域的像素值，拟合出lowthreshold值
ratio = 3
kernel_size = 3
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
detected_edges = cv2.Canny(detected_edges, lowThreshold, lowThreshold * ratio, apertureSize=kernel_size)
#cv2.imshow('?',detected_edges)
#cv2.waitKey()

# find contours in the thresholded image
cnts = cv2.findContours(detected_edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[1]#########this is the key (opencv 3.4.1)   "cnts=cnts[0] (opencv 4.0.0)";

#分上下两部分
upres = []
downres = []
size = img.shape
'''
hist = cv2.calcHist(gray,[1],None,[256],[0,256])
plt.plot(hist)
plt.show()
sobelx=cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3)#1,0表示只在x方向求一阶导数
sobely=cv2.Sobel(gray,cv2.CV_64F,0,1,ksize=3)#0,1表示只在y方向求一阶导数
mag=cv2.magnitude(sobelx,sobely)
#print('sobelx=', sobelx)
#print('mag=', mag)
#print(len(sobelx))
sobelx=cv2.convertScaleAbs(cv2.Sobel(gray,cv2.CV_64F,1,0,ksize=3))
#print('sobelx2=', sobelx)
# plt.hist(sobelx, bins=40, normed=0, facecolor="blue", edgecolor="black", alpha=0.7)
'''
for cnt in cnts:
    # compute the center of the contour
    M = cv2.moments(cnt)
    
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    #cnt = np.array(cnt).reshape((-1,1,2)).astype(numpy.int32)
    if M["m00"]>0:
	    cv2.drawContours(img, [cnt], -1, (0, 255, 0), thickness=1)
	    # 画中心点
	    cv2.circle(img, (cX, cY), 7, (0, 0, 0), -1)
    # 画轮廓
    #cv2.putText(img, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

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
cv2.imshow('?',img)
cv2.waitKey()
#画出焊缝轨迹线
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
cv2.circle(img, (ups[0], ups[1]), 10, (0,155,155), 4)
cv2.circle(img, (downs[0], downs[1]), 10, (0,155,155), 4)
cv2.line(img, (ups[0], 0), (downs[0], size[0]), (255,255,255), thickness=4)
array = np.array([ups,downs])
rec = cv2.minAreaRect(array)
print(rec[2])#旋转角度θ是水平轴（x轴）逆时针旋转，与碰到的矩形的第一条边的夹角。并且这个边的边长是width，另一条边边长是height。也就是说，在这里，width与height不是按照长短来定义的。
cv2.imshow('?',img)
cv2.imwrite('OUT1.png', img)
cv2.waitKey()
