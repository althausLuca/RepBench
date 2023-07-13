from django import forms

class UploadFilesForm(forms.Form):
    file1 = forms.FileField(label="DataFile (Required)",
                            widget=forms.ClearableFileInput(
                                attrs={'placeholder': 'No file selected', "class": "form-control"}))
    title = forms.CharField(label="Data Name (Required)", max_length=100,
                                widget=forms.TextInput(
                                    attrs={"class": "form-control"}))

    granularity = forms.CharField(label="Granularity (Required)", max_length=100, initial="1s",
                                  widget=forms.TextInput(
                                      attrs={"class": "form-control"}))

    description = forms.CharField(label="Description (Required)", max_length=100, initial="No Description",
                                  widget=forms.TextInput(
                                      attrs={"class": "form-control"}))
    ref_url = forms.CharField(label="Reference URL (Required)", max_length=100, initial="No Reference URL",
                              widget=forms.TextInput(
                                  attrs={"class": "form-control"}))
    url_text = forms.CharField(label="URL Text (Required)", max_length=100, initial="-",
                               widget=forms.TextInput(
                                      attrs={"class": "form-control"}))

    injected_data = forms.FileField(label="Anomalous File", required=False,
                            widget=forms.ClearableFileInput(
                                attrs={'placeholder': 'No file selected', "class": "form-control"}))
    # file2 = forms.FileField(label="File 2 (Optional)", required=False)
    # file3 = forms.FileField(label="File 3 (Optional)", required=False)
