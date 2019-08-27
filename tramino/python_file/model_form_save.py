# coding: utf-8

"""
This file is a collection of functions
that save data in the model.
"""
from ..models import TeamInformations, User
from ..forms import TeamInfoForm


def TeamInfoSave(request):
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
