# coding: utf-8

"""
This file calculate profile complete percent.
"""

def percent(objects,count):
    # team_information_columns = ['organization_name', 'club_name', 'sex', 'school_attribute', 'prefectures_name', 'city_name', 'activity_place', 'team_picture', 'url', 'achievement', 'practice_frequency', 'number_of_members', 'commander_name', 'commander_career', 'commander_picture', 'commander_introduction']
    results = [objects.organization_name,objects.club_name,objects.sex,objects.school_attribute,objects.prefectures_name,objects.city_name,objects.activity_place,objects.team_picture,objects.url,objects.achievement,objects.practice_frequency,objects.number_of_members,objects.commander_name,objects.commander_career,objects.commander_picture,objects.commander_introduction]
    columns =9
    flag = 0
    for result in results:
        try:
            if len(result)==0:
                flag += 1
        except:
            flag += 1

    team_information_score = (columns - flag)*5+35
    
    if count * 4 < 21:
        past_game_record_score = count * 4
    else:
        past_game_record_score = 20

    score = team_information_score + past_game_record_score
    return score


# organization_name
# club_name
# sex
# school_attribute
# prefectures_name
# city_name
# activity_place
# team_picture
# url
# achievement
# practice_frequency
# number_of_members
# commander_name
# commander_career
# commander_picture
# commander_introduction
