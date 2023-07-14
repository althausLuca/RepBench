let probabilityChart = null
let scoreChart = null

const ProbabilityChart = {
    chart: null,
    init: function (chartHeight_) {
        // Create an empty chart using Highcharts
        this.chart = Highcharts.chart('probabilities-chart', {
            chart: {
                type: 'column',
                height: chartHeight_
            },
            title: {
                text: ''
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: [],
                title: {
                    text: 'Algorithm'
                }
            },
            yAxis: {
                min: 0,
                max: 1,
                title: {
                    text: 'Probability'
                }
            },
            plotOptions: {
                column: {
                    dataLabels: {
                        enabled: true,
                        format: '{point.y:.2f}'
                    }
                }
            },
            series: [{
                showInLegend: false,
                name: 'Probability',
                data: [],
            }]
        });
    },

    update: function (probabilities) {
        const categories = Object.keys(probabilities).sort();
        this.chart.xAxis[0].setCategories(categories);
        const data = categories.map(function (key) {
            return {
                name: key,
                y: probabilities[key]
            };
        });

        // Update the chart data
        this.chart.series[0].setData(data);
    }
};


//
// const createErrorChart = function (alg_scores) {
//     console.log("CREATE ERROR CHART" , alg_scores)
//   const categories = Object.keys(alg_scores);
//   const maeData = categories.map((category) => alg_scores[category].MAE);
//   const rmseData = categories.map((category) => alg_scores[category].RMSE);
//   const rmseAnomalyData = categories.map((category) => alg_scores[category]["RMSE on Anomaly"]);
//   // const originalRmseData = categories.map((category) => alg_scores[category].original_RMSE);
//
//   scoreChart = Highcharts.chart('alg-scores-chart', {
//     chart: {
//       type: 'column',
//       height: chartHeight
//     },
//     title: {
//       text: ''
//     },
//     xAxis: {
//       categories: categories
//     },
//     yAxis: {
//       title: {
//         text: 'Error Value'
//       }
//     },
//     legend: {
//       // align: 'top',
//       verticalAlign: 'top',
//       // layout: 'vertical'
//     },
//     plotOptions: {
//       series: {
//         borderWidth: 0,
//         dataLabels: {
//           enabled: true,
//           format: '{point.y:.4f}'
//         }
//       }
//     },
//     series: [
//       {
//         name: 'MAE',
//         data: maeData
//       },
//       {
//         name: 'RMSE',
//         data: rmseData
//       },
//       {
//         name: 'RMSE on Anomaly',
//         data: rmseAnomalyData
//       },
//     ]
//   });
// };

const ErrorChart = {
    chart: null,
    init: function (chartHeight) {
        this.chart = Highcharts.chart('alg-scores-chart', {
            chart: {
                type: 'column',
                height: chartHeight
            },
            title: {
                text: ''
            },
            xAxis: {
                categories: [],
                title: {
                    text:"Algorithm"
                }
            },
             credits: {
                enabled: false
            },
            yAxis: {
                title: {
                    text: 'Error Value'
                },
                min: 0,
                max: 1
            },
            legend: {
                verticalAlign: 'top'
            },
            plotOptions: {
                series: {
                    borderWidth: 0,
                    dataLabels: {
                        enabled: true,
                        format: '{point.y:.4f}'
                    }
                }
            },
            series: [
                {
                    name: 'MAE',
                    data: []
                },
                {
                    name: 'RMSE',
                    data: []
                },
                {
                    name: 'RMSE on Anomaly',
                    data: []
                }
            ]
        });
    },

    update: function (alg_scores) {
        const categories = Object.keys(alg_scores).sort();
        const maeData = categories.map(category => alg_scores[category].MAE);
        const rmseData = categories.map(category => alg_scores[category].RMSE);
        const rmseAnomalyData = categories.map(category => alg_scores[category]['RMSE on Anomaly']);


        const allData = [...maeData, ...rmseData, ...rmseAnomalyData];
        const maxOverall = Math.max(...allData);

        const data = [
            {name: 'MAE', data: maeData},
            {name: 'RMSE', data: rmseData},
            {name: 'RMSE on Anomaly', data: rmseAnomalyData}
        ];
        this.chart.yAxis[0].update({max: maxOverall*1.2})
        this.chart.xAxis[0].setCategories(categories);
        this.chart.series.forEach((series, index) => series.setData(data[index].data));
    }
};