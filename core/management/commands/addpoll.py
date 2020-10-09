# from django.core.management.base import BaseCommand, CommandError

# from core.models import State, StatePoll
# from django.utils import timezone

import csv

# def date_convert(str_date):
#         """
#         Converts a string in the form YYYY-MM-DD HH:MM:SS to a datetime object
#         """
#         str_date = str_date.split(" ")[0]
#         y_m_d = str_date.split('-')
#         y = int(y_m_d[0])
#         m = int(y_m_d[1])
#         d = int(y_m_d[2])
#         date = timezone.datetime(y, m, d)

#         return date

# class Command(BaseCommand):
#     help = 'adds the polls from csv to model'

     

#     def add_arguments(self, parser):
#         # Correct for PATH TO CSV FILE
#         parser.add_argument('file_name', type=str)

#     def handle(self, *args, **options):
#         file_name = options['file_name']

#         with open(file_name, 'r') as file:

#             rows = csv.reader(file, delimiter=',')
            
#             # remove header

#             next(rows)

#             #            0      1                2    3           4         5            6            7    8      9                     
#             # Structure: State, Polling Company, URL, Start Date, End Date, Sample Size, Sample Type, MOE, Biden, Trump 
#             for row in rows:
#                 state_name = row[0]
                
#                 pollster = row[1]
#                 url = row[2]
                
#                 # print(row)
#                 start_date_str = row[3]
#                 start_date = date_convert(start_date_str)
                

#                 end_date_str = row[4]
#                 end_date = date_convert(end_date_str)

#                 if row[5] != '':
#                     n = int(row[5])
#                 else:
#                     n = None
#                 pollType = row[6]
#                 if row[7] != '':
#                     moe = float(row[7])
#                 else:
#                     moe = None
#                 percent_biden = float(row[8])
#                 percent_trump = float(row[9])

#                 # id = f'{url}{state_name}{percent_biden}{percent_trump}'

#                 # Will create new StatePoll if the call returns Does Not Exist error
#                 try:
#                     # get State Object
#                     state = State.objects.get(name=state_name)
                    
                    
#                     try:
#                         exist_poll = StatePoll.objects.get(state=state, url=url, percent_biden=percent_biden, percent_trump=percent_trump)
#                     except:
#                         state_poll = StatePoll(state=state, start_date=start_date, end_date=end_date, percent_trump=percent_trump, percent_biden=percent_biden, n=n, pollType=pollType, pollster=pollster, moe=moe, url=url)
#                         state_poll.save()
                
#                 except:
#                     print(state_name)


with open('polls.csv', 'r') as file:

    rows = csv.reader(file, delimiter=',')
            
            # remove header

    next(rows)
    count = 0
    for row in rows:
        state = row[0]
        if 'Maine' not in state and 'Nebraska' not in state and 'National' not in state:
            count+=1
print(count)