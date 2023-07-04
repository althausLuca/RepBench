class TimePoint:
    def __init__(self, timestamp, val):
        self.timestamp = timestamp
        self.value = val  # the observe value
        self.modify = val  # modify is in [minVal, maxVal]
        self.minVal = None  # the minimum/maximum value of candidates
        self.maxVal = None
        self.setRange(float('-inf'), float('inf'))

    def getTimestamp(self):
        return self.timestamp

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def getValue(self):
        return self.value

    def setValue(self, observeval):
        self.value = observeval

    def getModify(self):
        return self.modify

    def setModify(self, modify):
        self.modify = modify

    def getMinVal(self):
        return self.minVal

    def getMaxVal(self):
        return self.maxVal

    def setRange(self, minVal, maxVal):
        self.minVal = minVal
        self.maxVal = maxVal