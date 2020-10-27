from django.core.management.base import BaseCommand, CommandError

from core.models import *
from django.utils import timezone
import os
import csv
from django.shortcuts import get_object_or_404
import datetime

def date_convert(str_date):
         """
         Converts a string in the form YYYY-MM-DD HH:MM:SS to a datetime object
         """
         str_date = str_date.split(" ")[0]
         y_m_d = str_date.split('-')
         y = int(y_m_d[0])
         m = int(y_m_d[1])
         d = int(y_m_d[2])
         date = timezone.datetime(y, m, d)

         return date

def inUse(y,m,d):
    try:
        get_object_or_404(NationalPrediction,timestamp=timezone.datetime(y,m,d))
        return True
    except:
        return False
    

class Command(BaseCommand):
     help = 'imports simulation results'
##     def add_arguments(self, parser):
##         # Correct for PATH TO CSV FILE
##         parser.add_argument('file_name', type=str)

     def handle(self, *args, **options):
         os.chdir("ignored/results/")
         aps = []
         nws = []
         sos = []
         reader = csv.reader(open("../mich/StatePrediction_Seeding_State_Shifts.csv"))
         for l in reader:
             sos.append(l)
         reader = csv.reader(open("AveragedPolls - "+open('../mich/date').read()+".csv"))
         for l in reader:
             aps.append(l)
         reader = csv.reader(open("../mich/NationalPrediction_Seeding_State_Shifts.csv"))
         for l in reader:
             nws.append(l)
         print(aps.pop(0))
         print(sos.pop(0))
         print(nws.pop(0))
         n=NationalPrediction()
         n.timestamp = NationalPrediction.objects.latest('timestamp').timestamp + datetime.timedelta(days=1)
         n.rep_win = float(nws[0][1])
         n.dem_win = float(nws[1][1])
         n.save()
         for count in range(53):
             state = aps[count][1]
             mean = float(aps[count][2])
             variance = float(aps[count][3])
             biden = float(sos[count][-2])*100
             trump = float(sos[count][-3])*100
             if state in ["Maine CD-2","Nebraska CD-2"]:
                 s = get_object_or_404(State,name=state.split(" ")[0])
                 p = Prediction2()
                 p.state = s
                 p.percent_trump=trump
                 p.percent_biden=biden
                 p.mean=mean
                 p.variance=variance
                 p.timestamp=NationalPrediction.objects.latest('timestamp').timestamp + datetime.timedelta(days=1)
                 p.save()
                 s.biden2 = biden
                 s.trump2 = trump
                 s.mean2 = mean
                 s.save()
             else:
                 s = get_object_or_404(State,name=state)
                 p = Prediction()
                 p.state = s
                 p.percent_trump=trump
                 p.percent_biden=biden
                 p.mean=mean
                 p.variance=variance
                 p.timestamp=NationalPrediction.objects.latest('timestamp').timestamp + datetime.timedelta(days=1)
                 p.save()
                 s.biden = biden
                 s.trump = trump
                 s.mean = mean
                 s.save()
