import sys
import telebot
from threading import Timer, Event
import time

from config import available_users, BOT_TOKEN, access_time


bot = telebot.TeleBot(BOT_TOKEN)


def update_time_access(key, is_first_use):
    deleted_user = False
    try:
        while not deleted_user:
            if is_first_use:
                cur_time = int(available_users.get(key))
                print(available_users.get(key))

                while available_users.get(key) is not None:
                    while cur_time < access_time:
                        if available_users.get(key) is None:
                            deleted_user = True
                            break

                        cur_time += 1
                        available_users[key] = cur_time

                        time.sleep(1)
                        print(available_users)

                    available_users.pop(key)
                    print(available_users)

    except Exception:
        print("Счетчика времени у администратора нет | Ошибка в использовании команд")
