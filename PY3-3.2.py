from pprint import pprint
from urllib.parse import urlencode, urlparse
import requests
import time
import operator


AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.63'
APP_ID = 5948629

auth_data = {
    'client_id': APP_ID,
    'display': 'mobile',
    'response_type': 'token',
    'scope': 'friends,status,video',
    'v': VERSION,
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

token_url = 'https://oauth.vk.com/blank.html#access_token=19d52aa5d2c5497bab56ad81f91faf3d75b3900f772ee620cdf42380398ef89a87361f25cf33708ae4b6e&expires_in=86400&user_id=7203087'

o = urlparse(token_url)
fragments = dict(i.split('=') for i in o.fragment.split('&'))
access_token = fragments['access_token']

print(fragments)

params = {'access_token': access_token,
          'v': VERSION, }


def get_friend_list(user_id = None):
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return response.json()['response']['items']

def vk_execute(method, param_name, param_value):
    frlist = [6998, 170920]
    parameters = params
    parameters['method'] = method
    parameters[param_name] = param_value
    response = requests.get('https://api.vk.com/method/execute', parameters)
    return response.json()

def parts(lst, n=25):
    # разбиваем список на части - по 25 в каждой
    return [lst[i:i + n] for i in iter(range(0, len(lst), n))]


my_friends = get_friend_list()
print(my_friends)
my_friends_lst = parts(my_friends)
print(my_friends_lst)

all_friends = {}

for friend_lst in my_friends_lst:
    request_string = ''
    for friend in friend_lst:
        request_string += '"{}": API.friends.get({{"user_id": {}}}), '.format(friend,friend)
    request_string = 'return {' + request_string + '};'
    # print(request_string)
    params['code'] = request_string
    response = requests.get('https://api.vk.com/method/execute', params).json()['response']
    all_friends.update(response)
    time.sleep(1)
    print(response)

with open('export.json', 'w') as f:
    f.write(str(all_friends))

all_friends_friends = []
for friend in all_friends:
    all_friends_friends.append(friend)
    try:
        all_friends_friends += all_friends[friend]['items']
    except:
        pass

top_friends = {}
for friend in all_friends_friends:
    if friend in top_friends:
        value = top_friends[friend]
        top_friends[friend] = value + 1
    else:
        top_friends[friend] = 1
sorted_top_friends = sorted(top_friends.items(), key=operator.itemgetter(1), reverse=True)

with open ('top_friends.txt', 'w') as f:
    f.write(str(sorted_top_friends))
print(sorted_top_friends)
