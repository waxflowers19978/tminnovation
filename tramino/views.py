#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords
from .forms import TeamInformationsForm, EventPostPoolForm

"""
python code in python_file
"""
from .python_file.model_form_save import *

# Create your views here.



def index(request):
    return render(request, 'tramino/index.html')

@login_required
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
    username = request.user.username
    params = {
        'username': username,
    }
    return render(request, 'tramino/mypage.html', params)

@login_required
def match_search(request):
    username = request.user.username
    event_post_pool = EventPostPool.objects.all()
    params = {
        'events': event_post_pool,
        'username': username,
    }
    return render(request, 'tramino/match_search.html', params)

# def match_detail(request):
#     return render(request, 'tramino/match_detail.html')
@login_required
def match_detail(request, event_id):
    username = request.user.username
    match  = EventPostPool.objects.get(id=event_id)
    params = {
        'match': match,
        'username': username,
    }
    return render(request, 'tramino/match_detail.html', params)

@login_required
def event_post(request):
    username = request.user.username
    form = EventPostPoolForm()
    params = {
    'form': form,
    'username': username,
    }
    return render(request, 'tramino/event_post.html', params)

@login_required
def team_search(request):
    username = request.user.username
    team_informations = TeamInformations.objects.all()
    params = {
        'teams': team_informations,
        'username': username,
    }
    return render(request, 'tramino/team_search.html', params)

@login_required
def team_detail(request, team_id):
    username = request.user.username
    team  = TeamInformations.objects.get(id=team_id)
    params = {
        'team': team,
        'username': username,
    }
    return render(request, 'tramino/team_detail.html', params)


def create(request):
    form = TeamInformationsForm()
    params = {
    'form': form,
    }
    return render(request, 'tramino/create.html', params)

@login_required
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


    return redirect('tramino:mypage')
