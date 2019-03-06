##modified from c code: https://cloud.tencent.com/developer/article/1011628
##inspired by the paper An Improved Canny Edge Detection Algorithm Based on
##Type-2 Fuzzy Sets

##Kinree Hou  2018.2.28

import cv2
import math

class getThreshold:
    def __init__(self,hist):
        self.hist=hist
        self.range1=self.getFirst()
        self.range2=self.getLast()
        self.T = self.calculateFuzzyThreshold(self.range1,self.range2)

    def getFirst(self):
        first = 0
        while self.hist[first] == 0 and first < len(self.hist):
            first = first + 1
        return first

    def getLast(self):
        last = len(self.hist)-1
        while self.hist[last] == 0 and last > first:
            last = last - 1
        return last

    def calculateFuzzyThreshold(self,range1,range2):
        ## find the first and the last non-zero value in the histogram
        hist=self.hist
        Threshold=-1
        bestEntropy = math.inf


        ##special case: only one/two colours in the image
        if range1==range2 or range1+1==range2:
            return range1

        ##calculate the weighted/sum histograms

        sumHist = [0]*(range2+1)
        weightHist = [0]*(range2+1)

        sumHist[0]=hist[0]
        if range1>1:
            starti=range1
        else:
            starti=1


        for i in range(starti,range2+1):
            sumHist[i]=sumHist[i-1]+hist[i]
            weightHist[i]=weightHist[i-1]+i*hist[i]

        ##build search table
        sTable=[0]*(range2+1-range1)
        for i in range(1,len(sTable)):
            mu=1/(1+i/(range2-range1))
            sTable[i]=-mu*math.log(mu)-(1-mu)*math.log(1-mu)

        ##caculate best threshold via iteration
        for i in range(range1,range2+1):
            entropy=0
            mu=round(weightHist[i]/sumHist[i])
            for j in range(range1,i+1):
                entropy=entropy+sTable[int(abs(j-mu))]*hist[j]

            if i!=range2:
                mu =round((weightHist[range2]-weightHist[i])/(sumHist[range2]-sumHist[i])) ##warning range2==i , /0
            else:
                mu=0

            for j in range(i+1, range2+1):
                entropy=entropy+sTable[int(abs(j-mu))]*hist[j]

            if bestEntropy>entropy:
                bestEntropy=entropy
                Threshold=i


        return Threshold


    def getCannyThreshold(self):
        if self.T>self.range1:
            T1=self.calculateFuzzyThreshold(self.range1,T-1)
        else:
            T1=self.T
        if self.T<self.range2:
            T2=self.calculateFuzzyThreshold(self.T+1,self.range2)
        else:
            T2=self.T

        return (T1,T2)




class getHistogram():
    def __init__(self,filename):
        self.filename = filename
    def getHistList(self):
        img = cv2.imread(self.filename)
        hist = cv2.calcHist([img],[0],None,[256],[0,256])
        histList = []
        for i in hist:
            histList.append(i[0])

        return histList



##test start from here!!!!!!!!!!!!!!!!!!!!!!
test = getHistogram('p1.png')
test_Hist=test.getHistList()
#print(test_Hist)

test_getThreshold=getThreshold(test_Hist)
histFirst = test_getThreshold.range1
histLast = test_getThreshold.range2
#print(histFirst,histLast)

T=test_getThreshold.calculateFuzzyThreshold(histFirst,histLast)
print(test_getThreshold.getCannyThreshold())











