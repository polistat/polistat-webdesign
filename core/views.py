from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from markdown import markdown
import json


def index(request):
	prediction = NationalPrediction.objects.latest('timestamp')
	predictions = NationalPrediction.objects.order_by('timestamp').all()
	model = {}
	for state in State.objects.all():
		pred = state.predictions.latest('timestamp')
		model[state.initials] = {"voteshare_inc": pred.mean, "voteshare_chal": 1 - pred.mean, "winstate_inc": state.trump, "winstate_chal": state.biden}
	return render(request, "core/model.html", {"model": json.dumps(model), "prediction": prediction, "timeseries": {"biden": repr(list(map(lambda p: p.dem_win, predictions))), "trump": repr(list(map(lambda p: p.rep_win, predictions)))}})

def state(request,initials):
	cd2 = False
	if len(initials) > 2 and initials[2] == "2":
		cd2 = True
		initials = initials[:2]
	obj = get_object_or_404(State,initials=initials)
	trump = obj.trump if not cd2 else obj.trump2
	biden = obj.biden if not cd2 else obj.biden2
	mean = obj.mean if not cd2 else obj.mean2
	predictions = obj.predictions if not cd2 else obj.predictions2
	bpi = obj.bpi if not cd2 else obj.bpi2
	result = 'trump' if trump >= 55 else ('biden' if biden >= 55 else 'tossup')
	return render(request, "core/state.html", {"trump": trump, "biden": biden, "bpi": bpi, "mean": mean, "CD2": cd2, "pollavg": ("+" if mean >= 50 else "")+"{:.1f}".format(mean - 50), "state": obj, "result": result, "trumpv": mean, "bidenv": 100-mean, "timeseries": {"biden": repr(list(map(lambda p: p.percent_biden, predictions.order_by('timestamp').all()))), "trump": repr(list(map(lambda p: p.percent_trump, predictions.order_by('timestamp').all())))}})

def blog(request,bid):
    return render(request,"core/blogpost.html",{"blogpost":get_object_or_404(Blogpost,pk=bid),"text":markdown(get_object_or_404(Blogpost,pk=bid).content)})

def methods(request):
    return render(request,"core/methods.html",{"methods":markdown(open("core/templates/core/methods.txt",encoding="utf-8").read(),extensions=["footnotes"])})
