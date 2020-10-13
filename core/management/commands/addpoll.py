from django.core.management.base import BaseCommand, CommandError

from core.models import State, StatePoll
from django.utils import timezone

import csv

class Command(BaseCommand):
	help = 'adds the polls from csv to model'

	def add_arguments(self, parser):
		# Correct for PATH TO CSV FILE
		parser.add_argument('file_name', type=str)

	def handle(self, *args, **options):
		file_name = options['file_name']
		with open(file_name, 'r') as file:
			rows = csv.reader(file, delimiter=',')
			next(rows)
			#            0      1                2    3           4         5            6            7      8
			# Structure: State, Polling Company, URL, Start Date, End Date, Sample Size, Sample Type, Biden, Trump
			for row in rows:
				state_name = row[0]
				
				pollster = row[1]
				url = row[2]
				
				start_date_str = row[3]
				start_date = timezone.datetime(2000+int(start_date_str.split('/')[2]), int(start_date_str.split('/')[0]), int(start_date_str.split('/')[1]))
				if start_date < timezone.datetime(2020, 8, 12): continue
				
				end_date_str = row[4]
				end_date = timezone.datetime(2000+int(end_date_str.split('/')[2]), int(end_date_str.split('/')[0]), int(end_date_str.split('/')[1]))

				if row[5] != '':
					n = int(row[5])
				else:
					n = None
				pollType = row[6]
				percent_biden = float(row[7])
				percent_trump = float(row[8])

				try:
					state = State.objects.filter(name=state_name.split(' CD-2')[0]).get()
					try:
						exist_poll = StatePoll.objects.filter(state=state, url=url, percent_biden=percent_biden, percent_trump=percent_trump).get()
					except StatePoll.DoesNotExist:
						state_poll = StatePoll(state=state, cd2=(' CD-2' in state_name), start_date=start_date, end_date=end_date, percent_trump=percent_trump, percent_biden=percent_biden, n=n, pollType=pollType, pollster=pollster, url=url)
						state_poll.save()
				except State.DoesNotExist:
					print('failed to find state: ' + state_name)
