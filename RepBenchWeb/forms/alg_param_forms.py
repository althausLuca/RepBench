import numpy as np

from django import forms
from repair.algorithms_config import SPEEDandAcceleration, IMR, SCREEN, RPCA, CDREP, ALGORITHM_TYPES, SCR, KalmanFilter
from RepBenchWeb.forms.utils import hiddenField

ALGORITHM_CHOICES = [(a, a) for a in ALGORITHM_TYPES]


class AlgorithmsForm(forms.Form):
    algorithms = forms.MultipleChoiceField(label='Algorithmss',
                                           initial=[choice[1] for choice in ALGORITHM_CHOICES[:3]],
                                           widget=forms.CheckboxSelectMultiple(
                                               attrs={'class': 'multi-checkbox', "name": 'algorithms[]'}),
                                           choices=ALGORITHM_CHOICES,

                                           )


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
    alg_type = hiddenField(RPCA)


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
    alg_type = hiddenField(CDREP)


class SCREENparamForm(forms.Form):
    smin = forms.FloatField(help_text="Minimal change less than 0.", label='SMIN', initial=-0.5,
                            widget=forms.NumberInput(attrs={'max': "0", "step": "any", "class": 'form-control'}))
    smax = forms.FloatField(help_text="Maximal change greater than 0.", label='SMAX', initial=0.5,
                            widget=forms.NumberInput(attrs={'min': "0", "step": "any", "class": 'form-control'}))
    alg_type = hiddenField(SCREEN)


class IMRparamField(forms.Form):
    p = forms.FloatField(help_text="ARX parameter", label='p', initial=3,
                         widget=forms.NumberInput(attrs={'min': "1", "step": "1", "class": 'form-control'}))
    tau = forms.FloatField(help_text="Minimal change parameter", label='Tau', initial=0.01,
                           widget=forms.NumberInput(attrs={'min': "0.000001", "step": "any", "class": 'form-control'}))
    alg_type = hiddenField(IMR)


class SpeedAndAccelerationField(forms.Form):
    alg_type = hiddenField(SPEEDandAcceleration)
    # amin = forms.FloatField(help_text="Minimal change in acceleration less than 0.", label='AMIN', initial=-0.5,
    #                         widget=forms.NumberInput(attrs={'max': "0", "step": "any", "class": 'form-control'}))
    amax = forms.FloatField(help_text="Maximal change in acceleration greater than 0.", label='AMAX', initial=0.5,
                            widget=forms.NumberInput(attrs={'min': "0", "step": "any", "class": 'form-control'}))

    # smin = forms.FloatField(help_text="Minimal change less than 0.", label='SMIN', initial=-0.5,
    #                        widget=forms.NumberInput(attrs={'max': "0", "step": "any", "class": 'form-control'}))
    smax = forms.FloatField(help_text="Maximal change greater than 0.", label='SMAX', initial=0.5,
                            widget=forms.NumberInput(attrs={'min': "0", "step": "any", "class": 'form-control'}))


class SRCFForm(forms.Form):
    alg_type = hiddenField(SCR)
    THETA = forms.FloatField(help_text="Theta", label='Theta', initial=5,
                             widget=forms.NumberInput(attrs={'min': "0", "step": 1, "class": 'form-control'}))
    delta = forms.FloatField(help_text="Delta", label='Delta', initial=500,
                             widget=forms.NumberInput(attrs={'min': "0", "step": "any", "class": 'form-control'}))


class KalmanFilterFilterForm(forms.Form):
    alg_type = hiddenField(KalmanFilter)
    transition_cov = forms.FloatField(help_text="transition_covariance", label='Cov', initial=0.5,
                                      widget=forms.NumberInput(
                                          attrs={'min': 0, "step": 0.1, "max": 1, "class": 'form-control'}))


ParamForms = {"SCREEN": SCREENparamForm(), "RPCA": RPCAparamForm(), "CDrec": CDparamForm(), "IMR": IMRparamField()}
