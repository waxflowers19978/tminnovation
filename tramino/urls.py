from django.conf.urls import url
from django.urls import path, include
from . import views
# from tminnovation import settings

app_name = 'tramino'
urlpatterns = [
    # path('hp/', views.hp, name = 'hp'),
    path('index/', views.index, name = 'index'),
    path('mypage/', views.mypage, name='mypage'),
    path('schedule/', views.schedule, name='schedule'),
    path('match_search/', views.match_search, name='match_search'),
    path('match_refine/', views.match_refine, name='match_refine'),
    path('match_detail/<int:event_id>/', views.match_detail, name='match_detail'),
    path('match_detail/update/<int:pk>/', views.EventUpdateView.as_view(), name='edit_event'),
    path('match_detail/delete/<int:pk>/', views.EventDeleteView.as_view(), name='delete_event'),
    path('event_post/', views.event_post, name='event_post'),
    path('team_search/', views.team_search, name='team_search'),
    path('team_detail/<int:team_id>/', views.team_detail, name='team_detail'),
    path('create/', views.create, name='create'),
    path('school_list/', views.school_list, name='school_list'),
    path('school_info/', views.school_info, name='school_info'),
    path('done/', views.done, name='done'),
    # path('logout/', views.logout, name='logout'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user_create/', views.UserCreate.as_view(), name='user_create'),
    path('user_create/done', views.UserCreateDone.as_view(), name='user_create_done'),
    path('user_create/complete/<token>/', views.UserCreateComplete.as_view(), name='user_create_complete'),
    path('myteams/',views.MyTeamsListView.as_view(), name='myteams'),
    path('myteams/detail/<int:pk>/', views.MyTeamsDetailView.as_view(), name='myteams_detail'),
    path('myteams/update/<int:pk>/', views.MyTeamsUpdateView.as_view(), name='edit_myteams'),
    path('myteams/delete/<int:pk>/', views.MyTeamsDeleteView.as_view(), name='delete_myteams'),
    path('user_update/',views.UserUpdateView.as_view(), name='user_update'),
    path('past_game_post/', views.past_game_post, name='past_game_post'),
    path('myteams/delete_past_game/<int:pk>/', views.PastGameDeleteView.as_view(), name='delete_past_game'),
    path('message_home/', views.message_home, name='message_home'),
    path('message_home/<str:room_name>/', views.message_room, name='message_room'),
    path('message_template', views.message_template, name='message_template'),
]
