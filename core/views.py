from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, "core/model.html")

def vizualization(request):
    return render(request,"core/State Map.html")

def vizualization2(request):
    return render(request,"core/State Map2.html")
