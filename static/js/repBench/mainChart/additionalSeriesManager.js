class ChartManager {
    //needs mainChart to be initialized to use
    constructor() {
        this.normalized = false;
        this.injectedSeries = [];
        this.repairedSeries = [];
        this.originalSeries = [];
        this.reducedSeries = [];

        this.colors = ['#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9', '#50394c', '#e4d354', '#8085e8', '#8d4653',
            '#91e8e1', '#7cb5ec', '#434348', '#90ed7d', '#f7a35c', '#8085e9'];
        this.repairedColors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
            '#bcbd22', '#17becf', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f'];
    }

    getColor(type) {
        if (type === "repair") {
            return this.repairedColors[this.repairedSeries.length % this.repairedColors.length];
        }
        if (type === "injected") {
            return "red"
        }
        return this.colors[this.originalSeries.length % this.colors.length];
    }

    setTimeInterval(timeStepMS, timeStart) {
        // this.timeInterval = timeStepMS;
        // this.timeStart = timeStart
    }

    getMinMaxIndices() {
        let {min, max} = mainChart.series[0].xAxis.getExtremes()
        let pointStart = mainChart.series[1].data[0].x
        let pointInterval = mainChart.series[1].data[1].x - pointStart
        return {
            "min": parseInt((min - pointStart) / pointInterval),
            "max": parseInt((max - pointStart) / pointInterval)
        }
    }

    getSeriesChartData(ser) {
        let chartSeriesData = ser._chartSeriesData
        chartSeriesData.color = ser.color
        chartSeriesData.data = this.normalized ? [...ser.normData] : [...ser.originalData];
        return chartSeriesData
    }

    addSeries(series, addToChart = true, series_type = "original", merge_with = null) {
        series_type = series.series_type ? series.series_type : series_type


        let ser = {
            id: series.id,
            originalData: series.data.map(s => s),
            normData: series.norm_data.map(s => s),
            name: series.name,
            series_type: series_type,
            color: series.color !== undefined ? series.color : this.getColor(series_type),
            chartSeriesObj: null, // ref to series in chart
            _chartSeriesData: series//  acces with getSeriesChartData
        };


        if (series_type === "original") {
            this.originalSeries.push(ser);
        } else if (series_type === "injected") {
            try {
                updateExportInjectedButton(this.injectedSeries);
            } catch (error) {
                console.error('Failed to call updateExportInjectedButton:');
            }
            this.injectedSeries.push(ser);
        } else if (series_type === "repair") {
            this.repairedSeries.push(ser);
        } else if (series_type === "reduced") {
            this.reducedSeries.push(ser);
        }
        if (addToChart) {
            ser.chartSeriesObj = mainChart.addSeries(this.getSeriesChartData(ser));
            // ser.chartSeriesData = null;
        }
        return ser;
    }

    get_injected_norm_data() {
        //data that gets sent to the back end
        return this.injectedSeries.map(s => {
            return {
                linkedTo: s._chartSeriesData.linkedTo,
                id: s._chartSeriesData.id, //injected id
                data: s.normData
            }
        })
    }

    clearAllSeries() {
        this.repairedSeries.length = 0
        this.injectedSeries.length = 0
        this.reducedSeries.length = 0
        this.resetSeries()
        // removeScores()
    }

    getAllSeries() {
        return this.originalSeries.concat(this.injectedSeries).concat(this.repairedSeries).concat(this.reducedSeries)
    }


    removeSeries(id) {
        this.injectedSeries = this.injectedSeries.filter(s => s._chartSeriesData.id !== id)
        this.repairedSeries = this.repairedSeries.filter(s => s._chartSeriesData.id !== id)
        this.reducedSeries = this.reducedSeries.filter(s => s._chartSeriesData.id !== id)
        this.originalSeries = this.originalSeries.filter(s => s._chartSeriesData.id !== id)
        mainChart.get(id).remove();
    }

    removeSeriesByName(name) {
        this.injectedSeries = this.injectedSeries.filter(s => s._chartSeriesData.name !== name)
        this.repairedSeries = this.repairedSeries.filter(s => s._chartSeriesData.name !== name)
        this.reducedSeries = this.reducedSeries.filter(s => s._chartSeriesData.name !== name)
        this.originalSeries = this.originalSeries.filter(s => s._chartSeriesData.name !== name)
    }

    _getChartXAxis() {
        const axis0isDefined = mainChart !== null && mainChart.xAxis !== undefined && mainChart.xAxis[0] !== undefined
        if (axis0isDefined) {
            const chartMin = mainChart.xAxis[0].min + 0
            const chartMax = mainChart.xAxis[0].max + 0
            return {"min": chartMin, "max": chartMax}
        }
        return false
    }

    resetSeries(showOnlyInjected = false) {
        // if (mainChart !== null) {
        //     mainChart.showLoading('<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif">');
        // }
        if (showOnlyInjected) {
            const repairLinks = this.injectedSeries.map(s => {
                return s._chartSeriesData.linkedTo
            })
            this.originalSeries.forEach(originalS => {
                originalS._chartSeriesData.isVisible = repairLinks.includes(originalS._chartSeriesData.id)
            })
        }
        let allChartSeries = this.getAllSeries().map(s => this.getSeriesChartData(s))

        const axis0isDefined = this._getChartXAxis()
        initMainChart(allChartSeries)
        if (axis0isDefined) {
            mainChart.xAxis[0].setExtremes(axis0isDefined.min, axis0isDefined.max)
        }

        if (typeof adjustLayout === 'function') {
            adjustLayout()
        }
    }


    setZscore() {
        this.normalized = true
        this.resetSeries()
    }

    setOriginal() {
        this.normalized = false
        this.resetSeries()
    }


}







