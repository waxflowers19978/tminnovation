#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


""" import models or forms """
from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords,EventPostComment
from .forms import TeamInformationsForm, EventPostPoolForm, EventPostUpdateForm, MessageForm

""" python code in python_file """
from .python_file.model_form_save import *
from .python_file import message


""" 08/10以降追加 """
from django.shortcuts import get_object_or_404, resolve_url

from django.views.generic import ListView, UpdateView, DetailView, UpdateView, DeleteView, CreateView
from .python_file.profile_complate_percent import *

# Create your views here.



def index(request):
    return render(request, 'tramino/index.html')


def mypage(request):
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
        commander_info = ""
        commander_picture = ""
        team_counts = 0
    params = {
        'username': username,
        'my_teams': my_teams,
        'commander_info':commander_info,
        'commander_pic':commander_picture,
        'tab_names':tab_names,
        'team_counts':team_counts,
        }
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
        # return render(request, 'tramino/mypage.html')
    return render(request, 'tramino/mypage.html', params)


def match_search(request):
    username = request.user.username
    event_post_pool = EventPostPool.objects.all()
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_id = []# 自分のチームIDを持つイベントを表示しないようにする
    for my_team in my_teams:
        my_teams_id.append(my_team.id)
    for i,my_team_id in enumerate(my_teams_id):
        event_post_pool = event_post_pool.exclude(event_host_team=my_team_id)

    params = {
        'events': event_post_pool,
        'username': username,
    }
    return render(request, 'tramino/match_search.html', params)


def match_detail(request, event_id):
    """
    GET : match_searchやteam_detail,mypageのリンクから移動してくる
    POST : match_detailからイベントをファボした際POSTで入りなおす
    """
    message = ""
    username = request.user.username
    match  = EventPostPool.objects.get(id=event_id)
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    match.host_team_id = match.event_host_team.id# イベント詳細ページからチーム詳細に飛ぶためのURL生成に必要なイベントホストチームID
    applies = EventApplyPool.objects.all().filter(event_post_id=event_id)
    if request.method == 'POST':
        if request.POST['page_name'] == 'event_favorite':

            event_id, apply_team_id = request.POST['event_id'], request.POST['apply_team_id']
            apply = FavoriteEventPool()
            apply.event_post_id, apply.guest_team_id = EventPostPool.objects.get(id=event_id) ,TeamInformations.objects.get(id=apply_team_id)
            favorited_events = FavoriteEventPool.objects.all().filter(guest_team_id=apply.guest_team_id.id)
            if apply.event_post_id.id in list(favorited_events.values_list('event_post_id',flat=True)):
                FavoriteEventPool.objects.all().filter(guest_team_id=apply.guest_team_id.id).get(event_post_id=apply.event_post_id.id).delete()
                message = '気になるを取り消しました。'
            elif int(match.host_team_id) == int(apply.guest_team_id.id):
                message = '同チームのイベントは気になるリストに追加できません'

            else:
                apply.save()
                message = '気になるに追加しました。'
        elif request.POST['page_name'] == 'comment_submit':
            event_id = request.POST['event_id']
            posted_team_name = request.POST['team_name']
            print(posted_team_name)
            print("--")

            form = MessageForm()
            comment = EventPostComment()
            comment.message = request.POST['any_message']
            comment.post = EventPostPool.objects.get(id=event_id)
            comment.guest_team_id = TeamInformations.objects.get(organization_name=posted_team_name)
            comment.save()
            message = 'コメントを投稿しました'

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
    return render(request, 'tramino/match_detail.html', params)


def event_post(request):
    username = request.user.username
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    form = EventPostPoolForm()

    params = {
    'form': form,
    'username': username,
    'my_teams_name':my_teams_name,
    }
    return render(request, 'tramino/event_post.html', params)



def team_search(request):
    username = request.user.username
    team_informations = TeamInformations.objects.all().exclude(user=request.user.id)

    params = {
        'teams': team_informations,
        'username': username,
    }
    return render(request, 'tramino/team_search.html', params)


def team_detail(request, team_id):
    """
    GET : team_searchやmatch_detailのリンクから移動してくる
    POST : team_detailからチームをフォローした際POSTで入りなおす
    """
    message = ""
    if request.method == 'POST':
        if request.POST['page_name'] == 'team_favorite':
            team_id, apply_team_id = request.POST['team_id'], request.POST['apply_team_id']
            apply = FavoriteTeamPool()
            apply.host_team_id, apply.guest_team_id = TeamInformations.objects.get(id=team_id) ,TeamInformations.objects.get(id=apply_team_id)

            favorited_teams = FavoriteTeamPool.objects.all().filter(guest_team_id=apply.guest_team_id.id)
            if apply.host_team_id.id in list(favorited_teams.values_list('host_team_id',flat=True)):
                FavoriteTeamPool.objects.all().filter(guest_team_id=apply.guest_team_id.id).get(host_team_id=apply.host_team_id.id).delete()
                message = 'フォローを解除しました。'
            elif int(team_id) == apply.guest_team_id.id:
                message = '同チームをフォローすることはできません'
            else:
                apply.save()
                message = 'チームをフォローしました。'


    username = request.user.username
    team  = TeamInformations.objects.get(id=team_id)
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    events = EventPostPool.objects.all().filter(event_host_team=team_id)
    pastgamerecords = PastGameRecords.objects.all().filter(register_team_id=team_id)

    my_teams_id = []
    for my_team in my_teams:
        my_teams_id.append(my_team.id)
    if team_id in my_teams_id:# 自分のチームのならフォローできないようにする
        params = {
            'team': team,
            'username': username,
            'events':events,
            'pastgamerecords':pastgamerecords,
            'message':message,
        }
    else:# フォロー済みかどうかの判定
        for i,my_team_id in enumerate(my_teams_id):
            follow = list(FavoriteTeamPool.objects.all().filter(guest_team_id=my_team_id).values_list('host_team_id',flat=True))
            if int(team_id) in follow:
                my_teams[i].follow_judge = 'からのフォローを解除する'
            else:
                my_teams[i].follow_judge = 'からフォローする'

        params = {
            'team': team,
            'my_teams': my_teams,
            'username': username,
            'events':events,
            'pastgamerecords':pastgamerecords,
            'message':message,
        }

    return render(request, 'tramino/team_detail.html', params)


def create(request):
    form = TeamInformationsForm()
    params = {
    'form': form,
    }
    return render(request, 'tramino/create.html', params)


def done(request):
    username = request.user.username
    if request.method == 'POST':
        if request.POST['page_name'] == 'event_post':
            posted_team_name = request.POST['team_name']
            form = EventPostPoolForm(request.POST, request.FILES)
            message = ""
            if form.is_valid():
                event = EventPostPool()
                event.event_host_team = TeamInformations.objects.get(organization_name=posted_team_name)
                event.event_name = form.cleaned_data['event_name']
                event.event_description = form.cleaned_data['event_description']
                event.event_picture = form.cleaned_data['event_picture']
                event.event_date = form.cleaned_data['event_date']
                event.apply_deadline = form.cleaned_data['apply_deadline']
                event.save()
                message = 'イベントの募集を投稿しました。'
            else:
                message = '投稿フォームのパラメータに不備があります。'
                pass

        elif request.POST['page_name'] == 'event_apply':

            event_id = request.POST['event_id']
            apply_team_id = request.POST['apply_team_id']
            apply = EventApplyPool()
            apply.event_post_id = EventPostPool.objects.get(id=event_id)
            apply.guest_team_id = TeamInformations.objects.get(id=apply_team_id)
            apply.save()
            message = 'イベントに応募しました。'

        params = {
            'message': message,
            'username' : username,
        }
        return render(request, 'tramino/done.html', params)


    return redirect('tramino:mypage')


def logout(request):
    return render(request, 'tramino/logout.html')


class UserUpdateView(UpdateView):
    """ ユーザー情報を変更するためのページ """
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'tramino/crud/user_update.html'

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
        my_teams = TeamInformations.objects.filter(user=self.request.user.id)
        context['my_teams'] = my_teams
        scores = []
        for my_team in my_teams:# 各チームの達成率を算出し各パラメータに渡す
            pastgamerecords = PastGameRecords.objects.filter(register_team_id=my_team.id)
            scores.append(percent(my_team,pastgamerecords.count()))
        for i,score in enumerate(scores):
            my_teams[i].score = score
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
        # commander_pic = teaminformations.commander_picture.url

        pastgamerecords = PastGameRecords.objects.filter(register_team_id=self.kwargs.get('pk'))
        context['profile_complate'] = percent(teaminformations,pastgamerecords.count())# プロフィール完成率計算
        context['pastgamerecords'] = pastgamerecords
        username = self.request.user.username
        context['username'] = username
        return context


class MyTeamsUpdateView(UpdateView):
    """ チームそれぞれの情報編集ページ """
    model = TeamInformations
    # form_class = MyTeamsUpdateForm
    fields = '__all__'# ホントは下のように一つずつ指定した方がいい
    # fields = ('first_name', 'last_name', 'email')
    template_name = 'tramino/crud/myteams_edit.html'

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
    template_name = 'tramino/crud/myteams_delete.html'

    def get_success_url(self):
        #return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        return resolve_url('tramino:myteams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class EventUpdateView(UpdateView):
    """ イベント投稿を変更するためのページ """
    model = EventPostPool
    form_class = EventPostUpdateForm
    # fields = '__all__'
    template_name = 'tramino/crud/event_edit.html'

    def get_success_url(self):
        return resolve_url('tramino:mypage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class EventDeleteView(DeleteView):
    """ イベント投稿を削除するためだけのページ """
    model = EventPostPool
    template_name = 'tramino/crud/event_delete.html'

    def get_success_url(self):
        #return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        return resolve_url('tramino:mypage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


class PastGameCreateView(CreateView):
    """ チームそれぞれの対戦履歴を登録するページ """
    model = PastGameRecords
    fields = '__all__'# ホントは下のように一つずつ指定した方がいい
    template_name = 'tramino/create_past_game.html'

    def get_success_url(self):
        return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        # return resolve_url('tramino:myteams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        teaminformations = get_object_or_404(TeamInformations, pk=self.kwargs.get('pk'))
        username = self.request.user.username
        context['username'] = username
        return context


class PastGameDeleteView(DeleteView):
    """ チームそれぞれの対戦履歴をを削除するためだけのページ """
    model = PastGameRecords
    template_name = 'tramino/crud/past_game_delete.html'

    def get_success_url(self):
        #return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        return resolve_url('tramino:mypage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context



def message_home(request):
    message_redis = MessageRedis()
    params = {
        'aiueo':'aiueo',
    }
    return render(request, 'tramino/message_home.html', params)


def message_room(request, room_name):
    params = {
    }
    return render(request, 'tramino/message_room.html', params)
