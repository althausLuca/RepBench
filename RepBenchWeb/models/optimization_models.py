from django.db import models

from RepBenchWeb.models import InjectedContainer


class OptimizationModel(models.Model):
    injected_container = models.Field(InjectedContainer)
    aquisition_functions = models.JSONField(default=list)
    algorithms = models.JSONField(default=list)
    metrics = models.JSONField(default=dict)
    initial_points = models.JSONField(default=list)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)