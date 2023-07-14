import csv

import numpy as np
import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from RepBenchWeb.forms.file_upload import UploadFilesForm
from RepBenchWeb.models import DataSet


def django_file_to_pandas(uploaded_file: UploadedFile) -> pd.DataFrame:
    # Check if the file is comma or whitespace-separated
    uploaded_file.open('r')

    first_line = uploaded_file.readline().decode('utf-8')
    dialect = csv.Sniffer().sniff(first_line)
    # uploaded_file.seek(0)
    delimiter: str = dialect.delimiter

    print("first line", first_line)
    print(delimiter)

    if "." in first_line:
        # print("float detected no header applied")
        df = pd.read_csv(uploaded_file, delimiter=delimiter,header=None)
        print(df)
    else:
        # print("HAAAAAS HEADER")
        df = pd.read_csv(uploaded_file, delimiter=delimiter, header=None , names=[column.strip() for column in first_line.split(delimiter)])
    print(df)
    return df


def upload_files(request):
    upload_form = UploadFilesForm()
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if True:
            file1 = request.FILES['file1']
            print(request.FILES)
            print(dict(request.POST))
            data_name = request.POST.get('title')
            df = django_file_to_pandas(file1)
            granularity = request.POST.get('granularity')
            ref_url = request.POST.get('ref_url')
            url_text = request.POST.get('url_text')
            description = request.POST.get('description')
            # recommendation = get_recommendation_non_containerized(df,
            #                                                       column_for_recommendation=column_for_recommendation)
            # print(df)
            DataSet.objects.create(title=data_name, dataframe=df.to_json(), ref_url=ref_url, description=description, url_text=url_text,
                                   granularity=granularity)

    import RepBenchWeb.views.injection_view as injection_view
    return injection_view.InjectionView().get(request, setname=data_name)
