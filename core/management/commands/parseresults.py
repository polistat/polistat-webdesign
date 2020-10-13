from django.core.management.base import BaseCommand, CommandError

from core.models import *
from django.utils import timezone
import os
import csv
from django.shortcuts import get_object_or_404


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
     help = 'adds the polls from csv to model'
##     def add_arguments(self, parser):
##         # Correct for PATH TO CSV FILE
##         parser.add_argument('file_name', type=str)

     def handle(self, *args, **options):
         os.chdir("ignored/results/")
         files = os.listdir()
         dates = []
         for file in files:
             if not "NationalWins" in file:
                 continue
             print(file)
             date = file.split(" - ")[1]
             date = date.split(".")[0].split("-")
             idate = list(map(int,date))
             y=idate[0]
             m=idate[1]
             d=idate[2]
             print(idate)
             if not inUse(y,m,d):
                 dates.append(date)
         for date in sorted(dates, lambda d: timezone.datetime(int(d[0]),int(d[1]),int(d[2]))):
             aps = []
             nws = []
             sos = []
             reader = csv.reader(open("StateOutcomes - "+date[0]+"-"+date[1]+"-"+date[2]+".csv"))
             for l in reader:
                 sos.append(l)
             reader = csv.reader(open("AveragedPolls - "+date[0]+"-"+date[1]+"-"+date[2]+".csv"))
             for l in reader:
                 aps.append(l)
             reader = csv.reader(open("NationalWins - "+date[0]+"-"+date[1]+"-"+date[2]+".csv"))
             for l in reader:
                 nws.append(l)
             print(aps.pop(0))
             print(sos.pop(0))
             print(nws.pop(0))
             n=NationalPrediction()
             n.timestamp = timezone.datetime(int(date[0]),int(date[1]),int(date[2]))
             n.rep_win = nws[0][1]
             n.dem_win = nws[0][2]
             n.save()
             for count in range(53):
                 state = aps[count][1]
                 mean = float(aps[count][2])
                 variance = float(aps[count][3])
                 biden = float(sos[count][3])/10000
                 trump = float(sos[count][4])/10000
                 if state in ["Maine CD-2","Nebraska CD-2"]:
                     s = get_object_or_404(State,name=state.split(" ")[0])
                     p = Prediction2()
                     p.state = s
                     p.percent_trump=trump
                     p.percent_biden=biden
                     p.mean=mean
                     p.variance=variance
                     p.timestamp=timezone.datetime(int(date[0]),int(date[1]),int(date[2]))
                     p.save()
                     s.biden2 = biden
                     s.trump2 = trump
                     s.save()
                 else:
                     s = get_object_or_404(State,name=state)
                     p = Prediction()
                     p.state = s
                     p.percent_trump=trump
                     p.percent_biden=biden
                     p.mean=mean
                     p.variance=variance
                     p.timestamp=timezone.datetime(int(date[0]),int(date[1]),int(date[2]))
                     p.save()
                     s.biden = biden
                     s.trump = trump
                     s.save()
