import math

from repair.statistica_aproach.assist import Assist


class BaseScr:
    def __init__(self, timeseries, theta, delta):
        self.timeseries = timeseries
        self.tpList = timeseries.getTimeseries()
        self.delta = delta
        self.THETA = theta
        self.RES = 0
        self.ORGRES = 0
        self.PARAM = 0
        self.LAMBDA = {}
        self.sizeLBase = 0
        self.sizeLs = []
        self.maxP = 0
        self.minP = 0

    def setTimeSeries(self, timeSeries):
        self.timeseries = timeSeries

    def setDelta(self, delta):
        self.delta = delta

    def setTHETA(self, THETA):
        self.THETA = THETA

    def normalizeParams(self, RES, PARAM):
        self.ORGRES = RES
        self.PARAM = PARAM
        self.RES = RES * PARAM

        self.normalizeTuples()

    def normalizeTuples(self):
        minVal = float('inf')
        maxVal = float('-inf')

        for tp in self.tpList:
            value = round(tp.getValue() * self.PARAM)
            minVal = min(minVal, value)
            maxVal = max(maxVal, value)
            tp.setValue(value)
            tp.setModify(value)

        for tp in self.tpList:
            value = tp.getValue()
            tp.setRange(value - self.THETA, value + self.THETA)

    def normalizeProbability(self, assist):
        size = len(self.tpList)
        self.LAMBDA = {}

        conMap = assist.convolution(self.timeseries)
        maxMinP = assist.calcLnProbability(conMap, self.LAMBDA, size)
        self.maxP = maxMinP[0]
        self.minP = maxMinP[1]

        self.sizeLBase = round(self.THETA / self.RES)
        budgetMax = math.ceil(self.delta / self.RES) + 1
        self.sizeLs = [min(self.sizeLBase * (i + 1) + 1, budgetMax) for i in range(size)]

    def calcIncumbent(self):
        incumbent = 0

        valQ = self.tpList[0].getValue()
        valP = self.tpList[1].getValue()
        timeQ = self.tpList[0].getTimestamp()
        timeP = self.tpList[1].getTimestamp()

        for i in range(1, len(self.tpList) - 1):
            valK = self.tpList[i + 1].getValue()
            timeK = self.tpList[i + 1].getTimestamp()

            tmpPr = self.getLikelihood(timeK, timeP, timeQ, valK, valP, valQ)
            if tmpPr > 0:
                return 1
            incumbent += tmpPr

            valQ = valP
            valP = valK
            timeQ = timeP
            timeP = timeK

        return incumbent

    def getLikelihood(self, timeK, timeP, timeQ, valK, valP, valQ):
        vKP = (valK - valP) / (timeK - timeP)
        vPQ = (valP - valQ) / (timeP - timeQ)

        deltaV = Assist.calcDisV(vKP, vPQ)

        likelihood = self.LAMBDA[deltaV] if deltaV in self.LAMBDA else 1
        return likelihood

    def getIndexW(self, cost):
        index = round(cost / self.RES)
        return index

    def getTraceW(self, D, record):
        size = len(self.tpList)
        targetK = -1
        targetP = -1
        targetW = 0
        theta = round(self.THETA * 2 / self.RES) + 1

        lambda_ = float('-inf')
        tmpW = 0

        tpK = self.tpList[size - 1]
        minValk = tpK.getMinVal()

        for k in range(theta):
            for p in range(theta):
                for w in range(self.sizeLs[size - 1]):
                    if 0 < D[0][p][k][w] < lambda_:
                        lambda_ = D[0][p][k][w]
                        targetW = w
                        targetK = k
                        targetP = p

        valK = minValk + targetK * self.RES
        tpK.setModify(valK)
        if size == 1:
            return lambda_

        tpP = self.tpList[size - 2]
        valP = tpP.getMinVal() + targetP * self.RES
        tpP.setModify(valP)
        if size == 2:
            return lambda_

        j = size - 2
        valQ = record[size - 1][targetP][targetK][targetW]

        while j > 1:
            tpQ = self.tpList[j - 1]
            tpQ.setModify(valQ)

            tmpW = round(abs(valK - tpK.getValue()))
            targetW -= self.getIndexW(tmpW)

            tpK = tpP
            valK = valP
            targetK = targetP

            tpP = tpQ
            valP = valQ
            targetP = round((valP - tpP.getMinVal()) / self.RES)

            valQ = record[j][targetP][targetK][targetW]
            j -= 1

        tpQ = self.tpList[0]
        tpQ.setModify(valQ)

        return lambda_