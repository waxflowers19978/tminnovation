from django.contrib.auth.models import User

from ..models import TeamInformations

import redis
import datetime
import json
import base64


class MessageRedis():
    def __init__(self):
        """
        try:
            import local_settings
            self.host = 'localhost'
            self.port = 6379
            self.password = ''
        except:
            #本番(hroku)
            self.host = ''
            self.port = ''
            self.password = ''
        """
        return

    """redisに保存"""
    def save_message_to_redis(self, room_name, message):

        #key
        user_id = self.room_name_to_ord_user_id(room_name)
        grant_user_id = self.user_id_to_grant_user_id(user_id)
        save_key = self.grant_user_id_to_save_key(grant_user_id)

        #value
        dict_message = self.make_message_to_dict(grant_user_id, message)
        json_dict_message = self.make_message_json_dump(dict_message)

        #save_message
        redis_db_0 = redis.Redis(host='localhost', port=6379, db=0)
        # redis_db_0 = redis.StrictRedis(host=self.host, port=self.port, db=0, password=self.password)
        redis_db_0.lpush(save_key,  json_dict_message)

        #save_history
        user_id_1, user_id_2 = save_key.split('_')

        user_1_history = self.get_message_history(user_id_1)
        new_message_history_list_1 = self.new_message_history(user_1_history, save_key)
        self.save_message_history(user_id_1, new_message_history_list_1)

        user_2_history = self.get_message_history(user_id_2)
        new_message_history_list_2 = self.new_message_history(user_2_history, save_key)
        self.save_message_history(user_id_2, new_message_history_list_2)
        return

    """redisを参照"""
    def get_message_from_redis(self, room_name):

        #key
        user_id = self.room_name_to_ord_user_id(room_name)
        grant_user_id = self.user_id_to_grant_user_id(user_id)
        save_key = self.grant_user_id_to_save_key(grant_user_id)

        #参照
        redis_db_0 = redis.Redis(host='localhost', port=6379, db=0)
        # redis_db_0 = redis.StrictRedis(host=self.host, port=self.port, db=0, password=self.password)
        json_message_list = redis_db_0.lrange(save_key, 0 , -1)

        #復元
        message_list = self.make_message_json_loads(json_message_list)

        #既読をつける
        latest_message = message_list[0]
        grant_readed = self.latest_message_readed(grant_user_id, save_key, message_list[0])
        if grant_readed:
            latest_message['readed'] = '1'
            json_latest_message = json.dumps(latest_message)
            redis_db_0.lpop(save_key)
            redis_db_0.lpush(save_key, json_latest_message)

        return message_list


    """history"""
    def save_message_history(self, user_id, message_history_list):
        redis_db_1 = redis.Redis(host='localhost', port=6379, db=1)
        # redis_db_1 = redis.StrictRedis(host=self.host, port=self.port, db=1, password=self.password)
        result = redis_db_1.delete(user_id)
        for history in message_history_list:
            redis_db_1.rpush(user_id, history)
        return

    def latest_message_readed(self, grant_user_id, save_key, latest_message):
        request_id = grant_user_id[0]
        # print(latest_message['readed'])
        readed = latest_message['readed']
        if readed == '0':
            return True
        else:
            return False



        return

    def new_message_history(self, old_message_history_list, save_key):
        bytes_save_key = save_key.encode('utf-8')
        if bytes_save_key in old_message_history_list:
            old_message_history_list.remove(bytes_save_key)
        old_message_history_list.insert(0, save_key)
        new_message_history_list = old_message_history_list
        return new_message_history_list

    def room_name_to_ord_user_id(self, room_name):
        decoded_room_name = base64.b64decode(room_name)
        string_decoded_room_name = str(decoded_room_name, 'utf-8')
        user_id = string_decoded_room_name.split('_')
        return user_id

    def user_id_to_grant_user_id(self, user_id):
        grant_user_id = []
        for u_id in user_id:
            it = iter(u_id)
            temp = ""
            for i in it:
                ascii_user_id = int(i + next(it))
                temp += chr(ascii_user_id)
            grant_user_id.append(int(temp))
        return grant_user_id

    def grant_user_id_to_save_key(self, grant_user_id):
        minimum_id, maximum_id = sorted(grant_user_id)
        save_key = str(minimum_id) + '_' + str(maximum_id)
        return save_key

    def make_message_to_dict(self, grant_user_id, message):
        sender_id, receiver_id = grant_user_id
        date_now= datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
        dict_message = {
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'timestanp': date_now,
            'message': message,
            'readed': '0',
        }
        return dict_message

    def make_message_json_dump(self, dict_message):
        json_dict_message = json.dumps(dict_message)
        return json_dict_message

    def make_message_json_loads(self, json_message_list):
        message_list = [json.loads(message) for message in json_message_list]
        return message_list

    """一覧"""
    def get_message_user_list(self, user_id):
        message_user_list = []

        message_history_list = self.get_message_history(user_id)

        for save_key in message_history_list:
            history_dict = {}
            oponent_id = self.get_oponent_id(save_key, user_id)
            oponent_teams = self.get_oponent_teams(oponent_id)
            # room_name = self.save_key_to_room_name(save_key)
            # print(room_name)
            room_name = self.make_room_name(user_id, oponent_id)
            latest_message = self.get_latest_message(save_key)

            history_dict['oponent_id'] = oponent_id
            history_dict['oponent_teams'] = oponent_teams
            history_dict['history'] = save_key
            history_dict['room_name'] = room_name
            history_dict['latest_message'] = latest_message
            message_user_list.append(history_dict)

        return message_user_list

    def get_message_history(self, user_id):
        string_user_id = str(user_id)
        redis_db_1 = redis.Redis(host='localhost', port=6379, db=1)
        # redis_db_1 = redis.StrictRedis(host=self.host, port=self.port, db=1, password=self.password)
        message_history_list= redis_db_1.lrange(string_user_id, 0 , -1)
        return message_history_list

    def get_oponent_id(self, save_key, user_id):
        string_user_id = str(user_id)
        user_id_1, user_id_2 = str(save_key, 'utf-8').split('_')
        if string_user_id == user_id_1:
            oponent_id = user_id_2
        else:
            oponent_id = user_id_1

        return oponent_id

    def get_oponent_teams(self, user_id):
        int_str_id = int(user_id)
        oponent_teams = TeamInformations.objects.filter(user=int_str_id)
        return oponent_teams

    def make_room_name(self, user_id, oponent_id):
        string_user_id = str(user_id)
        ord_id_1 = ''.join([str(ord(i)) for i in string_user_id])
        ord_id_2 = ''.join([str(ord(i)) for i in oponent_id])
        ord_save_key = ord_id_1 + '_' + ord_id_2
        ord_save_key = ord_save_key.encode('utf-8')
        room_name = base64.b64encode(ord_save_key)
        room_name = str(room_name, 'utf-8')
        print(room_name)
        return room_name

    def get_latest_message(self, save_key):
        redis_db_0 = redis.Redis(host='localhost', port=6379, db=0)
        # redis_db_0 = redis.StrictRedis(host=self.host, port=self.port, db=0, password=self.password)
        latest_json_encoded_message = redis_db_0.lindex(save_key, 0)
        latest_json_message = latest_json_encoded_message.decode('utf-8')
        latest_json_message = latest_json_encoded_message
        latest_message = json.loads(latest_json_message)
        return latest_message
