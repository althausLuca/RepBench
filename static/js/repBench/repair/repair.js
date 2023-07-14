let createRepairRequestFormData = function (form_id) {
    const form = document.getElementById(form_id)
    const repairFormData = new FormData(form)
    repairFormData.append('csrfmiddlewaretoken', csrftoken)
    repairFormData.append("injected_series", JSON.stringify(chartManager.get_injected_norm_data()))
    return repairFormData
}

let repairResult = null
let repair = (form_id) => {
    let repairForm = createRepairRequestFormData(form_id)
    createScoreBoard()
    chartManager.hideNoneInjectedSeries()
    mainChart.showLoading()
    fetch(repair_url, {
        method: 'POST',
        body: repairForm,
    }).then(response => response.json()).then(responseJson => {
        const repSeries = responseJson.repaired_series
        const scores = responseJson.scores
        repairResult = repSeries


        const chartRepairSeries = Object.keys(repSeries).map(key => {
            let repair = repSeries[key]
            return chartManager.addSeries(repair,true,"repair")
        })
        // chartManager.resetSeries(true)
        scores["color"] = mainChart.series[mainChart.series.length-2].color
        updateScoreBoard(scores)

    }).finally( () => {
                mainChart.hideLoading()
    }
    )
}
