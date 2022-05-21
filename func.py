import config
import db
import json
import menu
import random

import datetime
import telebot
from bs4 import BeautifulSoup as bs

bot = telebot.TeleBot(config.BOT_TOKEN)

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def first_start(user_id, name):
    conn, cursor = db.connect()
    if db.get_value('value', base='adm_id') is None:
        cursor.execute('insert into adm_id values(?)', (user_id,))
        conn.commit()
    conn.commit()
    cursor.close()
    conn.close()

def get_user(user_id):
    conn, cursor = db.connect()
    user = cursor.execute('select * from users where user_id=?', (user_id,)).fetchone()
    cursor.close()
    conn.close()
    return user



def is_adm(id):
    if db.get_value('value', 'value', id, 'adm_id') is not None:
        return True
    else:
        return False


def is_ohr(id):
    if db.get_value('value', 'value', id, 'ohr_id') is not None:
        return True
    else:
        return False

def add_adm(message):
    id = message.text
    if id.isdigit() is False:
        id = id.replace('@', '')
        id = db.get_value('user_id', 'name', id, 'users')
    if db.get_value('*', 'user_id', id, 'users') is not None:
        db.add_adm(id)
        bot.send_message(chat_id=message.chat.id, text=f'Выдал админку пользователю {id}', reply_markup=menu.adm_menu)
    else:
        bot.send_message(chat_id=message.chat.id, text=f'Нет такого пользователя в базе', reply_markup=menu.adm_menu)


def remove_adm(message):
    id = message.text
    if id.isdigit() is False:
        id = id.replace('@', '')
        id = db.get_value('user_id', 'name', id, 'users')
    if db.get_value('*', 'user_id', id, 'users') is not None:
        db.remove_adm(id)
        bot.send_message(chat_id=message.chat.id, text=f'Удалил админа {id}', reply_markup=menu.adm_menu)
    else:
        bot.send_message(chat_id=message.chat.id, text=f'Нет такого пользователя в базе', reply_markup=menu.adm_menu)


def add_ohr(message):
    id = message.text
    if id.isdigit() is False:
        id = id.replace('@', '')
        id = db.get_value('user_id', 'name', id, 'users')
    if db.get_value('*', 'user_id', id, 'users') is not None:
        db.add_kur(id)
        bot.send_message(chat_id=message.chat.id, text=f'Выдал охрану пользователю {id}', reply_markup=menu.adm_menu)
    else:
        bot.send_message(chat_id=message.chat.id, text=f'Нет такого пользователя в базе', reply_markup=menu.adm_menu)


def remove_ohr(message):
    id = message.text
    if id.isdigit() is False:
        id = id.replace('@', '')
        id = db.get_value('user_id', 'name', id, 'users')
    if db.get_value('*', 'user_id', id, 'users') is not None:
        db.remove_kur(id)
        bot.send_message(chat_id=message.chat.id, text=f'Удалил охрану {id}', reply_markup=menu.adm_menu)
    else:
        bot.send_message(chat_id=message.chat.id, text=f'Нет такого пользователя в базе', reply_markup=menu.adm_menu)


