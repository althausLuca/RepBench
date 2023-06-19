import numpy as np

from django import forms
from django.forms import NumberInput

from repair import algo_mapper
from repair.estimator import Estimator

type_form_mapper = {
    float: forms.FloatField,
    int: forms.IntegerField,
    str: forms.CharField,
    np.int32: forms.IntegerField,
    np.int64: forms.IntegerField,
    np.float32: forms.FloatField,
    np.float64: forms.FloatField,
}


def hidden(initial):
    return forms.CharField(widget=forms.HiddenInput(), required=False, initial=initial)


class RPCAparamForm(forms.Form):
    classification_truncation = forms.IntegerField(label='Truncation', required=False, initial=2,
                                                   widget=forms.NumberInput(
                                                       attrs={'placeholder': 2, 'min': "1", "step": "1",
                                                              "class": 'form-control'}))
    delta = forms.FloatField(label="Delta", min_value=0, initial=1.2, widget=forms.NumberInput(
        attrs={'min': "0", "step": "any", 'placeholder': '1.2', "class": 'form-control'}))
    threshold = forms.IntegerField(label='Threshold', required=False, initial=1,
                                   widget=forms.NumberInput(
                                       attrs={'min': "0", "step": "any", 'placeholder': '1', "class": 'form-control'}))
    alg_type = hidden("rpca")


class CDparamForm(forms.Form):
    classification_truncation = forms.IntegerField(label='Truncation', required=False, initial=2,
                                                   widget=forms.NumberInput(
                                                       attrs={'placeholder': 2, 'min': "1", "step": "1",
                                                              "class": 'form-control'}))

    delta = forms.FloatField(label="Delta", min_value=0, initial=1.2,
                             widget=forms.NumberInput(
                                 attrs={'min': "0", "step": "any", 'placeholder': '1.2', "class": 'form-control'}))

    threshold = forms.IntegerField(label='Threshold', required=False, initial=1,
                                   widget=forms.NumberInput(
                                       attrs={'min': "0", "step": "any", 'placeholder': '1', "class": 'form-control'}))
    alg_type = hidden("cdrec")


class SCREENparamForm(forms.Form):
    smin = forms.FloatField(help_text="Minimal change less than 0.", label='SMIN', initial=-0.5,
                            widget=forms.NumberInput(attrs={'max': "0", "step": "any", "class": 'form-control'}))
    smax = forms.FloatField(help_text="Maximal change greater than 0.", label='SMAX', initial=0.5,
                            widget=forms.NumberInput(attrs={'min': "0", "step": "any", "class": 'form-control'}))
    alg_type = hidden("screen")


class IMRparamField(forms.Form):
    p = forms.FloatField(help_text="ARX parameter", label='p', initial=3,
                         widget=forms.NumberInput(attrs={'min': "1", "step": "1", "class": 'form-control'}))
    tau = forms.FloatField(help_text="Minimal change parameter", label='Tau', initial=0.01,
                           widget=forms.NumberInput(attrs={'min': "0.000001", "step": "any", "class": 'form-control'}))
    alg_type = hidden("imr")
