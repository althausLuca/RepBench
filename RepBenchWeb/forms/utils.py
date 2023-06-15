from  django.db.utils import OperationalError



def get_data_set_choices():
    DATASET_CHOICES = []
    try:
        from RepBenchWeb.models import DataSet
        DATASET_CHOICES =  [ (dataset.title,dataset.title)   for dataset in DataSet.objects.all() ]
    except OperationalError:
        pass # to avoid migration errors

    return DATASET_CHOICES

def get_injected_data_set_choices():
    INJECTED_DATASET_CHOICES = []
    try:
        from RepBenchWeb.models import InjectedContainer
        INJECTED_DATASET_CHOICES =  [ (dataset.title,dataset.title)   for dataset in InjectedContainer.objects.all() ]
    except OperationalError:
        pass  # to avoid migration errors

    return INJECTED_DATASET_CHOICES

