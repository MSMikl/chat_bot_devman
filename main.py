from time import sleep

import requests

from environs import Env

from tbot import BotMessage

env = Env()
env.read_env()
token = env('DEVMAN_TOKEN')
telegram_id = env.int('TG_ID')
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
        BotMessage(telegram_id, 'Преподаватель проверил работу!')
        payload['timestamp'] = response['last_attempt_timestamp']
    elif response['status'] == 'timeout':
        print('Keep waiting')
        payload['timestamp'] = response['timestamp_to_request']