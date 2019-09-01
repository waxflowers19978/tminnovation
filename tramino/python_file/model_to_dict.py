from django.core.serializers.json import DjangoJSONEncoder
import json


def make_model_list(objects):
    event_list = []
    for obj in objects:
        # print("{}:{}".format(obj, obj.event_host_team.club_name))
        model_dict = {}
        # model_dict['event_host_name'] = obj
        model_dict['pk'] = obj.id
        model_dict['organization_name'] = obj.event_host_team.organization_name
        model_dict['club_name'] = obj.event_host_team.club_name
        model_dict['prefectures_name'] = obj.event_host_team.prefectures_name
        model_dict['city_name'] = obj.event_host_team.city_name
        model_dict['number_of_members'] = obj.event_host_team.number_of_members
        model_dict['achievement'] = obj.event_host_team.achievement
        model_dict['activity_place'] = obj.event_host_team.activity_place
        model_dict['event_name']= obj.event_name
        model_dict['event_date'] = obj.event_date
        model_dict['dot_week'] = obj.dot_week
        model_dict['activity_place_picture_url'] = obj.event_host_team.activity_place_picture.url
        model_dict['team_picture_url'] = obj.event_host_team.team_picture.url


        event_list.append(model_dict)

    event_post_pool = json.dumps(event_list, ensure_ascii=False, cls=DjangoJSONEncoder)
    # event_post_pool = json.dumps(event_list, ensure_ascii=False, sort_keys=True, indent=4, default=json_serial)
    # event_post_pool = json.dumps(event_list, ensure_ascii=False, sort_keys=True, indent=4)
    return event_post_pool
