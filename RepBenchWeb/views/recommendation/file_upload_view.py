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

    # Read the first few lines to infer if the first row contains column names or data
    first_line = uploaded_file.readline().decode('utf-8').strip()
    second_line = uploaded_file.readline().decode('utf-8').strip()
    uploaded_file.seek(0)

    has_header = csv.Sniffer().has_header(first_line + '\n' + second_line)

    # Read the file into a pandas DataFrame
    if has_header:
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
        for first_row_element in df.iloc[0,:]:
            if isinstance(first_row_element,float) or isinstance(first_row_element, np.float):
                df = pd.read_csv(uploaded_file, delimiter=delimiter, header=None)
                break
    else:
        df = pd.read_csv(uploaded_file, delimiter=delimiter, header=None)

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
            DataSet.objects.create(title=data_name, dataframe=df.to_json() , ref_url="-", description="-",url_text="-",granularity="1s")

    import RepBenchWeb.views.injection_view as injection_view
    return injection_view.InjectionView().get(request,setname =data_name )
