import sys
import requests
import time

APP_ID = 7376843
BASE_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'response_type': 'token',
    'scope': 'status',
    'v': '5.95',
    'redirect_uri': 'https://example.com/'
}


TOKEN = 'f428320cf886b51998750431caae53420b854c4299d27a532e8dec3c07d6757eb2a55120f90265f78983c'


params = {
    'access_token': TOKEN,
    'v': '5.95'
}


class User:
    def __init__(self, token, user_id=None, first_name=None, last_name=None):
        self.token = token
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.95'
        )

    def get_info(self, user_id):
        """
        инфа о пользователе (по id)
        :return:
        """
        params = self.get_params()
        params['user_ids'] = user_id
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.user_id = response.json()['response'][0]['id']
        self.first_name = response.json()['response'][0]['first_name']
        self.last_name = response.json()['response'][0]['last_name']
        self.access = response.json()['response'][0]['can_access_closed']
        if self.access is False:
            print(f'{self.first_name} {self.last_name}:')
            print('Доступа нет, нельзя получить список общих друзей')
            sys.exit()
        # time.sleep(0.35)  # удалить, если наиграюсь в вывод имен общих друзей
        return response.json()

    def __and__(self, other_user):
        params = self.get_params()
        params['source_uid'] = user1.user_id
        params['target_uid'] = user2.user_id
        response = requests.get(
            'https://api.vk.com/method/friends.getMutual',
            params
        )
        return response.json()

    def __str__(self):
        # friend.get_info(userid)
        return f'https://vk.com/id{self.user_id}'
        # return f'https://vk.com/id{self.user_id} ({self.first_name} {self.last_name})'


def friends_list():
    common_friends_list = []
    for userid in mutal_user_list.get('response'):
        friend = User(TOKEN, userid)
        print(friend)
        common_friends_list.append(friend)  # список с представителями класса User
    print(f'Всего {len(common_friends_list)} общих друзей')
    print(common_friends_list)
    return





# 62117789 Me
# 110027658 Аня - нет доступа
# 23212039 Степа


user_id_1 = 62117789  # input
user_id_2 = 23212039  # input
user1 = User(TOKEN, user_id_1)
user1.get_info(user_id_1)
user2 = User(TOKEN, user_id_2)
user2.get_info(user_id_2)
mutal_user_list = user1 & user2

friends_list()


# common_friends_list = []
# for userid in mutal_user_list.get('response'):
#     friend = User(TOKEN, userid)
#     print(friend)
#     common_friends_list.append(friend)  # список с представителями класса User
# print(f'Всего {len(common_friends_list)} общих друзей')
# print(common_friends_list)
