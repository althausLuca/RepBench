function getPointCategoryName(point, dimension) {
    var series = point.series,
        isY = dimension === 'y',
        axis = series[isY ? 'yAxis' : 'xAxis'];
    return axis.categories[point[isY ? 'y' : 'x']];
}


// const warm_colors = ['rgb(255,205,116)', 'rgb(255,202,123)', 'rgb(255,114,81)', 'rgb(155,41,72)']

function getRGBColor(value) {
    // normalize value to range between 0 and 1
    const normalizedValue = (value + 1) / 2;
    const absValue = Math.abs(value);

    // if (value > 0) {
    //     if (value > 0.8){ return 'rgb(155,41,72,' + value + ')'}
    //     if (value > 0.6){
    //         return `rgb(${255}, ${114}, ${81}, ${255*value})`;
    //     }
    //     return `rgb(${255}, ${114}, ${81}, ${value})`;
    // }

    const blue = 0 // value > 0 ? 0 : Math.round(255);
    const green =  value < 0 ? 0 : Math.round(155)
    const red =  value > 0 ? 0 : Math.round(255)
    return `rgb(${red}, ${green}, ${blue} , ${Math.pow(absValue,1.5)})`;
}


initCorrTable = function (categories, data, id) {
    Highcharts.chart(id, {
        chart: {
            type: 'heatmap',
            marginTop: 40,
            marginBottom: 80,
        },
        credits: {
            enabled: false
        },
        title: {
            text: 'Time Series Correlation'
        },

        xAxis: {
            categories: categories
        },

        yAxis: {
            categories: categories,
            reversed: true
        },

        accessibility: {
            point: {
                descriptionFormatter: function (point) {
                    var ix = point.index + 1,
                        xName = getPointCategoryName(point, 'x'),
                        yName = getPointCategoryName(point, 'y'),
                        val = point.value;
                    return 'Corr between' + xName + 'and' + yName + ':' + val;
                }
            }
        },

        colorAxis: {
            stops: [
                [0, getRGBColor(-1)],
                [0.1, getRGBColor(-1+0.1*2)],
                [0.2, getRGBColor(-1+0.2*2)],
                [0.3, getRGBColor(-1+0.3*2)],
                [0.4, getRGBColor(-1+0.4*2)],
                [0.5, getRGBColor(-1+0.5*2)],
                [0.6, getRGBColor(-1+0.6*2)],
                [0.7, getRGBColor(-1+0.7*2)],
                [0.8, getRGBColor(-1+0.8*2)],
                [0.9, getRGBColor(-1+0.9*2)],
                [1, getRGBColor(1)],
            ],
            min: -1,
            max: 1,
            reversed: false
        },

        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 25,
            symbolHeight: 280
        },

        tooltip: {
            formatter: function () {
                return 'Corr(' + getPointCategoryName(this.point, 'x') + ',' +
                    '' + getPointCategoryName(this.point, 'y')
                    + '): <b>' + this.point.value + '</b>';
            }
        },

        series: [{
            name: 'Correlation',
            borderWidth: 0,
            data: corr_data.map(function (point) {
                return {
                    x: point[0],
                    y: point[1],
                    value: point[2],
                    color: getRGBColor(point[2])
                };
            }),
            dataLabels: {
                enabled: false,
                color: '#000000',
                borderWidth: 0,

            }
        }],

        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    yAxis: {
                        title: {
                            enabled: false
                        },
                        labels: {
                            formatter: function () {
                                return this.value;
                            }
                        }
                    }
                }
            }]
        }

    });
}
