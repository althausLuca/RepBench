class TimeSeries:
    def __init__(self, timeseries=None):
        self.timeseries = timeseries if timeseries is not None else []

    def getTimeseries(self):
        return self.timeseries

    def setTimeseries(self, timeseries):
        self.timeseries = timeseries

    def addTimePoint(self, tp):
        self.timeseries.append(tp)

    def getLength(self):
        return len(self.timeseries)