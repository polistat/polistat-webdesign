from django.shortcuts import render, get_object_or_404
from .models import *
from django.http import HttpResponse
from markdown import markdown
import json


def index(request):
	prediction = NationalPrediction.objects.latest('timestamp')
	predictions = NationalPrediction.objects.order_by('timestamp').all()
	tossups = State.objects.filter(trump__lt=55, biden__lt=55)
	cd2tossups = State.objects.filter(trump2__gt=0, trump2__lt=55, biden2__lt=55)
	print(cd2tossups)
	model = {}
	for state in State.objects.all():
		model[state.initials] = {"voteshare_inc": state.mean, "voteshare_chal": 1 - state.mean, "winstate_inc": state.trump, "winstate_chal": state.biden}
	return render(request, "core/model.html", {"tossups": tossups, "cd2tossups": cd2tossups, "model": json.dumps(model), "prediction": prediction, "timeseries": {"biden": repr(list(map(lambda p: p.dem_win, predictions))), "trump": repr(list(map(lambda p: p.rep_win, predictions)))}})

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

	correlations = json.loads(CorrelationMatrix.objects.first().matrix)[obj.initials+("2" if cd2 else "")]
	similarstates = list(map(lambda i: i[0], list(sorted([i for i in correlations.items() if i[1] != 0], key=lambda i: abs(i[1] - 1)))[:4]))
	similar = State.objects.filter(initials__in=similarstates)
	cd2similar = State.objects.filter(initials__in=map(lambda i: i[:2], filter(lambda i: '2' in i, similarstates)))

	return render(request, "core/state.html", {"similar": similar, "cd2similar": cd2similar, "trump": trump, "biden": biden, "bpi": bpi, "mean": mean, "CD2": cd2, "pollavg": ("+" if mean*100 >= 50 else "")+"{:.1f}".format(200*mean - 100), "state": obj, "result": result, "trumpv": mean*100, "bidenv": 100-mean*100, "timeseries": {"biden": repr(list(map(lambda p: p.percent_biden, predictions.order_by('timestamp').all()))), "trump": repr(list(map(lambda p: p.percent_trump, predictions.order_by('timestamp').all())))}})

def blog(request,bid):
    return render(request,"core/blogpost.html",{"blogpost":get_object_or_404(Blogpost,pk=bid),"text":markdown(get_object_or_404(Blogpost,pk=bid).content)})

def methods(request):
    return render(request,"core/methods.html",{"methods":markdown(open("core/templates/core/methods.md",encoding="utf-8").read(),extensions=["footnotes"])})
