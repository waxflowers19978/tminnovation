# coding: utf-8

"""
This file is a collection of functions
that save data in the model.
"""
from ..models import TeamInformations, User, EventApplyPool, EventPostPool
from ..forms import TeamInfoForm, EventPostPoolForm
import datetime
from .email_process import *


def TeamInfoSave(request):#mypage関数内で発火
    user_id = request.user.id
    form = TeamInfoForm(request.POST, request.FILES)
    if form.is_valid():
        team = TeamInformations()
        team.user = User.objects.get(id=user_id)
        team.organization_name = form.cleaned_data['organization_name']
        team.club_name = form.cleaned_data['club_name']
        team.sex = form.cleaned_data['sex']
        team.school_attribute = form.cleaned_data['school_attribute']
        team.prefectures_name = form.cleaned_data['prefectures_name']
        team.city_name = form.cleaned_data['city_name']
        team.activity_place = form.cleaned_data['activity_place']
        # team.team_picture = form.cleaned_data['team_picture']
        # team.url = form.cleaned_data['url']
        team.achievement = form.cleaned_data['achievement']
        # team.practice_frequency = form.cleaned_data['practice_frequency']
        team.number_of_members = form.cleaned_data['number_of_members']
        team.commander_name = form.cleaned_data['commander_name']
        # team.commander_career = form.cleaned_data['commander_career']
        # team.commander_picture = form.cleaned_data['commander_picture']
        # team.commander_introduction = form.cleaned_data['commander_introduction']
        team.save()

    return

def EventApplySave_when_apply_message_saved(request):#message_room関数内で発火
    event_id = request.POST['matchid']
    posted_team_name = request.POST['team_name']
    apply = EventApplyPool()
    apply.event_post_id = EventPostPool.objects.get(id=event_id)
    apply.guest_team_id = TeamInformations.objects.get(organization_name=posted_team_name)
    apply.save()
    send_mail_when_event_applied(request)


def EventPostSave(request,posted_team_name):#done関数内で発火
    form = EventPostPoolForm(request.POST, request.FILES)
    message = ""
    if form.is_valid():
        event = EventPostPool()
        event.event_host_team = TeamInformations.objects.get(organization_name=posted_team_name)
        event.event_name = form.cleaned_data['event_name']
        event.event_description = form.cleaned_data['event_description']
        # event.event_picture = form.cleaned_data['event_picture']
        event.event_date = form.cleaned_data['event_date']
        event.apply_deadline = form.cleaned_data['apply_deadline']
        eventdates = event.event_date
        applydeadline = event.apply_deadline
        today = datetime.date.today()
        if today<applydeadline and applydeadline<eventdates:
            event.save()
            message = 'イベントの募集を投稿しました。'
        else:
            message = '正しい日付を入力してください'
    else:
        message = '投稿フォームのパラメータに不備があります。'
        pass

    return message

