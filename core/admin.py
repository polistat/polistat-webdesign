from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from .models import *
# Register your models here.

class StatePollInline(admin.StackedInline):
    model = StatePoll
    extra=0
    
class PreviousElectionInline(admin.StackedInline):
    model = PreviousElection
    extra=0

class SenatorInline(admin.StackedInline):
    model = Senator
    extra=0

class SenateElectionInline(admin.StackedInline):
    model = SenateElection
    extra=0

class RepresentativeInline(admin.StackedInline):
    model = Representative
    extra=0

class HouseElectionInline(admin.StackedInline):
    model = HouseElection
    extra=0

class DemographicInline(admin.StackedInline):
    model = Demographic
    extra=0

class StateAdmin(admin.ModelAdmin):
    inlines = [
        StatePollInline,PreviousElectionInline,SenatorInline,SenateElectionInline,RepresentativeInline,HouseElectionInline,DemographicInline
    ]

##class BlogpostAdmin(admin.ModelAdmin):
##    formfield_overrides = {
##        models.TextField: {'widget': AdminMarkdownxWidget},
##    }

admin.site.register(State,StateAdmin)
admin.site.register(Tag)
admin.site.register(Blogpost,MarkdownxModelAdmin)
