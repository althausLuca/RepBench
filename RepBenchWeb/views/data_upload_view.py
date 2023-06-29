from django.shortcuts import render

from RepBenchWeb.forms.file_upload import UploadFilesForm
from django.views import View


class UploadView(View):
    template = "upload.html"

    def get(self, request):
        context = {}
        context["upload_form"] = UploadFilesForm()
        return render(request, self.template, context=context)