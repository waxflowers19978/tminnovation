import os
import json

def get_school_list(school_name):
    main_path = os.getcwd()
    h_s_path = '/tramino/school_list/high_school_list.json'
    j_h_s_path = '/tramino/school_list/junior_high_school_list.json'
    school_path_list = [h_s_path, j_h_s_path]
    school_list = []
    for path in school_path_list:
        f = open(main_path + path, 'r')
        s_list = json.load(f)
        f.close()
        s_list = [school for school in s_list if school_name in school]
        school_list += s_list
    return school_list

def get_school_info(confirm_school_name):
    main_path = os.getcwd()
    h_s_path = '/tramino/school_list/high_school_dict.json'
    j_h_s_path = '/tramino/school_list/junior_high_school_dict.json'
    school_path_list = [h_s_path, j_h_s_path]

    n = 0
    for path in school_path_list:
        f = open(main_path + path, 'r')
        s_dict = json.load(f)
        f.close()
        result = s_dict.get(confirm_school_name, 'none')
        if result != 'none':
            prefectures_name = result[0].replace('の中学校一覧', '')
            city_name = result[1].replace(prefectures_name, '')
            if n == 0:
                school_attribute = '高校'
            else:
                school_attribute = '中学'
        n += 1

    school_info = {
        'prefectures_name': prefectures_name,
        'city_name': city_name,
        'school_attribute': school_attribute,
    }
    print(school_attribute)
    return school_info
