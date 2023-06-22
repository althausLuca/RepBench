from django.db import models

from RepBenchWeb.models import InjectedContainer


class OptimizationModel(models.Model):
    injected_container = models.ForeignKey(InjectedContainer, on_delete=models.CASCADE)

    aquisition_functions = models.JSONField(default=[])
    algorithms = models.JSONField(default=[])
    metrics = models.JSONField(default=[])
    initial_points = models.JSONField(default=[])


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)