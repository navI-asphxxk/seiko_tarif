import sys
import json
import telebot
from telebot import types
from threading import Thread


from datetime import date

from menues import main_menu, admin_menu

from config import BOT_TOKEN, admin_id, available_users, is_first_use, is_deleted_user, owner_id

from txtmsg import welcome_msg, add_available_user, adm_welcome, delete_available_user, error_access
from txtmsg import copy_msg, get_copy_msg, add_admin, delete_admin

from text_handler import check_text

from timer import update_time_access


bot = telebot.TeleBot(BOT_TOKEN)
timer_thread = Thread()


@bot.message_handler(func=lambda message: str(message.chat.id) not in available_users.keys())
def block(message):
    bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


@bot.message_handler(commands=['start'])
def start(message):
    flag1 = is_first_use.get(str(message.chat.id))
    #flag2 = is_deleted_user.get(str(message.chat.id))

    Thread(target=hello, args=(message,)).start()
    if is_first_use:
        is_first_use.update({str(message.chat.id): False})

        global timer_thread
        timer_thread = Thread(target=update_time_access, args=(str(message.chat.id), flag1))
        timer_thread.start()


def hello(message):
    bot.send_message(message.chat.id, text=welcome_msg(str(message.chat.id)),
                     reply_markup=main_menu(), parse_mode='MarkdownV2')


@bot.message_handler(commands=['admin'])
def admin(message):
    if str(message.chat.id) in admin_id:
        bot.send_message(message.chat.id, text=adm_welcome, reply_markup=admin_menu(), parse_mode='MarkdownV2')
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


@bot.message_handler(func=lambda message: message.text == '✅Предоставить доступ пользователю')
def check_add_user_text(message):
    if str(message.chat.id) in admin_id:
        msg = bot.send_message(message.chat.id, text=add_available_user, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, add_user_access)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def add_user_access(message):
    #print(message.forward_from)
    try:
        access = message.forward_from.id

        if str(access) in admin_id:
            bot.send_message(message.chat.id, text="У Администратора уже есть доступ")
        else:
            if (access != None):
                available_users.update({str(access): 0})
                is_first_use.update({str(access): True})
                print(available_users)
                bot.send_message(message.chat.id, text="Пользователь успешно добавлен\n"
                                                       "Продлить время доступа можно *ПО ЗАВЕРШЕНИЮ ТЕКУЩЕГО ПЛАНА*",
                                 parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, text="Не удалось добавить пользователя!\n"
                                                       "Ошибка доступа - пользователю необходимо поменять настройки приватности в настройках")
    except Exception:
        bot.send_message(message.chat.id, text="Неправильный ввод команды, попробуйте снова")


@bot.message_handler(func=lambda message: message.text == '❌Удалить пользователя из доступа')
def check_delete_admin_text(message):
    if str(message.chat.id) in admin_id:
        msg = bot.send_message(message.chat.id, text=delete_available_user, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, delete_user_access)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def delete_user_access(message):
    #print(message.forward_from)
    try:
        access = message.forward_from.id

        if str(access) in admin_id:
            bot.send_message(message.chat.id, text="Нельзя удалить доступ Администратору")
        else:
            if (access is not  None):
                available_users.pop(str(access))
                print(available_users)
                #is_deleted_user.update({str(access): True})
                bot.send_message(message.chat.id, text="Пользователь успешно удален")
            else:
                bot.send_message(message.chat.id, text="Не удалось удалить пользователя!\n"
                                                       "Ошибка доступа - пользователю необходимо поменять настройки приватности в настройках")
    except Exception:
        bot.send_message(message.chat.id, text="Неправильный ввод команды, попробуйте снова || У пользователя  и так нет доступа")


@bot.message_handler(func=lambda message: message.text == '⚠️Добавить администратора')
def check_add_admin_text(message):
    if message.chat.id in owner_id:
        msg = bot.send_message(message.chat.id, text=add_admin, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, add_admin_access)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def add_admin_access(message):
    try:
        access = message.forward_from.id

        if str(access) in admin_id:
            bot.send_message(message.chat.id, text="У Администратора уже есть доступ")
        else:
            if (access != None):
                admin_id.append(str(access))
                available_users.update({str(access): None})

                bot.send_message(message.chat.id, text="Администратор успешно добавлен\n",
                                 parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, text="Не удалось добавить администратора!\n"
                                                       "Ошибка доступа - пользователю необходимо поменять настройки приватности в настройках")
    except Exception:
        bot.send_message(message.chat.id, text="Неправильный ввод команды, попробуйте снова")


@bot.message_handler(func=lambda message: message.text == '🚫Удалить администратора')
def check_delete_admin_text(message):
    if message.chat.id in owner_id:
        msg = bot.send_message(message.chat.id, text=delete_admin, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, delete_admin_access)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def delete_admin_access(message):
    try:
        access = message.forward_from.id
        if (access != None):
            admin_id.remove(str(access))
            available_users.pop(str(access))

            bot.send_message(message.chat.id, text="Администратор успешно удален\n",
                             parse_mode='MarkdownV2')
        else:
            bot.send_message(message.chat.id, text="Не удалось удалить администратора!\n"
                                                   "Ошибка доступа - пользователю необходимо поменять настройки приватности в настройках")

    except Exception:
        bot.send_message(message.chat.id, text="Неправильный ввод команды, попробуйте снова || У пользователя  и так нет доступа")


@bot.message_handler(func=lambda message: message.text == '💾Резервная копия')
def check_copy_text(message):
    if str(message.chat.id) in admin_id:
        with open('database/lastCopyDate.json', 'r') as f:
            cd = json.load(f)
        bot.send_message(message.chat.id, text=f"*Последняя копия:* {cd} МСК", parse_mode='MarkdownV2')

        msg = bot.send_message(message.chat.id, text=copy_msg, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, do_copy)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def do_copy(message):
    try:
        if message.text == 'Подтвердить':
            with open('database/usersTimes.json', 'w') as f:
                json.dump(available_users, f)

            with open('database/lastCopyDate.json', 'w') as f:
                json.dump(date, f)

            bot.send_message(message.chat.id, text="Копия успешно создана")
        else:
            bot.send_message(message.chat.id, text="Ошибка ввода", parse_mode='MarkdownV2')
    except Exception:
        bot.send_message(message.chat.id, text="Возникла ошибка, попробуйте снова")


@bot.message_handler(func=lambda message: message.text == '🔄Восстановить сохранение')
def check_reset_text(message):
    if str(message.chat.id) in admin_id:
        with open('database/lastCopyDate.json', 'r') as f:
            cd = json.load(f)
        bot.send_message(message.chat.id, text=f"*Последняя копия:* {cd} МСК", parse_mode='MarkdownV2')

        msg = bot.send_message(message.chat.id, text=get_copy_msg, parse_mode='MarkdownV2')
        bot.register_next_step_handler(msg, get_copy)
    else:
        bot.send_message(message.chat.id, text=error_access, parse_mode='MarkdownV2')


def get_copy(message):
    try:
        if message.text == 'Подтвердить':
            with open('database/usersTimes.json', 'r') as f:
                data = json.load(f)
            available_users.update(data)

            #with open('database/usersFirstUse.json', 'r') as f:
            #    data = json.load(f)
            #is_first_use.update(data)

            for key, value in is_first_use.items():
                is_first_use[key] = True

            bot.send_message(message.chat.id, text="Копия успешно загружена")
        else:
            bot.send_message(message.chat.id, text="Ошибка ввода", parse_mode='MarkdownV2')
    except Exception:
        bot.send_message(message.chat.id, text="Возникла ошибка, попробуйте снова")


@bot.message_handler(content_types=['text'])
def get_text(message):
    check_text(message)


bot.polling(none_stop=True)