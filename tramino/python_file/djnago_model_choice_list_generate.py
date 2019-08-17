# coding: utf-8

# コード説明
# input:1
# input:2
# input:3
# output:['1','1'],[2','2'],[3','3']

print("mode 1 output:['1','1'],[2','2'],[3','3']")
print("mode 2 output:'1','2','3'")
print("mode 3 output:('a', 'a'), ('b', 'b')")

mode = int(input("please choise mode : input 1 or 2 : "))

if mode ==1:
    result = "['"

    while True:
        text = str(input("input:"))
        if text=="":
            result = result[:-5]
            text+="']"
            result+=text
            break
        else:
            text = text+"','"+text+"'],['"
            result+=text
    print(result)
elif mode ==2:
    result = "'"

    while True:
        text = str(input("input:"))
        if text=="":
            result = result[:-5]
            text+="'"
            result+=text
            break
        else:
            text = text+"','"
            result+=text
    print(result)
else:
    result = "('"

    while True:
        text = str(input("input:"))
        if text=="":
            result = result[:-5]
            text+="')"
            result+=text
            break
        else:
            text = text+"','"+text+"'),('"
            result+=text
    print(result)


# 全国大会優勝レベル
# 全国大会入賞レベル
# 全国大会出場常連レベル
# 全国大会出場レベル
# 都道府県大会入賞レベル
# 都道府県大会常連レベル
# 都道府県大会出場レベル
# 地区大会入賞レベル
# 地区大会常連レベル


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


# event_host_team
# event_name
# event_description
# event_picture
# event_date
# apply_deadline
