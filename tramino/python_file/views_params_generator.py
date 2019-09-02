# coding: utf-8

"""
This file is a collection of functions
that generating params process on views.py.
"""
from ..models import TeamInformations, EventApplyPool, EventPostPool, FavoriteEventPool, FavoriteTeamPool

def generate_my_teams_name_list(user_id):
    my_teams = TeamInformations.objects.filter(user=user_id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    return my_teams_name


def generate_mypage_params(request):
    username = request.user.username
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_id = []
    for my_team in my_teams:
        my_teams_id.append(my_team.id)
    tab_names = []
    for i,my_team_id in enumerate(my_teams_id):
        my_teams[i].post_events =  EventPostPool.objects.all().filter(event_host_team=my_team_id)
        my_teams[i].apply_events =  EventApplyPool.objects.all().filter(guest_team_id=my_team_id)
        my_teams[i].favorite_events =  FavoriteEventPool.objects.all().filter(guest_team_id=my_team_id)
        my_teams[i].favorite_teams =  FavoriteTeamPool.objects.all().filter(guest_team_id=my_team_id)
        my_teams[i].tab_name = 'tab' + str(i+1)# tab切り替え用
        tab_names.append('tab' + str(i+1))# tab切り替えのためにjsに渡す変数

    try:
        commander_info = str(my_teams[0].organization_name) + str(my_teams[0].commander_name)
        commander_picture = my_teams[0].commander_picture
        team_counts = len(my_teams)
    except:
        commander_info, commander_picture, team_counts = 0, 0, 0
    params = {
        'username': username,
        'my_teams': my_teams,
        'commander_info':commander_info,
        'commander_pic':commander_picture,
        'tab_names':tab_names,
        'team_counts':team_counts,
        }
    return params
