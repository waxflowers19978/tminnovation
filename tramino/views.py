#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords



# Create your views here.


def hp(request):
    team_list = list(TeamInformations.objects.values_list('organization_name', flat=True))
    team_detail_info = TeamInformations.objects.values_list('organization_name', flat=True)
    all_team_info = TeamInformations.objects.all()
    all_team_info = all_team_info.values_list()

    all_event_info = EventPostPool.objects.all().values_list()
    all_event_applies = EventApplyPool.objects.all().values_list()
    all_favorite_event = FavoriteEventPool.objects.all().values_list()
    all_favorite_team = FavoriteTeamPool.objects.all().values_list()
    all_past_game_records = PastGameRecords.objects.all().values_list()
    


    #できたばかりの人工芝グラウンドで練習試合をしませんか？
    #当校のグラウンドは、2017年に人工芝グラウンドになったばかりです。広さは縦105メートル、横60メートルと広大で、ウォーミングアップ用のコートも併設してあります。ぜひ当校のグラウンドのお越しください。


    params={
        'all_team_info':all_team_info,
        'all_event_info':all_event_info,        
        'all_event_applies':all_event_applies,        
        'all_favorite_event':all_favorite_event,        
        'all_favorite_team':all_favorite_team,        
        'all_past_game_records':all_past_game_records,        
        
    }
    return render(request, 'tramino/hp.html',params)
