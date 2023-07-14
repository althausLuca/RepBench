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
        this.repairedColors = ['#2ca02c', '#1f77b4', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
            '#bcbd22', '#17becf', '#2ca02c', '#d62728', '#9467bd', '#e377c2', '#7f7f7f'];

        this.pointStart = Date.UTC(2010, 0, 1);
        this.pointInterval = 1000
    }

    setPointStartAndTimeInterval(pointSTart, pointInterval) {
        this.pointStart = pointSTart
        this.pointInterval = pointInterval
    }

    dotGroundTruth() {
        // this.injectedSeries.forEach(inj => {
        //     let zones = []
        //     let inArea = false
        //
        //     // create zones
        //     inj.originalData.forEach((d, i) => {
        //         if (d === null && inArea) { //leaving anomaly
        //             zones.push({
        //                 value: this.pointStart + Math.max(i - 1, 0) * chartManager.pointInterval,
        //                 dashStyle: "dot"
        //             })
        //             inArea = false
        //         }
        //         if (d !== null && !inArea) { //entering anomaly
        //             zones.push({
        //                 value: this.pointStart + i * this.pointInterval,
        //                 // dashStyle: "solid",
        //             })
        //             inArea = true
        //         }
        //     })
        //     // console.log(zones)
        //     inj.chartSeriesObj.linkedParent.update({zones: zones, zoneAxis: 'x'})
        // })
    }

    getColor(type) {
        let color = null
        if (type === "repair") {
            color = this.repairedColors[this.repairedSeries.length % this.repairedColors.length];
        } else if (type === "injected") {
            color = "red"
        } else {
            color = this.colors[this.originalSeries.length % this.colors.length];
        }
        return color
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
        // chartSeriesData.linkedTo = ser.linkedTo
        chartSeriesData.data = this.normalized ? [...ser.normData] : [...ser.originalData];
        return chartSeriesData
    }

    addSeries(series, addToChart = true, series_type = "original", merge_with = null) {
        this.removeSeries(series.id)
        series_type = series.series_type ? series.series_type : series_type
        series.color = series.color !== undefined ? series.color : this.getColor(series_type)
        let ser = {
            id: series.id,
            originalData: series.data.map(s => s),
            normData: series.norm_data.map(s => s),
            name: series.name,
            series_type: series_type,
            color: series.color,
            chartSeriesObj: null, // ref to series in chart
            _chartSeriesData: series//  acces with getSeriesChartData
        };


        if (series_type === "original") {
            this.originalSeries.push(ser);
        } else if (series_type === "injected") {
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
        try {
            this.dotGroundTruth()
        } catch (e) {
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

    clearRepairedSeries() {
        this.repairedSeries.length = 0
        this.resetSeries()
    }

    getAllSeries() {
        return this.originalSeries.concat(this.injectedSeries).concat(this.repairedSeries).concat(this.reducedSeries)
    }

    hideNoneInjectedSeries() {
        let seriesNamesToHide = this.injectedSeries.map(s => s._chartSeriesData.linkedTo)
        let seriesToHide = mainChart.series.filter(s => !seriesNamesToHide.includes(s.userOptions.name) &&
            this.originalSeries.map(s => s.name).includes(s.userOptions.name))
        seriesToHide.forEach(s => {
            s.hide()
        })
    }

    removeSeries(id) {
        this.injectedSeries = this.injectedSeries.filter(s => s._chartSeriesData.id !== id)
        this.repairedSeries = this.repairedSeries.filter(s => s._chartSeriesData.id !== id)
        this.reducedSeries = this.reducedSeries.filter(s => s._chartSeriesData.id !== id)
        this.originalSeries = this.originalSeries.filter(s => s._chartSeriesData.id !== id)
        try {
            mainChart.get(id).remove();
        } catch (err) {
        }
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
        try {
            allChartSeries.forEach(s => {
                s.isVisible = mainChart.get(s.id).isVisible
            })

        } catch (e) {
        }

        const axis0isDefined = this._getChartXAxis()

        initMainChart(allChartSeries)
        if (axis0isDefined) {
            mainChart.xAxis[0].setExtremes(axis0isDefined.min, axis0isDefined.max)
        }
        //  correct axis if its to large
        if (mainChart.xAxis[0].dataMax < mainChart.xAxis[0].max) {
            mainChart.xAxis[0].setExtremes(mainChart.xAxis[0].dataMin, mainChart.xAxis[0].dataMax)
        }
        this.getAllSeries().forEach((s, i) => {
            s.chartSeriesObj = mainChart.series[i]
        })


        if (typeof adjustLayout === 'function') {
            adjustLayout()
        }
        this.dotGroundTruth()
    }

    setZscore() {
        this.normalized = true
        this.resetSeries()
    }

    setOriginal() {
        this.normalized = false
        this.resetSeries()
    }


    downloadOriginalSeries() {
        var filename = "original_series.csv";
        var result = this.originalSeries.reduce((acc, original_series) => {
            var {name, data} = this.getSeriesChartData(original_series);
            acc[name] = data;
            return acc;
        }, {});

        download(result, filename)
    }

    downloadInjectedSeries() {
        var filename = "injected_series.csv";
        var result = this.injectedSeries.reduce((acc, injected_series) => {
            var {name, data} = this.getSeriesChartData(injected_series);
            var truthLink = injected_series._chartSeriesData.linkedTo;
            var truthSeries = this.originalSeries.find(s => s._chartSeriesData.id === truthLink);
            var truthData = this.getSeriesChartData(truthSeries).data;

            data = data.map((d, i) => {
                return d === null ? truthData[i] : d;
            });
            acc[name] = data;
            return acc;
        }, {});
        download(result, filename)
    }

    downloadRepairedSeries() {
        var filename = "repaired_series.csv";
        var result = this.repairedSeries.reduce((acc, repaired_series) => {
            var {name, data} = this.getSeriesChartData(repaired_series);
            acc[name] = data;
            return acc;
        }, {});
        download(result, filename)
    }

}







