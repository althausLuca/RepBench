# automl_settings = {
#     "time_budget": time_budget,  # in seconds
#     "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
#     "task": 'classification',
#     "log_file_name": "recommendation/logs/flaml.log",
#     "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
# }

from django import forms

ESTIMATOR_CHOICES = [
    ('lgbm', 'LGBM'),
    ('rf', 'Random Forest'),
    ('xgboost', 'XGBoost'),
    ('extra_tree', 'Extra Tree'),
    ('lrl1', 'Logisitc Regression')
]

RayTunes_ESTIMATOR_CHOICES = [
    ('LGBM', 'LGBM'),
    ('RandomForest', 'Random Forest'),
    ('ExtraTrees', 'Extra Tree'),
    ('LogisticRegression', 'Logistic Regression')
]

RAYTUNES_OPTIMIZER_CHOICES = [("hyperopt", "HyperOpt"), ("nevergrad", "NeverGrad"), ("ZOOpt", "ZOOpt"),
                              ("default", "Default(GridSearch)")]

FEATURE_CHOICES = [("catch22", "Catch22"), ("tsfresh_selected", "TSFresh") ,("tsfel" , "TSFEL") ]
METRIC_CHOICES = [('accuracy', 'Accuracy'), ('micro_f1', 'Micro F1'), ('macro_f1', 'Macro F1')]
TASK_CHOICES = [('classification', 'classification')]  # add more if needed
DATA_FRACTION_CHOICES = [('20', '20%'), ('40', '40%'), ('60', '60%'), ('80', '80%'), ('100', '100%')]

class FLAMLSettingsForm(forms.Form):
    time_budget = forms.IntegerField(label='Time Budget (seconds)', initial=60, widget=forms.NumberInput(
        attrs={'id': "time_budget_id", 'min': 0, "class": 'form-control'}))
    # metric = forms.CharField(label='Metric', initial='accuracy', widget=forms.Select(choices=METRIC_CHOICES, attrs={
    #     "class": 'form-control'}))
    # task = forms.CharField(initial='classification', widget=forms.HiddenInput(), required=False)
    estimator_list = forms.MultipleChoiceField(label='Estimators',
                                               initial=[choice[1] for choice in ESTIMATOR_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': 'multi-checkbox', "name": 'estimator_list[]'}),
                                               choices=ESTIMATOR_CHOICES
                                               )

    # todo make selection of features work
    features = forms.MultipleChoiceField(label='Feature Extrators',
                                         initial=[choice[0] for choice in FEATURE_CHOICES[:2]],
                                         widget=forms.CheckboxSelectMultiple(
                                             attrs={'class': 'kt-checkbox', "name": 'estimator_list[]'}),
                                         choices=FEATURE_CHOICES
                                         )

    # data_fraction = forms.CharField(label='Train Data Fraction', initial='100', widget=forms.Select(
    #     choices=DATA_FRACTION_CHOICES, attrs={"class": 'form-control'}))


    def __init__(self, *args, **kwargs):
        super(FLAMLSettingsForm, self).__init__(*args, **kwargs)
        self.fields['estimator_list'].initial = [choice[0] for choice in ESTIMATOR_CHOICES]


class RayTuneSettingsForm(forms.Form):
    # ray_tunes_time_budget = forms.IntegerField(label='Time Budget (secondss)', initial=60, widget=forms.NumberInput(
    #     attrs={'id': "time_budget_id", 'min': 0, "class": 'form-control'}))

    # task = forms.CharField(initial='classification', widget=forms.HiddenInput(), required=False)
    ray_tunes_estimator_list = forms.CharField(label='Estimator',
                                               widget=forms.Select(
                                                   attrs={'class': 'form-control', "name": 'estimator'},
                                                   choices=RayTunes_ESTIMATOR_CHOICES)
                                               )

    ray_tunes_optimizer = forms.CharField(label='Optimizer', initial='default', widget=forms.Select(
        choices=RAYTUNES_OPTIMIZER_CHOICES, attrs={"class": 'form-control'}))  # add more if needed

    ray_tunes_features = forms.MultipleChoiceField(label='Feature Extrators',
                                         initial=[choice[0] for choice in FEATURE_CHOICES[:2]],
                                         widget=forms.CheckboxSelectMultiple(
                                             attrs={'class': 'kt-checkbox', "name": 'estimator_list[]'}),
                                         choices=FEATURE_CHOICES
                                         )
    # ray_tunes_metric = forms.CharField(label='Metric', initial='accuracy',
    #                                    widget=forms.Select(choices=METRIC_CHOICES, attrs={
    #                                        "class": 'form-control'}))

    # ray_tunes_features = forms.ChoiceField(label='Features',
    #                                        initial=[choice[0] for choice in FEATURE_CHOICES],
    #                                        widget=forms.CheckboxSelectMultiple(
    #                                            attrs={'class': 'kt-checkbox', "name": 'estimator_list[]'}),
    #                                        choices=FEATURE_CHOICES
    #                                        )
    # ray_tunes_features = forms.IntegerField(widget=forms.NumberInput(attrs={'type': 'range', 'min': '0', 'max': '100', 'step': '1'}))
    # ray_tunes_data_fraction = forms.CharField(label='Train Data Fraction', initial='100', widget=forms.Select(
    #     choices=DATA_FRACTION_CHOICES, attrs={"class": 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(RayTuneSettingsForm, self).__init__(*args, **kwargs)
