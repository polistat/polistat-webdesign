from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    #Front Page
    path('', views.index, name='index'),
    path('state/<str:initials>/', views.state, name="state"),
    path('blog/<str:slug>/', views.blog, name="blog"),
    path('methodology/', views.methods, name="methods")
]
