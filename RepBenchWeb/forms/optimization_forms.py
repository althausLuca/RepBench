from django import forms

from repair import algo_mapper
from repair import algorithms_config as ac

error_choices = [("rmse", "RMSE"), ("mae", "MAE"), ("partial_rmse", "RMSE on anomaly")]


def hidden(initial):
    return forms.CharField(widget=forms.HiddenInput(), required=False, initial=initial)


class BayesianOptForm(forms.Form):
    n_initial_points = forms.IntegerField(label="Starting Samples", initial=5,
                                          widget=forms.Select(choices=[(i,i) for i in [1,5,10]]))
    n_initial_points.widget.attrs.update({"class": 'form-control', "title": "title"})
    n_calls = forms.IntegerField(label="Resampling", initial=20)
    n_calls.widget.attrs.update({"class": 'form-control'})
    # error_loss = forms.CharField(label='Loss', widget=forms.Select(choices=error_choices))
    # error_loss.widget.attrs.update({"class": 'form-control', "style": "display:none;;"})


def infer_step_size(min, max):
    ## check if min or max are floating point values float or numpy flaot
    if isinstance(min, float) or isinstance(max, float):
        return (max - min) / 10
    else:
        return 1


def optimization_param_forms_inputs(df):
    b_param_forms = {}
    alg_input_map = {alg: algo_mapper[alg]().suggest_param_range(df) for alg in ac.ALGORITHM_TYPES}
    for alg, param_range in alg_input_map.items():
        b_param_forms[alg] = [
            {"param_name": k, "min": min(v), "max": max(v), "step": infer_step_size(min(v), max(v)), "label": k}
            for k, v in param_range.items()]
    return b_param_forms


RPCA = "RPCA"


