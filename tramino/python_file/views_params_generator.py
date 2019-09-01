# coding: utf-8

"""
This file is a collection of functions
that generating params process on views.py.
"""
from ..models import TeamInformations

def generate_my_teams_name_list(user_id):
    my_teams = TeamInformations.objects.filter(user=user_id)
    my_teams_name = []
    for my_team in my_teams:
        my_teams_name.append(my_team.organization_name)
    return my_teams_name



