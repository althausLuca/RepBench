import math

from repair.statistica_aproach.TimePoint import TimePoint
from repair.statistica_aproach.constants import Constants
from repair.statistica_aproach.timeSeries import TimeSeries


class Assist:
    PATH = "data/"

    @staticmethod
    def readData(filename, index, splitOp):
        timeSeries = TimeSeries()

        try:
            with open(Assist.PATH + filename, 'r') as file:
                lines = file.readlines()

                for line in lines:
                    vals = line.strip().split(splitOp)
                    timestamp = int(vals[0])
                    value = float(vals[index])

                    tp = TimePoint(timestamp, value)
                    timeSeries.addTimePoint(tp)

        except IOError as e:
            print("Error reading the file:", e)

        return timeSeries

    @staticmethod
    def calcRMS(truthSeries, resultSeries):
        cost = 0.0
        delta = 0.0
        len_ = len(truthSeries.getTimeseries())

        for i in range(len_):
            delta = resultSeries.getTimeseries()[i].getModify() - truthSeries.getTimeseries()[i].getValue()
            cost += delta * delta

        cost /= len_

        return math.sqrt(cost)

    @staticmethod
    def buildVModel():
        minV = Constants.MINV
        maxV = Constants.MAXV
        interval = Constants.INTERV

        size = math.ceil((maxV - minV) / interval) + 1

        Constants.SPEEDPAT = [0.0] * size
        for i in range(size):
            Constants.SPEEDPAT[i] = minV + i * interval

        Constants.SPEEDOUT = [0.0] * size
        Constants.SPEEDOUT[0] = minV
        for i in range(1, size):
            Constants.SPEEDOUT[i] = (Constants.SPEEDPAT[i - 1] + Constants.SPEEDPAT[i]) / 2

    @staticmethod
    def calcDisV(v2, v1):
        disV = 0.0

        index = 0
        tmpV = v2 - v1
        if tmpV > Constants.MAXV or tmpV < Constants.MINV:
            disV = float('inf')
            return disV

        index = math.ceil((tmpV - Constants.MINV) / Constants.INTERV)
        disV = Constants.SPEEDOUT[index]
        return disV

    @staticmethod
    def calcLnProbability(conMap, LAMBDA, size):
        maxHit = 0
        minHit = size
        value = 0.0

        for entry in conMap.items():
            if entry[1] > maxHit:
                maxHit = entry[1]
            if entry[1] < minHit:
                minHit = entry[1]

        maxP = maxHit / size
        minP = minHit / size

        for entry in conMap.items():
            value = entry[1] / size
            LAMBDA[entry[0]] = math.log(value)

        return [maxP, minP]

    def convolution(self, timeseries):
        conMap = {}

        tpList = timeseries.getTimeseries()
        vList = []

        preVal = 0.0
        curVal = 0.0
        preTime = 0
        curTime = 0
        isFirst = True

        deltaVal = 0.0
        deltaTime = 0

        for tp in tpList:
            if isFirst:
                preVal = tp.getValue()
                preTime = tp.getTimestamp()
                isFirst = False
                continue

            curVal = tp.getValue()
            curTime = tp.getTimestamp()
            deltaVal = curVal - preVal
            deltaTime = curTime - preTime

            vList.append(deltaVal / deltaTime)
            preVal = curVal
            preTime = curTime

        preV = 0.0
        curV = 0.0
        deltaV = 0.0

        isFirst = True
        for v in vList:
            if isFirst:
                preV = v
                isFirst = False
                continue

            curV = v
            deltaV = self.calcDisV(curV, preV)
            if deltaV == float('inf'):
                preV = curV
                continue

            if deltaV in conMap:
                conMap[deltaV] += 1
            else:
                conMap[deltaV] = 1
            preV = curV

        return conMap