from django import forms
from django.utils.safestring import mark_safe
from RepBenchWeb.forms.form_config import ANOMALY_CHOICES , ratio_choices , factor_choices

class RangeSliderInput(forms.TextInput):
    input_type = 'range'
    min_value = 5
    max_value = 100
    step = 1

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.pop('min_value', self.min_value)
        self.max_value = kwargs.pop('max_value', self.max_value)
        self.step = kwargs.pop('step', self.step)
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['min'] = self.min_value
        context['widget']['attrs']['max'] = self.max_value
        context['widget']['attrs']['step'] = self.step
        return context

    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs=attrs, renderer=renderer)
        html = f'<div class="slider-container">{html}' \
               f'<span id="slider-value">{50}</span>' \
               f'</div>'
        return html

class InjectionForm(forms.Form):
    anomaly = forms.CharField(label='Anomaly Type', widget=forms.Select(choices=ANOMALY_CHOICES, attrs={
        "class": 'form-control', "id": "anomaly_id",
        "myInfo": "Anomaly Type to infect the data with."}))

    ratio = forms.FloatField(label='Contamination', initial=0.1, widget=forms.Select(choices=ratio_choices,
        attrs={'id': "ratio_id", "class": 'form-control',
               "myInfo": "Ratio of the Time Series to be injected."}))
    # ratio = forms.FloatField(label='Contamination', initial=0.1, widget=NumberInput(
    #     attrs={'id': "ratio_id", 'min': 0, 'max': 1, "class": 'form-control',
    #            "myInfo": "Ratio of the Time Series to be injected."}))
    factor = forms.FloatField(label='Anomaly Scale', initial=3.5, widget=forms.Select(choices=factor_choices,
        attrs={ "class": 'form-control',
                "myInfo": "Standard deviation factor of the anomaly."}))
    # factor = forms.FloatField(initial=3, widget=NumberInput(
    #     attrs={'id': "ratio_id", 'min': 0, 'max': 30, "class": 'form-control',
    #            "myInfo": "Standard deviation factor of the anomaly."}))

    def __init__(self, data_columns, ts_name="bafu", *args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)

        self.fields["data_columns"] = forms.CharField(
            label=mark_safe("Time Series"),  # to add white space
            widget=forms.Select(attrs={"class": "form-control"}, choices=[(i, i) for i in data_columns]),
        )

        self.fields["data_set"] = forms.CharField(widget=forms.HiddenInput(), required=False, initial=ts_name)
        self.fields["seed"] = forms.IntegerField(label='Seed', required=False, widget=forms.HiddenInput(
            attrs={'title': 'Enter numbers Only', 'min': 0, 'step': 1, "class": 'form-control'}))


class store_injection_form(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description', max_length=1000, required=False
                                  , widget=forms.Textarea())

    class Meta:
        fields = ['title', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'cols': 4, 'rows': 2})
        }
