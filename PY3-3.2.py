from pprint import pprint

import vk
from urllib.parse import urlencode, urlparse
import requests
import time


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

token_url = 'https://oauth.vk.com/blank.html#access_token=d6c009ad7e7c72da10230b5d3d4ccb6567b6823bb0c8dde1d1a4338eadd6e8688828174b370d8bde23776&expires_in=86400&user_id=7203087'

o = urlparse(token_url)
fragments = dict(i.split('=') for i in o.fragment.split('&'))
access_token = fragments['access_token']

print(fragments)

params = {'access_token': access_token,
          'v': VERSION, }

params['method'] = 'users.get'
params['user_ids'] = '6998, 170920, 329878025'


def get_friend_list(user_id = None):
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()['response']['items']

def vk_execute(method, param_name, param_value):
    frlist = [6998, 170920]
    parametres = params
    parametres['method']: method
    parametres[param_name]: param_value
    response = requests.get('https://api.vk.com/method/execute', parametres)
    return  response.json()

# gexecute = vk_execute()
# pprint(gexecute)