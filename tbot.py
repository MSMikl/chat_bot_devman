import telegram

from environs import Env


def bot_message(id, text):
    env = Env()
    env.read_env()
    token = env('TELEGRAM_TOKEN')
    tbot = telegram.Bot(token=token)
    tbot.sendMessage(id, text)


if __name__ == '__main__':
    bot_message()