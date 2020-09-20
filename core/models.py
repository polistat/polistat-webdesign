from django.db import models

# Create your models here.

#Model to represent a state.
class State(models.Model):
    name = models.CharField(max_length=100)
    data = models.FloatField()

#Blogpost Tag (or for anything else)
class Tag(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, null=True)
    #If an article is tagged with a state, it should be visible in that state's
    #States and their tags should be created in bulk
    
#Relatively simple if there are no authors
class Blogpost(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField() #When it appears on the homepage/state profile
    content = models.TextField() #Actual markdown content
    tags = models.ManyToManyField(Tag)
