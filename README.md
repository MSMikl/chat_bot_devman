# chat_bot_devman
 
Чат-бот присылает уведомления о проверке работ на [dvmn.org](https://dvmn.org/modules/)

## Установка 

Python 3 должен быть установлен

Скачать файлы из репозитория. Установить зависимости, выполнив

    pip install -r requirements.txt

## Настройка

В папке с `main.py` создать файл `env`, в который записать следующие ключи:

     DEVMAN_TOKEN = ### Токен от API Devman
     TELEGRAM_TOKEN = ### Токен телеграм-бота
     TG_USER_ID = ### ID пользователя Телеграм, которому будут отправляться сообщения
     
## Запуск

Выполнить в консоли
   
     main.py
     
Бот будет постоянно проверять статус проверки работ и присылать уведомления в случае их возврата с результатом.
