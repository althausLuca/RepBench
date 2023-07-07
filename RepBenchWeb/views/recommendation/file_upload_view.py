import csv

import numpy as np
import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from RepBenchWeb.forms.file_upload import UploadFilesForm
from RepBenchWeb.models import DataSet


def django_file_to_pandas(uploaded_file: UploadedFile) -> pd.DataFrame:
    # Check if the file is comma or whitespace-separated
    uploaded_file.open('r')
    dialect = csv.Sniffer().sniff(uploaded_file.readline().decode('utf-8'))
    uploaded_file.seek(0)
    delimiter: str = dialect.delimiter

    print(delimiter)
    print(uploaded_file)
    df = pd.read_csv(uploaded_file, delimiter=delimiter)
    print(df)
    df.columns = [column.strip() for column in df.columns]
    print(df.columns)
    print([type(column) for column in df.columns])
    if any("." in column for column in df.columns):
        df = pd.read_csv(uploaded_file, delimiter=delimiter,header=None , names=[i for i in range(len(df.columns))])

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

            # recommendation = get_recommendation_non_containerized(df,
            #                                                       column_for_recommendation=column_for_recommendation)
            print(df)
            DataSet.objects.create(title=data_name, dataframe=df.to_json(), ref_url="-", description="-", url_text="-",
                                   granularity="1s")

    import RepBenchWeb.views.injection_view as injection_view
    return injection_view.InjectionView().get(request, setname=data_name)
