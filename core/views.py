from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from markdown import markdown

def index(request):
    return render(request, "core/model.html")

def vizualization(request):
    return render(request,"core/State Map.html")

def vizualization2(request):
    return render(request,"core/State Map2.html")

def state(request,initials):
    return render(request,"core/state.html",{"state":get_object_or_404(State,initials=initials)})

def blog(request,bid):
    return render(request,"core/blogpost.html",{"blogpost":get_object_or_404(Blogpost,pk=bid),"text":markdown(get_object_or_404(Blogpost,pk=bid).content)})
