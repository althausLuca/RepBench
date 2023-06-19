from django import forms

from repair import algo_mapper

error_choices = [("rmse", "RMSE"), ("mae", "MAE"), ("partial_rmse", "RMSE on anomaly")]


def hidden(initial):
    return forms.CharField(widget=forms.HiddenInput(), required=False, initial=initial)


class BayesianOptForm(forms.Form):
    n_initial_points = forms.IntegerField(label="Starting Samples", initial=20)
    n_initial_points.widget.attrs.update({"class": 'form-control', "title": "title"})

    n_calls = forms.IntegerField(label="Resampling", initial=20)
    n_calls.widget.attrs.update({"class": 'form-control'})
    error_loss = forms.CharField(label='Loss', widget=forms.Select(choices=error_choices))
    error_loss.widget.attrs.update({"class": 'form-control'})


def bayesian_opt_param_forms_inputs(df):
    b_param_forms = {}
    alg_input_map = {alg_name: alg().suggest_param_range(df) for alg_name, alg in algo_mapper.items()}
    for alg, param_range in alg_input_map.items():
        b_param_forms[alg] = [{"param_name": k, "min": min(v), "max": max(v)} for k, v in param_range.items()]
    return b_param_forms
