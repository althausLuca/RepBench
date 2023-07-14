let createBayesianOptFormData = function (form_id) {
    var e = document.getElementById("optFormAlgSelect");
    var algorithm = e.value;
    let form = document.getElementById(algorithm)
    let formData = new FormData(form)
    let form_b_opt = document.getElementById("bayesian_opt_form_params")
    const bayesienOptFormData = new FormData(form_b_opt)

    for (var pair of formData.entries()) {
        bayesienOptFormData.append(pair[0], pair[1]);
    }
    bayesienOptFormData.append('csrfmiddlewaretoken', csrftoken)
    bayesienOptFormData.append("injected_series", JSON.stringify(chartManager.get_injected_norm_data()))
    bayesienOptFormData.append("setname", setname)
    return bayesienOptFormData
}

let optimData = null
let optimizeCurrentData = (form_id) => {
    fetch(optimization_url, {
        method: 'POST',
        body: createBayesianOptFormData(form_id),
    }).then(response => response.json()).then(responseJson => {
        optimData = responseJson
        //textract error_loss from formdata
        let error_loss = optimData.error_loss.toUpperCase();
        let params = Object.keys(optimData.param_ranges);
        let n_initial_points = optimData.n_initial_points;
        let n_calls = optimData.n_calls;
        let job_id = optimData.job_id;
        initOptChart(params, error_loss, n_initial_points, n_calls)
        fetch_loop(n_initial_points, job_id)
    })
}

let create_job_id_form = function () {
    const empty_form = new FormData()
    empty_form.append('csrfmiddlewaretoken', csrftoken)
    return empty_form
}

let fetch_loop = function (n_initial_points, job_id) {
    // Get the CSRF token value from the cookie
    fetch(fetch_opt_result, {
        method: 'POST', // or 'PUT'
        body: create_job_id_form(),
    }).then(response => response.json()).then(
        response => {
            if (response.data.length > 0) {
                let params = response.data[response.data.length -1].param_combinations
                let param_names = Object.keys(params[0])
                SuccessiveHalvingChart.setParamNames(param_names[0], param_names[1])
                SuccessiveHalvingChart.update(params)
            }
            setTimeout(function () {
                fetch_loop(n_initial_points, job_id)
            }, 1000)
        })
}


