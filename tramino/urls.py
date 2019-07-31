from django.conf.urls import url
from django.urls import path
from . import views
#from tminnovation import settings

app_name = 'tramino'
urlpatterns = [
    path('hp/', views.hp, name = 'hp'),
]

