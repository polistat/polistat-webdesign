from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse

def index(request):
    return render(request, "core/model.html")

def vizualization(request):
    return render(request,"core/State Map.html")

def vizualization2(request):
    return render(request,"core/State Map2.html")

def state(request,initials):
    return render(request,"core/state.html",{"state":get_object_or_404(State,initials=initials)})
