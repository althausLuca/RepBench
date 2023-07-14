
//
// const display_recommendation_results = function (data, wait_for_chart) {
//     console.log("display recommendation results", data)
//     recommendationResults = data
//
//     document.getElementById("rec_info").style.display = "block"
//     document.getElementById("used_classifier").innerHTML = "<b>" + data.used_estimator + "</b>"
//     document.getElementById("recommended_algorithm").innerHTML = "<b>" + data.recommended_algorithm + "</b>"
//     if (data.hasOwnProperty("alg_score")) {
//         createErrorChart(data.alg_score)
//     }
//
//     createProbabilityChart(data.probabilities)
//     if (wait_for_chart) {
//         console.log("add repaired series")
//         Promise.all([mainChartFetchPromise]).then(() => {
//             Object.entries(data.alg_repairs).forEach(([k, v]) => {
//                 rep_series = Object.values(v)[0]
//                 rep_series.visible = k === data.recommended_algorithm
//                 rep_series.legendIndex = k === data.recommended_algorithm ? -2 : -1
//                 console.log("repseries", rep_series)
//                 chartManager.addSeries(rep_series, false, "repair")
//             });
//         })
//     } else {
//         Object.entries(data.alg_repairs).forEach(([k, v]) => {
//             rep_series = Object.values(v)[0]
//             rep_series.visible = k === data.recommended_algorithm
//             rep_series.legendIndex = k === data.recommended_algorithm ? -2 : -1
//             console.log("repseries", rep_series)
//             chartManager.addSeries(rep_series, false, "repair")
//         });
//     }
//     chartManager.resetSeries(true)
//
// }
//
//
// console.log("recommendation url", recommendation_url)
// if (typeof recommendation_url !== 'undefined') {
//     console.log("recommendation url", recommendation_url)
//     const recommendationFetchPromise = new Promise((resolve, reject) => {
//         fetch(recommendation_url, {
//             method: 'GET',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': '{{ csrf_token }}'
//             }
//         }).then(response => response.json()).then(data => {
//             recommendationResults = data
//             display_recommendation_results(data, true)
//             resolve()
//         }).catch(error => console.error(error))
//     })
// }

//
// let repair = (alg) => {
//     createScoreBoard()
//
//     fetch(repair_url, {
//         method: 'POST',
//         body: createRepairRequestFormData(alg),
//     }).then(response => response.json()).then(responseJson => {
//         const repSeries = responseJson.repaired_series
//         const scores = responseJson.scores
//         repairResult = repSeries
//         let color = null
//         repairedSeries.length  = 0
//         const chartRepairSeries = Object.keys(repSeries).map(key => {
//             let repair = repSeries[key]
//             return addRepairedSeries(repair,color)
//         })
//         updateScoreBoard(scores)
//
//         resetSeries(true)
//         scores["color"] = mainChart.series[mainChart.series.length-2].color
//
//
//     })
// }
