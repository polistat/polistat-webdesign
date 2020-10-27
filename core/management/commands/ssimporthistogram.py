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
		m = csv.reader(open('ignored/mich/Electoral_Outcomes_Seeding_State_Shifts.csv', newline=''))
		next(m)
		f = [int(i) for i in next(m)]
		print(f)
		frequencies.frequencies = json.dumps(f)
		frequencies.save()
