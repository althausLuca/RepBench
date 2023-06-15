from django import forms
from RepBenchWeb.forms.utils  import get_data_set_choices , get_injected_data_set_choices


class DataSetsForm(forms.Form):
    dataset = forms.CharField(label='Dataset', widget=forms.Select(choices=get_data_set_choices(), attrs={
        "class": 'form-control', "id": "anomaly_id",
        "myInfo": "Select the dataset to be used."}))

class InjectedDataSetForm(forms.Form):
    dataset = forms.CharField(label='Dataset', widget=forms.Select(choices=get_injected_data_set_choices(), attrs={
        "class": 'form-control', "id": "selected_dataset_title",
        "myInfo": "Select the dataset to be used."}))
