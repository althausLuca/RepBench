from  django.db.utils import OperationalError
from django import forms

def get_data_set_choices():
    DATASET_CHOICES = []
    try:
        from RepBenchWeb.models import DataSet
        DATASET_CHOICES =  [ (dataset.title,dataset.title)   for dataset in DataSet.objects.all() ]
    except OperationalError:
        pass # to avoid migration errors

    return DATASET_CHOICES

def get_injected_data_set_choices():
    "Return a list of tuples (dataset_title,dataset_title)"
    INJECTED_DATASET_CHOICES = []
    try:
        from RepBenchWeb.models import InjectedContainer
        INJECTED_DATASET_CHOICES =  [ (dataset.title,dataset.title)   for dataset in InjectedContainer.objects.all()  if len(dataset.title) > 3]
    except OperationalError:
        pass  # to avoid migration errors

    return INJECTED_DATASET_CHOICES

def hiddenField(value):
    return forms.CharField(widget=forms.HiddenInput(), required=False, initial=value)


def parse_param_input(p: str):
    "convert string to int or float if possible"
    if p.isdigit():
        return int(p)
    try:
        return float(p)
    except:
        return p