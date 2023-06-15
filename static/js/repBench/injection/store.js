let createStoreFormData = function (selectionOnly = false) {
    console.log("store")
    const form = document.getElementById("storeForm")
    console.log(form)
    const storeFormData = new FormData(form)
    storeFormData.append('csrfmiddlewaretoken', csrftoken)
    storeFormData.append("injected_series", JSON.stringify(chartManager.get_injected_norm_data()))
    console.log(JSON.stringify(chartManager.get_injected_norm_data()))
    let {min, max} = chartManager.getMinMaxIndices();
    let visible = chartManager.originalSeries.filter(s => s._chartSeriesData.visible).map(s => s.name)
    storeFormData.append("min", min)
    storeFormData.append("max", max)
    storeFormData.append("visible_series", JSON.stringify(visible))
    if(selectionOnly) {
            storeFormData.append("selectionOnly", "selectionOnly")
    }
    return storeFormData
}

let store = (selectionOnly = false) => {
    console.log("store")
    fetch(store_url, {
        method: 'POST',
        body: createStoreFormData(selectionOnly),
    }).then(response => response.json()).then(responseJson => {
    })
}

document.getElementById("storeButton").addEventListener('click',() =>   store(false))
document.getElementById("storeSelectionButton").addEventListener('click', () => store(true))
