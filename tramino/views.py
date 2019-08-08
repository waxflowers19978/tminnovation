#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords
from .forms import TeamInformationsForm, EventPostPoolForm


from .python_file.model_form_save import *

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

def index(request):
    return render(request, 'tramino/index.html')

def mypage(request):
    if request.method == 'POST':

        form = TeamInformationsForm(request.POST, request.FILES)
        if form.is_valid():
            teamInfoSave()
            team = TeamInformations()
            team.organization_name = form.cleaned_data['organization_name']
            team.club_name = form.cleaned_data['club_name']
            team.sex = form.cleaned_data['sex']
            team.school_attribute = form.cleaned_data['school_attribute']
            team.prefectures_name = form.cleaned_data['prefectures_name']
            team.city_name = form.cleaned_data['city_name']
            team.activity_place = form.cleaned_data['activity_place']
            team.team_picture = form.cleaned_data['team_picture']
            team.url = form.cleaned_data['url']
            team.achievement = form.cleaned_data['achievement']
            team.practice_frequency = form.cleaned_data['practice_frequency']
            team.number_of_members = form.cleaned_data['number_of_members']
            team.commander_name = form.cleaned_data['commander_name']
            team.commander_career = form.cleaned_data['commander_career']
            team.commander_picture = form.cleaned_data['commander_picture']
            team.commander_introduction = form.cleaned_data['commander_introduction']
            team.save()
        return render(request, 'tramino/mypage.html')
    return render(request, 'tramino/mypage.html')

def match_search(request):
    event_post_pool = EventPostPool.objects.all()
    params = {
        'events': event_post_pool,
    }
    return render(request, 'tramino/match_search.html', params)

# def match_detail(request):
#     return render(request, 'tramino/match_detail.html')
def match_detail(request, event_id):
    match  = EventPostPool.objects.get(id=event_id)
    params = {
        'match': match,
    }
    return render(request, 'tramino/match_detail.html', params)

def event_post(request):
    form = EventPostPoolForm()
    params = {
    'form': form,
    }
    return render(request, 'tramino/event_post.html', params)

def team_search(request):
    team_informations = TeamInformations.objects.all()
    params = {
        'teams': team_informations,
    }
    return render(request, 'tramino/team_search.html', params)

def team_detail(request, team_id):
    team  = TeamInformations.objects.get(id=team_id)
    params = {
        'team': team,
    }
    return render(request, 'tramino/team_detail.html', params)

def login(request):
    return render(request, 'tramino/login.html')

def create(request):
    form = TeamInformationsForm()
    params = {
    'form': form,
    }
    return render(request, 'tramino/create.html', params)


def done(request):
    if request.method == 'POST':
        if request.POST['page_name'] == 'event_post':

            form = EventPostPoolForm(request.POST, request.FILES)
            if form.is_valid():
                event = EventPostPool()
                event.event_host_team = form.cleaned_data['event_host_team']
                event.event_name = form.cleaned_data['event_name']
                event.event_description = form.cleaned_data['event_description']
                event.event_picture = form.cleaned_data['event_picture']
                event.event_date = form.cleaned_data['event_date']
                event.apply_deadline = form.cleaned_data['apply_deadline']
                event.save()
            message = 'イベントの募集を投稿しました。'

        params = {
            'message': message,
        }
        return render(request, 'tramino/done.html', params)

    # return redirect('mypage')
    params = {
        'message': 'why???'
    }
    # return render(request, 'tramino/done.html', params)
    return redirect('tramino:mypage')
