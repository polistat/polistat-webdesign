from .models import *

def states(request):
	return {"states": State.objects.all()}
