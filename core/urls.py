from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    #Front Page
    path('', views.index, name='index'),
    path('viz/', views.vizualization, name='vizualization'),
]
