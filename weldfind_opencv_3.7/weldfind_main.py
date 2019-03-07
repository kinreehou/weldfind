from weldfind_getFuzzyThreshold import *
from weldfind_processImage import *


##test start from here
cannyThresholds = imgToThresholdValues('p1.png')
testProcess = ProcessImage(cannyThresholds.getThresholdValues(),'p1.png')
testProcess.myDrawContours()
testProcess.drawCentrePoints()
testProcess.drawCenterline()

#display
cv2.imshow('?', testProcess.img)
cv2.waitKey(0)
cv2.destroyAllWindows()

