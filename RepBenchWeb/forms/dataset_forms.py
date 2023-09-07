from django import forms
from RepBenchWeb.forms.utils  import get_data_set_choices , get_injected_data_set_choices


class DataSetsForm(forms.Form):
    dataset = forms.CharField(label='Dataset', widget=forms.Select(choices=get_data_set_choices(), attrs={
        "class": 'form-control', "id": "selected_dataset_title",
        "myInfo": "Select the dataset to be used."}))



class InjectedDataSetForm(forms.Form):
    dataset = forms.CharField(
        label='Dataset',
        initial= None if len(get_injected_data_set_choices()) == 0 else get_injected_data_set_choices()[0],
        widget=forms.Select(
            choices=get_injected_data_set_choices(),
            attrs={
                "class": 'form-control',
                "id": "selected_dataset_title",
                "myInfo": "Select the dataset to be used."
            }
        )
    )

    # def __init__(self, *args, **kwargs):
    #     initial_dataset = kwargs.pop('initial_dataset', None)
    #     super(InjectedDataSetForm, self).__init__(*args, **kwargs)
    #     if initial_dataset:
    #         self.fields['dataset'].initial = initial_dataset
