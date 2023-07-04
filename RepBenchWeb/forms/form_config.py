import numpy as np
from django import forms

## injection
ANOMALY_CHOICES = [
    ("shift", "Shift"),
    ("outlier", "Outlier"),
    ("distortion", "Distortion"),
]

ratio_choices = [( 0.05,"low") , ( 0.1,"medium"), (0.2,"large")]
factor_choices = [(2,"small"), (3.5,"medium"), (6,"large")]



METRIC_CHOICES = [("rmse", "RMSE"), ("mae", "MAE"), ("partial_rmse", "RMSE on anomaly")]


type_form_mapper = {
    float: forms.FloatField,
    int: forms.IntegerField,
    str: forms.CharField,
    np.int32: forms.IntegerField,
    np.int64: forms.IntegerField,
    np.float32: forms.FloatField,
    np.float64: forms.FloatField,
}


## Optimization forms Values
