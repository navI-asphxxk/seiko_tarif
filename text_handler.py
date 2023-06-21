import telebot
from telebot import types

from menues import main_menu

from config import BOT_TOKEN, admin_id, available_users

from txtmsg import study_dict, individual_less, write_curator, maraffon


bot = telebot.TeleBot(BOT_TOKEN)


class CheckText:
    def __init__(self, message):
        self.text = message.text
        self.chat_id = message.chat.id

    def check_study_dict_text(self):
        if self.text == '🎓Библиотека знаний':
            bot.send_message(self.chat_id, text=study_dict, parse_mode='MarkdownV2', reply_markup=main_menu())

    def check_individual_less_text(self):
        if self.text == '📅Записаться на 1 индивидуальный урок':
            markup = types.InlineKeyboardMarkup(row_width=1)
            b1 = types.InlineKeyboardButton("✍️Написать куратору", url="https://t.me/elizaveta_seiko")
            markup.add(b1)

            bot.send_message(self.chat_id, text=individual_less, parse_mode='MarkdownV2', reply_markup=markup)

    def check_write_curator_text(self):
        if self.text == '📢Связаться с куратором курсов':
            bot.send_message(self.chat_id, text=write_curator, parse_mode='MarkdownV2', reply_markup=main_menu())

    def check_maraffon_text(self):
        if self.text == '👉Выбрать марафон':
            bot.send_message(self.chat_id, text=maraffon, parse_mode='MarkdownV2', reply_markup=main_menu())
            try:
                bot.send_document(self.chat_id, open('maraffons.pdf', 'rb'), timeout=10)
            except Exception:
                bot.send_message(self.chat_id, text="Ошибка загрузки документа. Попробуйте загрузить снова, или напишите нам",
                                 reply_markup=main_menu())


def check_text(message):
    m = CheckText(message)
    m.check_study_dict_text()
    m.check_write_curator_text()
    m.check_individual_less_text()
    m.check_maraffon_text()
