let createRepairRequestFormData = function (alg) {
    const form = document.getElementById(alg)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    repairFormData.append("injected_series", JSON.stringify(chartManager.get_injected_norm_data()))
    return repairFormData
}

let repairResult = null
let repair = (alg) => {
    createScoreBoard()
    chartManager.hideNoneInjectedSeries()
    mainChart.showLoading()
    fetch(repair_url, {
        method: 'POST',
        body: createRepairRequestFormData(alg),
    }).then(response => response.json()).then(responseJson => {
        const repSeries = responseJson.repaired_series
        const scores = responseJson.scores
        repairResult = repSeries


        const chartRepairSeries = Object.keys(repSeries).map(key => {
            let repair = repSeries[key]
            console.log(repair)
            return chartManager.addSeries(repair,true,"repair")
        })
        console.log(scores)
        // chartManager.resetSeries(true)
        scores["color"] = mainChart.series[mainChart.series.length-2].color
        updateScoreBoard(scores)

    }).finally( () => {
                mainChart.hideLoading()
    }
    )
}
