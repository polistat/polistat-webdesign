from django.core.management.base import BaseCommand
from core.models import *
import csv
import json
from datetime import datetime

class Command(BaseCommand):
	help = 'imports the correlation matrix'

	def handle(self, *args, **options):
		if not EVFrequencies.objects.exists(): frequencies = EVFrequencies()
		else: frequencies = EVFrequencies.objects.first()

		f = [0]*539
		m = csv.reader(open('ignored/results/ElectoralBins - '+datetime.now().isoformat()[:10]+'.csv', newline=''))
		next(m)
		for l in m:
			f[int(l[0])] = int(l[1])
		frequencies.frequencies = json.dumps(f)
		frequencies.save()
