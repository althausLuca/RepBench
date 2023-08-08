let chartManager = new ChartManager()
if (typeof chartHeight === 'undefined') {
    var chartHeight = 750; // Variable declaration and assignment
}


const chartNavigator = { // do not use navigator since it is used by another script
    // xAxis: {
    //     labels: {
    //         formatter: function () {
    //             return this.value.toString();
    //         }
    //     }
    // },
    enabled: true,
    adaptToUpdatedData: true,
    height: 60
}

// All series that are not part of the original graph have to be linked to some other series
const events = {
    // hide linked series elements
    render: function () {
        let series = this.series

        if (series.filter(s => s.visible).length === 0) {
            series[0].show()
        }
        series.forEach(s => {
            var id = s.userOptions.id,
                name = s.userOptions.name
            var boundedId = Array.from(document.getElementsByClassName(id + "-bounded"))
            var boundedName = Array.from(document.getElementsByClassName(name + "-bounded"));
            // concatenate boundedId and boudedName
            var bounded = boundedId.concat(boundedName);
            if (bounded.length > 0) {
                if (s.visible) {
                    bounded.forEach(b => {
                        b.style.display = "block";
                    })
                } else {
                    bounded.forEach(b => {
                        b.style.display = "none";
                    })
                }
            }

        })
    },

}


let tooltip = {
    formatter: function (e) {
        let x = this.x
        // return ['<p style=\"color:black;font-size:15px;\"> ' + this.series.name + ': ' + this.y + '</p>'].concat(
        //     this.series.linkedSeries.map(function (s) {
        //         console.log("SSSSSSSSSS" , s)
        //         selectedY = s.data[x].y
        //         selectedY = Math.round(selectedY * 1000) / 1000
        //         if (selectedY !== null) {
        //             if (s.name.includes('injected')) {
        //                 return "<br> <p style=\"color:red;font-size:15px;\">" + s.name + " " + selectedY + "<\p> "
        //             } else return "<br> <p style=\"color:" + s.color + ";font-size:15px;\">" + s.name + ": " + selectedY + "<\p> "
        //         }
        //
        //     })
        // );
        return ['<p style=\"color:black;font-size:15px;\"> ' + this.series.name + ': ' + this.y + '</p>']
    },
    shared: false,
    valueDecimals: 2
}


let mainChart = null
let threshold = null
let legendWidth = null
let load_chart = null
const loadChart = function (series = {}, container = 'load_chart') {
    document.getElementById("content").style["overflow-y"] = "hidden"
    if (load_chart !== null) {
        load_chart = null
    }
    load_chart = Highcharts.chart(document.getElementById("load_chart"), {
        series: [{data: [], showInLegend: false}],
        title: {
            text: chart_title,
            style: {
                color: 'black',
                fontWeight: 'bold',
                "font-size": "30px"
            }
        },
        credits: {
            enabled: false
        },
    })
    load_chart.showLoading('<img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Loading_icon.gif">');
}


const createEmptyChart = function (length, container = 'highcharts_container') {
    chartManager = new ChartManager();
    length = parseInt(length)
    if (length > 1000) length = 1000
    length = timeInterval * 1000 * length

    // chartManager.setTimeInterval(timeInterval*1000)
    // let series = [{data:[] , visible:false, showInLegend: false}]
    let series = [{
        data: [[Date.UTC(2010, 0, 1), 7], [Date.UTC(2010, 0, 1) + length, 12]],
        opacity: 0,
        showInLegend: false,
        visible: false
    }]
    chartManager.setPointStartAndTimeInterval(Date.UTC(2010, 0, 1), timeInterval * 1000)
    initMainChart(series)
    mainChart.showLoading()
}

const initMainChart = function (series = {}, addSeriesToChartManager = false, container = 'highcharts_container') {
    // loadChart()
    mainChart = Highcharts.chart(document.getElementById(container), {
        credits: {
            enabled: false
        },
        xAxis: {
            type: 'datetime'
        },
        plotOptions: {
            series: {
                pointStart: chartManager.pointStart,
                pointInterval: chartManager.pointInterval // one day
            }
        },
        legend: {
            enabled: true,
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            width: legendWidth
        },
        tooltip: tooltip,
        chart: {
            height: chartHeight + 40,
            type: 'line',
            zoomType: 'x',
            // animation: false,
            events: events,
            // spacingTop: 20
            x: -200,
        },

        title: {
            text: chart_title ? chart_title : "",
            style: {
                color: 'black',
                fontWeight: 'bold',
                "font-size": "30px"
            }
        },

        navigator: chartNavigator,
        rangeSelector: {
            x: 0,
            // floating: true,
            style: {
                color: 'black',
                fontWeight: 'bold',
                position: 'relative',
                "font-family": "Arial"
            },
            enabled: true,
            inputEnabled: false,
            // inputDateFormat: '%y',
            // inputEditDateFormat: '%y',
            buttons: [{
                type: 'hour',
                count: 1,
                text: 'H'
            },
                {
                    type: 'day',
                    count: 1,
                    text: 'D'
                },

                {
                    type: 'month',
                    count: 1,
                    text: 'M'
                },
                {
                    type: 'year',
                    count: 1,
                    text: 'Y'
                },

                {
                    type: 'all',
                    text: 'All',
                    align: 'right',
                    x: 1000,
                    y: 100,
                }],
        },

        series: series, // add a series otherwise it does not work
    });


    if (addSeriesToChartManager) {
        series.forEach(s => {
            chartManager.addSeries(s, false,)
        })
    }


    mainChart.update({
        chart: {
            events: {
                redraw: function () {
                    if (typeof updateCorrTable === 'function') {
                        console.log("redraw")
                        let series_to_show = mainChart.series.filter(s => s.visible && !(typeof s.name === "string" && s.name.includes("Navigator"))).map(s => s.name)
                        updateCorrTable(series_to_show)
                    }

                },
                load: function () {
                    if (typeof updateCorrTable === 'function') {
                        console.log("load")
                        let series_to_show = mainChart.series.filter(s => s.visible &&
                            !(typeof s.name === "string" &&
                                s.name.includes("Navigator"))).map(s => s.name)
                        updateCorrTable(series_to_show)
                    }
                },
            }
        },
    });


}


const fetchMainChartData = function (data_url) {
    return new Promise((resolve, reject) => {
        fetch(data_url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            }
        }).then(response => response.json())
            .then(data => {
                data.series.forEach(s => chartManager.addSeries(s, false))
                if (data.injected) {
                    data.injected.forEach(s => chartManager.addSeries(s, false, "injected"))
                }
                chartManager.resetSeries()
                resolve()


            }).catch(error => console.error(error))
    })
}



