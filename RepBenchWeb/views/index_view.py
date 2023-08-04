
from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'index.html', context=context)

def about(request):
    context = {}
    return render(request, 'about.html', context=context)