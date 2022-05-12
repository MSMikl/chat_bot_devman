import telegram

from environs import Env

if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env('TELEGRAM_TOKEN')
    tbot = telegram.Bot(token=token)
    user = tbot.getChat(176649151)
    tbot.sendMessage(176649151, 'Hello, {} {}'.format(user['first_name'], user['last_name']))

