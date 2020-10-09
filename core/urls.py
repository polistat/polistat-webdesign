from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    #Front Page
    path('', views.index, name='index'),
    path('viz/', views.vizualization, name='vizualization'),
    path('viz/trump/', views.vizualization2, name='vizualization2'),
    path('state/<str:initials>/', views.state, name="state"),
    path('blog/<int:bid>/', views.blog, name="blog")
]
