# coding: utf-8

"""
This file is a collection of functions
that generating params process on views.py.
"""
from ..models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords
from ..forms import EventPostPoolForm, EventPostUpdateForm, MessageForm, PastGameRecordsForm, UserCreateForm, TeamInfoForm
from .schedule_process import *

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

def generate_match_detail_params(request):
    event_id = request.POST['matchid']
    message = ""
    username = request.user.username
    match  = EventPostPool.objects.get(id=event_id)
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    match.host_team_id = match.event_host_team.id# イベント詳細ページからチーム詳細に飛ぶためのURL生成に必要なイベントホストチームID
    match = match_and_deadline_day_of_the_week(match)
    applies = EventApplyPool.objects.all().filter(event_post_id=event_id)

    my_teams_id = []
    for my_team in my_teams:
        my_teams_id.append(my_team.id)

    if match.host_team_id in my_teams_id:# 自分のチームの投稿なら応募やファボをできないようにする
        params = {
            'match': match,
            'username': username,
            'applies' : applies,
            'message' : message,
        }
    else:# 気になる済みかどうかの判定
        for i,my_team_id in enumerate(my_teams_id):
            favo = list(FavoriteEventPool.objects.all().filter(guest_team_id=my_team_id).values_list('event_post_id',flat=True))
            if int(event_id) in favo:
                my_teams[i].favo_judge = 'の気になるリストから取り消す'
            else:
                my_teams[i].favo_judge = 'の気になるリストに追加する'
        form = MessageForm()
        params = {
            'form': form,
            'match': match,
            'my_teams': my_teams,
            'my_teams_name':my_teams_name,
            'username': username,
            'applies' : applies,
            'message' : message,
        }
    return params