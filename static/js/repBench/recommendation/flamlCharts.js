const RecommendationChart = {
    chart: null,
    init: function () {
        this.chart = Highcharts.chart('flaml-chart', {

            chart: {
                type: 'column',
                height: 500,
            },
            plotOptions: {
                column: {
                    stacking: 'normal',
                    /*  dataLabels: {
                         enabled: true
                     } */
                },
                series: {
                    events: {
                        legendItemClick: function (e) {
                            e.preventDefault();
                        }
                    },
                }
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: [""],
                plotLines: [{
                    // color: 'red',
                    width: 3,
                    value: 0.5,
                    dashStyle: "dot"
                }],

            },
            yAxis: {
                min: 0,
                max: 1,
                title: {
                    text: 'Test Score'
                }
            },

            // plotOptions: {
            //     column: {
            //         borderWidth: 0
            //     },
            //
            // },
            credits: {
                enabled: false
            },

            series: [{name: "Estimator", color: "black", data: [0], showInLegend: false}, {
                name: "Optimal",
                color: "red",
                data: [0],
                showInLegend: true
            }]

        });
    },
    addData: function (score, estimator, iter, parameters) {
        let categories = this.chart.xAxis[0].categories
        if (!categories.includes(estimator)) {
            this.chart.xAxis[0].setCategories([...categories, estimator]);
            this.chart.series.filter(s => s.name === "Estimator")[0].addPoint(score)
            // if (iter === 0) {
            //     this.chart.series.filter(s => s.name === "Best")[0].addPoint(score)
            // }
        } else {
            let seriesData = this.chart.series.filter(s => s.name === "Estimator")[0].data
            seriesData[categories.indexOf(estimator)].update(score)

            // let bestSeries = this.chart.series.filter(s => s.name === "Best")[0]
            let best = seriesData[0]
            // console.log("best", best)
            if (score > best.y) {
                best.update({color: "red", y: score})
                categories[0] = "<b>" + estimator + "</b>"
            }
        }
    }
}

