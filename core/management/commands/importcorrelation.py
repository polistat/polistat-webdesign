from django.core.management.base import BaseCommand, CommandError

from core.models import *
from django.shortcuts import get_object_or_404
import csv
import json
import collections

class Command(BaseCommand):
	help = 'imports the correlation matrix'

	def handle(self, *args, **options):
		if not CorrelationMatrix.objects.exists(): matrix = CorrelationMatrix()
		else: matrix = CorrelationMatrix.objects.first()

		abbrev = lambda s: State.objects.filter(name=s.split(' CD-2')[0]).first().initials + ('2' if 'CD-2' in s else '')

		correlations = collections.defaultdict(dict)
		m = csv.DictReader(open('ignored/data/StateCorrelationWith7', newline=''))
		for r in m:
			state = abbrev(r[''])
			for k in r:
				if k == '': continue
				correlations[state][abbrev(k)] = float(r[k])
		matrix.matrix = json.dumps(correlations)
		matrix.save()
