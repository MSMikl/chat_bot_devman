from time import sleep

import logging
import os

import dotenv
import requests
import telegram


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    dotenv.load_dotenv()
    dvmn_token = os.getenv('DEVMAN_TOKEN')
    telegram_id = int(os.getenv('TG_USER_ID'))
    tg_token = os.getenv('TELEGRAM_TOKEN')
    tbot = telegram.Bot(token=tg_token)
    logger = logging.getLogger('tbot')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(tbot, telegram_id))
    headers = {
        'Authorization': 'Token {}'.format(dvmn_token)
    }
    payload = {}
    logger.debug('Бот запущен')
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
            logger.warning('Потеряно соединение с сервером')
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
            payload['timestamp'] = review_info['timestamp_to_request']


if __name__ == '__main__':
    main()
