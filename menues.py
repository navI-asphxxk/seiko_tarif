from telebot import types

def admin_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    b1 = types.KeyboardButton("✅Предоставить доступ пользователю")
    b2 = types.KeyboardButton("❌Удалить пользователя из доступа")
    b3 = types.KeyboardButton("⚠️Добавить администратора")
    b4 = types.KeyboardButton("🚫Удалить администратора")
    b5 = types.KeyboardButton("💾Резервная копия")
    b6 = types.KeyboardButton("🔄Восстановить сохранение")

    markup.add(b1)
    markup.add(b2)
    markup.add(b3)
    markup.add(b4)
    markup.add(b5, b6)

    return markup

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    b1 = types.KeyboardButton(text='🎓Библиотека знаний')
    b2 = types.KeyboardButton(text='👉Выбрать марафон')
    b3 = types.KeyboardButton(text='📅Записаться на 1 индивидуальный урок')
    b4 = types.KeyboardButton(text='📢Связаться с куратором курсов')

    markup.add(b1)
    markup.add(b2)
    markup.add(b3)
    markup.add(b4)

    return markup

