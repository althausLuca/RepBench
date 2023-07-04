from repair.statistica_aproach.assist import Assist
from repair.statistica_aproach.dp import DP

RES = 0.1  # the resolution of the data
PARAM = 10  # RES * PARAM = 1, the normalized parameter
THETA = 5  # after normalized
delta = 1500
inputFileName = "stock1.2k.data"



def main():
    # inputFileName = "stock10k.data" # may be out of memory under 10G

    assist = Assist()
    splitOp = ","

    dirtySeries = assist.readData(inputFileName, 1, splitOp)
    truthSeries = assist.readData(inputFileName, 2, splitOp)

    rmsDirty = assist.calcRMS(truthSeries, dirtySeries)
    print("Dirty RMS error is", rmsDirty)

    RES = 0.1  # the resolution of the data
    PARAM = 10  # RES * PARAM = 1, the normalized parameter
    THETA = 5  # after normalized
    delta = 1500

    assist.buildVModel()
    dp = DP(dirtySeries, THETA, delta)
    dp.normalizeParams(RES, PARAM)
    dp.normalizeProbability(assist)
    resultSeries = dp.mainDP()

    rms = assist.calcRMS(truthSeries, resultSeries)

    print("Repair RMS error is", rms)


if __name__ == "__main__":
    main()
