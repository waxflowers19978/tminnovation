from django.conf.urls import url
from django.urls import path
from . import views
# from tminnovation import settings

app_name = 'tramino'
urlpatterns = [
    # path('hp/', views.hp, name = 'hp'),
    path('index/', views.index, name = 'index'),
    path('mypage/', views.mypage, name='mypage'),
    path('match_search/', views.match_search, name='match_search'),
    path('match_detail/<int:event_id>/', views.match_detail, name='match_detail'),
    path('event_post/', views.event_post, name='event_post'),
    path('team_search/', views.team_search, name='team_search'),
    path('team_detail/<int:team_id>/', views.team_detail, name='team_detail'),
    path('create/', views.create, name='create'),
    path('done/', views.done, name='done'),
    path('logout/', views.logout, name='logout'),
]
