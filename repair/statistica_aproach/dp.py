import math

import numpy as np

from repair.statistica_aproach.TimePoint import TimePoint
from repair.statistica_aproach.base import BaseScr
from repair.statistica_aproach.timeSeries import TimeSeries


class DP(BaseScr):
    def __init__(self, timeseries, THETA, delta):
        super().__init__(timeseries, THETA, delta)

    def mainDP(self):
        size = len(self.tpList)
        theta = round(self.THETA * 2) + 1

        indexList = list(range(theta))

        D = np.ones((2, theta, theta, self.sizeLs[size - 1]))
        record = np.zeros((size, theta, theta, self.sizeLs[size-1]))

        minValk, minValp, minValq = 0, 0, 0
        valK, valP, valQ = 0, 0, 0
        timeK, timeP, timeQ = 0, 0, 0
        tpK = None

        lambda_, cost, tmpL = 0, 0, 0
        indexW = 0

        # for middle store, save space
        D[0] = np.ones((theta, theta, self.sizeLs[size - 1]))
        D[1] = np.ones((theta, theta, self.sizeLs[size - 1]))

        # initial likelihood, lower bound
        incumbent = self.calcIncumbent()
        if incumbent == 1:
            incumbent = -float('inf')

        # The first one, record[0] is null
        tpK = self.tpList[0]
        minValq = tpK.getMinVal()
        timeQ = tpK.getTimestamp()

        # The second one, record[1] is null
        tpK = self.tpList[1]
        minValp = tpK.getMinVal()
        timeP = tpK.getTimestamp()

        # initialize D(1), the first two points
        for p in indexList:
            valP = minValp + self.RES * p
            for q in indexList:
                valQ = minValq + self.RES * q

                cost = abs(valP - self.tpList[1].getValue())
                cost += abs(valQ - self.tpList[0].getValue())
                if cost > self.delta:
                    continue

                indexW = self.getIndexW(cost)

                D[0][q][p][indexW] = 0

        startIndexW, targetIndexW = 0, 0
        # others
        for i in range(2, size):
            if i % 100 == 0:
                print(i)

            tpK = self.tpList[i]
            minValk = tpK.getMinVal()
            timeK = tpK.getTimestamp()
            record[i] = np.zeros((theta, theta, self.sizeLs[i]))

            for k in indexList:
                valK = minValk + self.RES * k
                cost = abs(valK - tpK.getValue())
                startIndexW = self.getIndexW(cost)

                for p in indexList:
                    valP = minValp + self.RES * p

                    for w in range(startIndexW, self.sizeLs[i], 1):
                        # the former point
                        targetIndexW = w - startIndexW

                        for q in indexList:
                            valQ = minValq + self.RES * q

                            if D[0][q][p][targetIndexW] > 0:
                                continue

                            # compute the likelihood for point P
                            tmpL = self.getLikelihood(timeK, timeP, timeQ, valK, valP, valQ)
                            if tmpL > 0:
                                tmpL = self.Constants.ZEROP
                            lambda_ = tmpL + D[0][q][p][targetIndexW]
                            # prune
                            if lambda_ + (size - 1 - i) * math.log(self.maxP) < incumbent:
                                continue

                            if D[1][p][k][w] > 0 or D[1][p][k][w] < lambda_:
                                D[1][p][k][w] = lambda_
                                record[i][p][k][w] = valQ

            D[0] = D[1].copy()

            minValq = minValp
            timeQ = timeP

            minValp = minValk
            timeP = timeK

        targetLikelihood = self.getTraceW(D, record)
        print("The final likelihood is", targetLikelihood)

        # form resultSeries
        resultSeries = TimeSeries()
        for timePoint in self.timeseries.getTimeseries():
            timestamp = timePoint.getTimestamp()
            modify = timePoint.getModify()
            tp = TimePoint(timestamp, modify * self.ORGRES)
            resultSeries.addTimePoint(tp)

        return resultSeries

    def initialize(self, D):
        D.fill(1)