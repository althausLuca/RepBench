// let optChart = null
// let initOptChart = function (params, error, n_init, n_sample) {
//     optChart = Highcharts.chart('optChartContainer', {
//             tooltip: {
//                 shared: true,
//                 crosshairs: true
//             },
//             xAxis: {
//                 labels: {
//                     tickInterval: 1,
//                     start: 1
//
//                 },
//                 max: n_init + n_sample,
//             },
//             title: {
//                 text: '',
//             },
//             yAxis: [{
//                 title: {
//                     text: 'Parameters'
//                 },
//                 height: '43%',
//                 lineWidth: 2,
//                 decimalValues: 2,
//             }, {
//                 title: {
//                     text: error
//                 },
//                 top: '57%',
//                 height: '43%',
//                 offset: 0,
//                 lineWidth: 2,
//                 labels: {
//                     formatter: function () {
//                         return this.value.toFixed(2);
//                     },
//                 },
//             }],
//             series: params.map(param => {
//                 return {
//                     type: 'line',
//                     name: param,
//                     yAxis: 0,
//                     data: []
//                 }
//             }).concat([{
//                 //error chart
//                 showInLegend: false,
//                 type: 'line',
//                 // name: error,
//                 color: 'red',
//                 data: [],
//                 yAxis: 1,
//
//             }])
//
//         }
//     );
//
//     optChart.addParamError = function (params, error) {
//         params.forEach((param, i) => {
//
//             optChart.series[i].addPoint(param);
//         })
//         optChart.series[optChart.series.length - 1].addPoint(error)
//     }
// }
//
// initOptChart([], 'RMSE', 20, 20)
