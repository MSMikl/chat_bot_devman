from time import sleep

import requests
import telegram

from environs import Env


def main():
    env = Env()
    env.read_env()
    dvmn_token = env('DEVMAN_TOKEN')
    telegram_id = env.int('TG_USER_ID')
    tg_token = env('TELEGRAM_TOKEN')
    tbot = telegram.Bot(token=tg_token)
    headers = {
        'Authorization': 'Token {}'.format(dvmn_token)
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
        review_info = response.json()
        if review_info['status'] == 'found':
            for attempt in review_info['new_attempts']:
                message = 'Преподаватель проверил работу "{}"\n{}'.format(
                    attempt['lesson_title'],
                    attempt['lesson_url'],
                )
                if attempt['is_negative']:
                    message += '\n Пока неудачно'
                else:
                    message += '\n Работа сдана'
                tbot.sendMessage(telegram_id, message)
            payload['timestamp'] = review_info['last_attempt_timestamp']
        elif review_info['status'] == 'timeout':
            payload['timestamp'] = response['timestamp_to_request']


if __name__ == '__main__':
    main()
