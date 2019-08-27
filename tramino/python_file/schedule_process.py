# coding: utf-8

"""
This file calculate all process related schedule.
"""
from datetime import datetime, date, timedelta
# import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

yobi = ["月","火","水","木","金","土","日"]


def schedule_dataset_generator(my_teams_id,event_objects,apply_objects):
    """ カレンダー上にユーザーの募集・応募したイベントのスケジュール情報を二次元配列で出力する関数 """
    schedule_data_set = []

    for i,my_team_id in enumerate(my_teams_id):
        event_post_date_list = list(event_objects.filter(event_host_team=my_team_id).values_list('event_date',flat=True))
        apply_event_date_list = list(apply_objects.filter(guest_team_id=my_team_id).values_list('event_post_id__event_date',flat=True))
        events = event_objects.filter(event_host_team=my_team_id)
        applies = apply_objects.filter(guest_team_id=my_team_id)
        if len(events)>0:
            for i,event in enumerate(events):
                weekday = event_post_date_list[i].weekday()
                result = [event,str(event_post_date_list[i]),0,"募集",yobi[weekday]]
                schedule_data_set.append(result)
        if len(applies)>0:
            for i,apply in enumerate(applies):
                weekday = apply_event_date_list[i].weekday()
                result = [apply,str(apply_event_date_list[i]),1,"応募",yobi[weekday]]
                schedule_data_set.append(result)
    schedule_data_set = sorted(schedule_data_set, key=lambda x: str2date(x[1]))
    calendar_data_set = calendar_list_generator()
    for i in schedule_data_set:
        for p in calendar_data_set:
            if i[1]==p[0]:
                p[1].append(i)
    # for i in 〇〇〇〇〇:# オリジナル予定モデルを追加して、ユーザーがとらみの以外の予定もカレンダーに追加できるようにする
    #     for p in calendar_data_set:
    #         if i[1]==p[0]:
    #             p[1].append(i)

    return schedule_data_set, calendar_data_set

def str2date(d):
    # tmp = datetime.datetime.strptime(d, '%Y-%m-%d')
    # return datetime.date(tmp.year, tmp.month, tmp.day)
    tmp = datetime.strptime(d, '%Y-%m-%d')
    return date(tmp.year, tmp.month, tmp.day)


def calendar_list_generator():
    """ 先月から再来月までの計四カ月間のカレンダーリストを出力する関数 """
    today = date.today()
    one_month_after = today + relativedelta(months=1)
    one_month_ago = today - relativedelta(months=1)
    two_month_after = one_month_after + relativedelta(months=1)
    counts = 0

    # lm means last_month
    lm_first_day = one_month_ago.replace(day=1)
    lm_last_day = (lm_first_day + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
    counts += (lm_last_day - lm_first_day).days
    counts += 1
    # this month
    first_day = today.replace(day=1)
    last_day = (today + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
    counts += (last_day - first_day).days
    counts += 1
    # nm means next month
    nm_first_day = one_month_after.replace(day=1)
    nm_last_day = (nm_first_day + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
    counts += (nm_last_day - nm_first_day).days
    counts += 1
    # n2m means 2next month
    n2m_first_day = two_month_after.replace(day=1)
    n2m_last_day = (n2m_first_day + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
    counts += (n2m_last_day - n2m_first_day).days
    counts += 1
    calendar_data_set = []
    the_day = lm_first_day
    for i in range(counts):
        weekday = the_day.weekday()
        result = [str(the_day),[],yobi[weekday],weekday]
        calendar_data_set.append(result)
        the_day = the_day + timedelta(days=1)

    return calendar_data_set


def calendar():
    """ アプリでは使わないメモ用関数。Datetime関連のリマインド用に使える """
    today = datetime.today()
    print(datetime.strftime(today, '%Y-%m-%d'))

    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    print("tomorrow -> " + datetime.strftime(tomorrow, '%Y-%m-%d'))
    print("yesterday -> " + datetime.strftime(yesterday, '%Y-%m-%d'))

    one_month_after = today + relativedelta(months=1)
    one_month_ago = today - relativedelta(months=1)

    print("one_month_after -> " + datetime.strftime(one_month_after, '%Y-%m-%d'))
    print("one_month_ago -> " + datetime.strftime(one_month_ago, '%Y-%m-%d'))    

    first_day = today.replace(day=1)
    print(datetime.strftime(first_day, '%Y-%m-%d'))
    last_day = (today + relativedelta(months=1)).replace(day=1) - timedelta(days=1)
    print(datetime.strftime(last_day, '%Y-%m-%d'))

    first_day = one_month_ago.replace(day=1)
    print(datetime.strftime(first_day, '%Y-%m-%d'))
    tomorrow = last_day + timedelta(days=1)
    print("tomorrow -> " + datetime.strftime(tomorrow, '%Y-%m-%d'))

if __name__ == "__main__":
    calendar_generator()

    # for i,my_team_id in enumerate(my_teams_id):
    #     event_post_date_list = list(EventPostPool.objects.all().filter(event_host_team=my_team_id).values_list('event_date',flat=True))
    #     apply_event_date_list = list(EventApplyPool.objects.filter(guest_team_id=my_team_id).values_list('event_post_id__event_date',flat=True))
    #     events = EventPostPool.objects.all().filter(event_host_team=my_team_id)
    #     applies = EventApplyPool.objects.filter(guest_team_id=my_team_id)
    #     if len(events)>0:
    #         for i,event in enumerate(events):
    #             weekday = event_post_date_list[i].weekday()
    #             result = [event,str(event_post_date_list[i]),0,"募集",yobi[weekday]]
    #             schedule_data_set.append(result)
    #     if len(applies)>0:
    #         for i,apply in enumerate(applies):
    #             weekday = apply_event_date_list[i].weekday()
    #             result = [apply,str(apply_event_date_list[i]),1,"応募",yobi[weekday]]
    #             schedule_data_set.append(result)
    # schedule_data_set = sorted(schedule_data_set, key=lambda x: str2date(x[1]))
    # for i in schedule_data_set:
    #     print(i[1])
    #     print("---------")
