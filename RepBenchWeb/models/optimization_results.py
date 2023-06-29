
from django.db import models



class SucessiveHalvingResults(models.Model):
    data_set_title = models.CharField(max_length=100,required=True)
    parameters = models.JSONField(default=[])
    alg_name = models.CharField(max_length=100,required=True)
    data = models.JSONField(default=[])
    data_description = models.CharField(max_length=1000,default="")
    "(param1_name  ,param2_name, param1_value, param2_value) => data : {}"

    def addData(self,data):
        data = self.data
        data.append(data)
        self.data = data
        self.save()
