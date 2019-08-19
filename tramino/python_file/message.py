import redis
import datetime
import json
import base64


class MessageRedis():
    def __init__(self):
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

        #save
        redis_db_0 = redis.Redis(host='localhost', port=6379, db=0)
        redis_db_0.lpush(save_key,  json_dict_message)

        #history
        self.save_message_history(save_key)
        return

    """redisを参照"""
    def get_message_from_redis(self, room_name):

        #key
        user_id = self.room_name_to_ord_user_id(room_name)
        grant_user_id = self.user_id_to_grant_user_id(user_id)
        save_key = self.grant_user_id_to_save_key(grant_user_id)

        #参照
        redis_db_0 = redis.Redis(host='localhost', port=6379, db=0)
        json_message_list = redis_db_0.lrange(save_key, 0 , -1)

        #復元
        message_list = self.make_message_json_loads(json_message_list)
        return message_list


    """history"""
    def save_message_history(self, save_key):
        redis_db_1 = redis.Redis(host='localhost', port=6379, db=1)
        user_id_1, user_id_2 = save_key.split('_')
        redis_db_1.lpush(user_id_1, save_key)
        redis_db_1.lpush(user_id_2, save_key)
        return

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
        }
        return dict_message

    def make_message_json_dump(self, dict_message):
        json_dict_message = json.dumps(dict_message)
        return json_dict_message

    def make_message_json_loads(self, json_message_list):
        message_list = [json.loads(message) for message in json_message_list]
        return message_list
