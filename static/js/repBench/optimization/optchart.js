let optChart = null
let initOptChart = function (params, error, n_init, n_sample) {
    optChart = Highcharts.chart('optChartContainer', {
            tooltip: {
                shared: true,
                crosshairs: true
            },
            xAxis: {
                // label: {
                //     text: 'Iteration',
                //     style: {
                //         "font-size": "15px",
                //         transform: "translate(0, -37px)"
                //     },
                // },
                // plotBands: [{
                //     color: 'rgba(3, 11, 12, 0.2)',// Color value
                //     from: -0.2, // Start of the plot band
                //     to: n_init + 0.5, // End of the plot band
                //     label: {
                //         text: 'Initial Sampling',
                //         verticalAlign: 'middle',
                //         style: {
                //             "font-size": "15px"
                //         }
                //
                //     }, // Content of the label
                // }, {
                //     color: 'rgba(30, 11, 102, 0.2)',// Color value
                //     from: n_init + 0.5, // Start of the plot band
                //     to: n_init + n_sample, // End of the plot band
                //     y: 20,
                //     label: {
                //         text: 'Maximum Expectation Sampling',
                //         verticalAlign: 'middle',
                //         style: {
                //             "font-size": "15px",
                //         }
                //
                //     }, // Content of the label
                // }],
                labels: {
                    tickInterval: 1,
                    start: 1

                },
                max: n_init + n_sample,
            },
            title: {
                text: '',
            },
            yAxis: [{
                title: {
                    text: 'Parameters'
                },
                height: '43%',
                lineWidth: 2,
                decimalValues: 2,
            }, {
                title: {
                    text: error
                },
                top: '57%',
                height: '43%',
                offset: 0,
                lineWidth: 2,
                labels: {
                    formatter: function () {
                        return this.value.toFixed(2);
                    },
                },
            }],
            series: params.map(param => {
                return {
                    type: 'line',
                    name: param,
                    yAxis: 0,
                    data: []
                }
            }).concat([{
                //error chart
                showInLegend: false,
                type: 'line',
                // name: error,
                color: 'red',
                data: [],
                yAxis: 1,

            }])

        }
    );

    optChart.addParamError = function (params, error) {
        params.forEach((param, i) => {

            optChart.series[i].addPoint(param);
        })
        optChart.series[optChart.series.length - 1].addPoint(error)
    }
}

initOptChart([], 'RMSE', 20, 20)
