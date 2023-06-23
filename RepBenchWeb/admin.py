from django.contrib import admin

# Register your models here.
from .models import DataSet , InjectedContainer , TaskData
admin.site.register(DataSet)
admin.site.register(InjectedContainer)
admin.site.register(TaskData)
