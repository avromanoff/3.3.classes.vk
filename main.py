from pprint import pprint
from typing import Any
import sys
import requests
from urllib.parse import urlencode

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

TOKEN = 'cdf94efcb4a5021a7d008f5bb3f132cf2c2a9b34fb3be4b64d67a655803058c243af493eecae65163b4a9'

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

    def get_info(self):
        """
        инфа о текущем пользователе
        :return:
        """
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.user_id = response.json()['response'][0]['id']
        self.first_name = response.json()['response'][0]['first_name']
        self.last_name = response.json()['response'][0]['last_name']
        return response.json()

    def get_more_info(self):
        """
        Инфа о тех, чьи ID указываются, и проверка доступа к профилю
        :return:
        """
        params = self.get_params()
        params['user_ids'] = userid
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        self.user_id = response.json()['response'][0]['id']
        self.first_name = response.json()['response'][0]['first_name']
        self.last_name = response.json()['response'][0]['last_name']
        self.access = response.json()['response'][0]['can_access_closed']
        if self.access == False:
            print(f'{self.first_name} {self.last_name}')
            print('доступа нет\nНельзя получить список общих друзей')
            sys.exit()
        return response.json()

    def get_status(self):
        params = self.get_params()
        response = requests.get(
            'https://api.vk.com/method/status.get',
            params
        )
        return response.json()

    def friends_in_common(self):
        params = self.get_params()
        params['source_uid'] = users_from_string()[0]
        params['target_uid'] = users_from_string()[1]
        response = requests.get(
            'https://api.vk.com/method/friends.getMutual',
            params
        )
        return response.json()


def users_from_string():
    """
    Получаем из введенной строки список с 2 ID без пробелов
    :return:
    """
    users_split = two_users.split('&')
    users = []
    for u in users_split:
        u = u.strip()
        users.append(u)
    return users


username = User(TOKEN)
username.get_info()
print(f'Текущий пользователь - {username.first_name} {username.last_name}')

# two_users = input('Укажите ID двух пользователей, разделив их символом &, например, 62117789 & 23212039 ')
two_users = '23212039 & 62117789'  # test

# 62117789 Me
# 110027658 Аня - нет доступа
# 23212039 Степа


for usr in users_from_string():
    userid = usr
    username.get_more_info()
    print(username.first_name, username.last_name)


pprint(username.friends_in_common().get('response'))  # список ID общих друзей


common_friends_list = []
for userid in username.friends_in_common().get('response'):
    friend = User(userid)
    common_friends_list.append(friend)  # список с представителями класса Friend
print(common_friends_list)
