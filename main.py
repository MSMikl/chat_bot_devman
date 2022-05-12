import asyncio
from time import sleep

import telegram
import requests

from environs import Env

env = Env()
env.read_env()
token = env('DEVMAN_TOKEN')
headers = {
    'Authorization':'Token {}'.format(token)
}
payload = {}
while True:
    try:
        response = requests.get(
            'https://dvmn.org/api/long_polling/',
            headers=headers,
            timeout=90,
            params=payload).json()
    except requests.exceptions.ReadTimeout:
        print('Таймаут соединения')
        sleep(5)
        continue
    except requests.exceptions.ConnectionError:
        print('Потеряно соединение с сервером')
        sleep(5)
        continue
    if response['status'] == 'found':
        print (response)
        payload['timestamp'] = response['last_attempt_timestamp']
    elif response['status'] == 'timeout':
        print('Keep waiting')
        payload['timestamp'] = response['timestamp_to_request']