#from django.shortcuts import render
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)



""" import models or forms """
from .models import TeamInformations, EventPostPool, EventApplyPool, FavoriteEventPool,FavoriteTeamPool,PastGameRecords
from .forms import EventPostPoolForm, EventPostUpdateForm, MessageForm, PastGameRecordsForm, UserCreateForm, TeamInfoForm
from .forms import LoginForm

""" python code in python_file """
from .python_file.model_form_save import *
from .python_file import message
from .python_file.profile_complete_percent import *
from .python_file.schedule_process import *


""" 08/10以降追加 """
from django.shortcuts import get_object_or_404, resolve_url

from django.views import generic
from django.views.generic import ListView, UpdateView, DetailView, UpdateView, DeleteView, CreateView
import datetime
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.conf import settings
from django.template.loader import render_to_string
# Create your views here.

User = get_user_model()


class UserCreate(generic.CreateView):
    """ユーザー仮登録"""
    template_name = 'tramino/register/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('tramino/register/mail_template/create/subject.txt', context)
        message = render_to_string('tramino/register/mail_template/create/message.txt', context)

        user.email_user(subject, message)
        return redirect('tramino:user_create_done')


class UserCreateDone(generic.TemplateView):
    """ユーザー仮登録状態"""
    template_name = 'tramino/register/user_create_done.html'


class UserCreateComplete(generic.TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'tramino/register/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'tramino/login.html'


class Logout(LoginRequiredMixin, LogoutView):
    """ログアウトページ"""
    template_name = 'tramino/index.html'


def index(request):
    try:
        params = {
            'id':request.user.id,
            'email':request.user.email,
        }
        return render(request, 'tramino/index.html', params)
    except:
        params = {
            'id': "なし",
            'email': "なし"
        }
        return render(request, 'tramino/index.html', params)


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
        commander_info, commander_picture, team_counts = "", 0, 0
    params = {
        'username': username,
        'my_teams': my_teams,
        'commander_info':commander_info,
        'commander_pic':commander_picture,
        'tab_names':tab_names,
        'team_counts':team_counts,
        }
    if request.method == 'POST':
        user_id = request.user.id
        form = TeamInfoForm(request.POST, request.FILES)
        if form.is_valid():
            TeamInfoSave(request)
    return render(request, 'tramino/mypage.html', params)


def schedule(request):
    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_id = []
    for my_team in my_teams:
        my_teams_id.append(my_team.id)
    schedule_data_set,calendar_data_set = schedule_dataset_generator(my_teams_id,EventPostPool.objects.all(),EventApplyPool.objects.all())
    params = {
        'schedule_data_set': schedule_data_set,
        'calendar_data_set': calendar_data_set,
        }
    return render(request, 'tramino/schedule.html', params)


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
    form = TeamInfoForm()
    params = {
    'form': form,
    }
    return render(request, 'tramino/create.html', params)


def done(request):
    username = request.user.username
    if request.method == 'POST':
        if request.POST['page_name'] == 'event_post':
            posted_team_name = request.POST['team_name']
            if posted_team_name == '':
                message = 'チームがありません。対戦相手の募集にはチームの登録が必要です。'
                params = {'message': message}
                return render(request, 'tramino/done.html', params)
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
                eventdates = event.event_date
                applydeadline = event.apply_deadline
                today = datetime.date.today()
                if today<eventdates and today<applydeadline:
                    event.save()
                else:
                    message = '正しい日付を入力してください'
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
        pastgamerecords = PastGameRecords.objects.filter(register_team_id=self.kwargs.get('pk'))
        context['profile_complete'] = percent(teaminformations,pastgamerecords.count())# プロフィール完成率計算
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


class PastGameDeleteView(DeleteView):
    """ チームそれぞれの対戦履歴をを削除するためだけのページ """
    model = PastGameRecords
    template_name = 'tramino/crud/past_game_delete.html'

    def get_success_url(self):
        #return resolve_url('tramino:myteams_detail', pk=self.kwargs['pk'])
        return resolve_url('tramino:myteams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['username'] = username
        return context


def past_game_post(request):
    username = request.user.username
    message = ""
    complete_message = ""
    posted_by = ""
    if request.method == 'POST':
        if request.POST['page_name'] == 'past_game_post':
            posted_team_name = request.POST['posted_by']
            # posted_team_name = request.POST['team_name']
            form = PastGameRecordsForm(request.POST, request.FILES)
            message = ""
            complete_message = ""
            if form.is_valid():
                past_game = PastGameRecords()
                past_game.register_team_id = TeamInformations.objects.get(organization_name=posted_team_name)
                past_game.opponent_team_name = form.cleaned_data['opponent_team_name']
                past_game.game_category = form.cleaned_data['game_category']
                past_game.my_score = form.cleaned_data['my_score']
                past_game.opponent_score = form.cleaned_data['opponent_score']
                past_game.game_date = form.cleaned_data['game_date']
                past_game.game_description = form.cleaned_data['game_description']
                past_game.save()
                message = '試合記録を登録しました。続けて登録できます。'
                complete_message = '登録チーム情報の確認に戻る'
            else:
                message = '投稿フォームのパラメータに不備があります。'
                pass
        elif request.POST['page_name'] == 'past_game_register_ready':
            posted_by = request.POST['team_name']

    my_teams = TeamInformations.objects.filter(user=request.user.id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    form = PastGameRecordsForm()
    params = {
    'form': form,
    'username': username,
    'my_teams_name':my_teams_name,
    'message':message,
    'complete_message':complete_message,
    'posted_by':posted_by,
    }

    return render(request, 'tramino/create_past_game.html', params)


def message_home(request):
    user_id = request.user.id
    message_redis = message.MessageRedis()
    try:
        message_user_list = message_redis.get_message_user_list(user_id)
    except:
        message_user_list = ''
        print("----- non users -----")
    # print(message_user_list[0]['latest_message']['readed'])
    params = {
        'message_user_list': message_user_list,
    }
    return render(request, 'tramino/message_home.html', params)


def message_room(request, room_name):
    user_id = request.user.id
    message_redis = message.MessageRedis()

    # user_id = message_redis.room_name_to_ord_user_id(room_name)
    # grant_user_id = message_redis.user_id_to_grant_user_id(user_id)
    # my_id = request.user.id
    # print(grant_user_id)
    # print(type(grant_user_id[0]))
    # print()
    # print(my_id)
    # print(type(my_id))
    # if my_id != grant_user_id[0]:
    #     return render(request, 'tramino/message_room.html')


    if request.method == 'POST':
        message_text = request.POST['message_text']
        message_redis.save_message_to_redis(room_name, message_text)

    # request_path = request.path
    # room_name = request_path.replace('/tramino/message_home/', '')[:-1]
    message_list = message_redis.get_message_from_redis(room_name)
    params = {
        'message_list': message_list,
        'room_name': room_name,
        'user_id': user_id,
    }
    return render(request, 'tramino/message_room.html', params)

def message_template(request):
    message_redis = message.MessageRedis()
    if request.method == "POST":
        my_id = str(request.user.id)
        matchid = request.POST['matchid']
        oponent_id = str(EventPostPool.objects.get(pk=matchid).event_host_team.user.id)

        room_name = message_redis.make_room_name(my_id, oponent_id)
        params = {
            'room_name': room_name,
        }
        return render(request, 'tramino/message_template.html', params)

    else:
        return redirect('tramino:mypage')
