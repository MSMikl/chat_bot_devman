from time import sleep

import requests

from environs import Env

from tbot import BotMessage


def main():
    env = Env()
    env.read_env()
    token = env('DEVMAN_TOKEN')
    telegram_id = env.int('TG_USER_ID')
    headers = {
        'Authorization': 'Token {}'.format(token)
    }
    payload = {}
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers=headers,
                timeout=90,
                params=payload)
            response.raise_for_status()
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            print('Потеряно соединение с сервером')
            sleep(5)
            continue
        responsed_data = response.json()
        if responsed_data['status'] == 'found':
            for attempt in responsed_data['new_attempts']:
                message = 'Преподаватель проверил работу "{}"\n{}'.format(
                    attempt['lesson_title'],
                    attempt['lesson_url'],
                )
                if attempt['is_negative']:
                    message += '\n Пока неудачно'
                else:
                    message += '\n Работа сдана'
                BotMessage(telegram_id, message)
            payload['timestamp'] = responsed_data['last_attempt_timestamp']
        elif responsed_data['status'] == 'timeout':
            payload['timestamp'] = response['timestamp_to_request']


if __name__ == '__main__':
    main()
