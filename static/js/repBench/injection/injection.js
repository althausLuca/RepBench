let createInjectFormData = function (form_id) {
    let form = document.getElementById(form_id)
    let formData = new FormData(form)
    return formData
}

const inject = function (injectionURL) {
    const formData = createInjectFormData('injectionForm')
    const columnsToInject = [...formData.getAll('data_columns')]
    const promises = []
    columnsToInject.forEach(val => {
        formData.set('data_columns', val)
        promises.push(
            fetch(injectionURL, {
                method: 'POST',
                body: formData,
            }).then(response => response.json()).then(responseJson => {
                //delete old series
                let s = responseJson.injected_series
                //remove old series in the same column
                if (mainChart.get(s["id"])) {
                    let previously_injected = chartManager.injectedSeries.filter(inj_s => inj_s._chartSeriesData.id === s["id"])[0]
                    // merge the two series
                    previously_injected.originalData.forEach((val, idx) => {
                        if (s["data"][idx] === null) {
                            s["data"][idx] = val
                            s["norm_data"][idx] = previously_injected.normData[idx]
                        }
                    })
                    chartManager.removeSeries(s["id"])
                }

                chartManager.addSeries(s, true, "injected")
            })
        )

    })
    Promise.all(promises).then(() => {
        // resetSeries()
    })
    return false
}

// init injection_form

// $('#length-slider').on('input', function () {
//     var value = $(this).val();
//     $('#slider-value').text(' ' + value + ' ');
// });
//
//
// const select = document.getElementById('anomaly-select');
// const slider = document.getElementById('range-slider');
//
// select.addEventListener('change', () => {
//     console.log("SELECTED");
//     const value = select.value;
//     if (value === 'outlier') {
//         slider.step = '0';
//     } else {
//         slider.step = '1';
//     }
// });
