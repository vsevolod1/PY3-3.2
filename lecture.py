from pprint import pprint

import vk
from urllib.parse import urlencode, urlparse
import requests


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
APP_ID = 5948629  # Your app_id here

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status,video',
    'v': VERSION,
}
print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

token_url = 'https://oauth.vk.com/blank.html#access_token=a13fcf3d45963fd2673fa8c8b84e8d3deb84c36f7f77c9ebe97038d26d36428e15af3bc3f9c654540552a&expires_in=86400&user_id=7203087'

o = urlparse(token_url)
fragments = dict(i.split('=') for i in o.fragment.split('&'))
access_token = fragments['access_token']

print(fragments)

params = {'access_token': access_token,
          'v': VERSION,
          }

# response = requests.get('https://api.vk.com/method/database.getCities', params)
# print(response.json())
#
# params = {'access_token': access_token,
#           'v': VERSION,
#           'q': 'Ольга Мартыненко',
#           'city': 818
#           }
#
# response = requests.get('https://api.vk.com/method/users.search', params)
# print(response.json())

# response = requests.get('https://api.vk.com/method/status.get', params)
# print(response.json())
#
# params['text'] = 'Hello!'
#
# response = requests.get('https://api.vk.com/method/status.set', params)
# print(response.json())
#

#
#
# response = requests.get('https://api.vk.com/method/video.get', params)
# pprint(response.json())


def get_status(user_id = None):
    # if user_id:
    #     params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/status.get', params)
    return response.json()['response']['text']

# params['fields'] = 'user_id'
def get_friend_list(user_id = None):
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()['response']['items']

# print('Статус: ', get_status())
my_friends = get_friend_list()
pprint(len(my_friends))

friends_friends = {fragments['user_id'] : my_friends}

# print(friends_friends)

for friend in my_friends[0:9]:
    friend_list = get_friend_list(friend)
    friends_friends[friend] = friend_list

pprint(friends_friends.keys())