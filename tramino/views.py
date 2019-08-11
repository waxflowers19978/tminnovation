#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


""" import models or forms """
from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords
from .forms import TeamInformationsForm, EventPostPoolForm

""" python code in python_file """
from .python_file.model_form_save import *


""" 08/10以降追加 """
from django.shortcuts import get_object_or_404, resolve_url
from .forms import MyTeamsUpdateForm

from django.views.generic import ListView, UpdateView, DetailView, UpdateView, DeleteView
# from .forms import EventApplyPoolForm

# Create your views here.



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
    username = request.user.username
    params = {
        'username': username,
    }
    return render(request, 'tramino/mypage.html', params)


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

def match_detail(request, event_id):
    username = request.user.username
    match  = EventPostPool.objects.get(id=event_id)
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    match.host_team_id = match.event_host_team.id# イベント詳細ページからチーム詳細に飛ぶためのURL生成に必要なイベントホストチームID

    params = {
        'match': match,
        'my_teams': my_teams,
        'username': username,
    }
    return render(request, 'tramino/match_detail.html', params)


def event_post(request):
    username = request.user.username
    form = EventPostPoolForm()
    params = {
    'form': form,
    'username': username,
    }
    return render(request, 'tramino/event_post.html', params)


def team_search(request):
    username = request.user.username
    team_informations = TeamInformations.objects.all()
    params = {
        'teams': team_informations,
        'username': username,
    }
    return render(request, 'tramino/team_search.html', params)


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

        elif request.POST['page_name'] == 'event_apply':

            event_id = request.POST['event_id']
            apply_team_id = request.POST['apply_team_id']
            apply = EventApplyPool()
            apply.event_post_id = EventPostPool.objects.get(id=event_id)
            apply.guest_team_id = TeamInformations.objects.get(id=apply_team_id)
            apply.save()
            message = 'イベントに応募しました。'

        elif request.POST['page_name'] == 'event_favorite':

            event_id, apply_team_id = request.POST['event_id'], request.POST['apply_team_id']
            apply = FavoriteEventPool()
            apply.event_post_id, apply.guest_team_id = EventPostPool.objects.get(id=event_id) ,TeamInformations.objects.get(id=apply_team_id)
            apply.save()
            message = 'イベントを気になるリストに追加しました。'

        params = {
            'message': message,
        }
        return render(request, 'tramino/done.html', params)


    return redirect('tramino:mypage')

def logout(request):
    return render(request, 'tramino/logout.html')


class UserUpdateView(UpdateView):
    """ ユーザー情報を変更するためのページ """
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'tramino/user_update.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return resolve_url('tramino:mypage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class MyTeamsListView(ListView):
    """ チームのリストを表示しCRUDに繋がるページ """
    model = TeamInformations
    context_object_name = 'teaminformationss'
    template_name = 'tramino/myteams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class MyTeamsDetailView(DetailView):
    """ チームそれぞれの詳細情報表示ページ """
    model = TeamInformations
    template_name = 'tramino/myteams_detail.html'
    def get_queryset(self):
        return TeamInformations.objects.filter().order_by('-published')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teaminformations = get_object_or_404(TeamInformations, pk=self.kwargs.get('pk'))
        username = self.request.user.username
        context['username'] = username
        return context


class MyTeamsUpdateView(UpdateView):
    """ チームそれぞれの情報編集ページ """
    model = TeamInformations
    # form_class = MyTeamsUpdateForm
    fields = '__all__'# ホントは下のように一つずつ指定した方がいい
    # fields = ('first_name', 'last_name', 'email')
    template_name = 'tramino/edit_myteams.html'

    def get_success_url(self):
        return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        #return resolve_url('tramino:myteams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class MyTeamsDeleteView(DeleteView):
    """ チームを削除するためだけのページ """
    model = TeamInformations
    form_class = MyTeamsUpdateForm
    template_name = 'tramino/delete_myteams.html'

    def get_success_url(self):
        #return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        return resolve_url('tramino:myteams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


