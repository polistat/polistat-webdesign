from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("Future Oracle of Blair Website")

def vizualization(request):
    return render(request,"core/State Map.html")
def vizualization2(request):
    return render(request,"core/State Map2.html")
