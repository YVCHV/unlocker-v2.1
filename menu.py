import telebot
from telebot import types
import sqlite3,db

main_menu = types.InlineKeyboardMarkup()
main_menu.add(
    types.InlineKeyboardButton(text='🔐Управление замком',callback_data='keyimaginer'),
    types.InlineKeyboardButton(text='Версия',callback_data='info')
)
###################################
adm_main_menu = types.InlineKeyboardMarkup()
adm_main_menu.add(
    types.InlineKeyboardButton(text='🔐Управление замком',callback_data='keyimaginer')
)
adm_main_menu.add(
    types.InlineKeyboardButton(text='🔰  НАЗАД ',callback_data='exit_to_adm_menu')
)
####################################
ohr_main_menu = types.InlineKeyboardMarkup()
ohr_main_menu.add(
    types.InlineKeyboardButton(text='🔐Управление замком',callback_data='keyimaginer')
)
ohr_main_menu.add(
    types.InlineKeyboardButton(text='🔰 Меню охраны',callback_data='exit_to_ohr_menu')
)

adm_zamok1 = types.InlineKeyboardMarkup(row_width = 2)
adm_zamok1.add(
    types.InlineKeyboardButton (text= '🔑  🔓',callback_data='zamokopen'),
    types.InlineKeyboardButton (text= '🔑  🔒',callback_data='zamokclose')
)
adm_zamok1.add(
    types.InlineKeyboardButton (text= '↩️ Назад',callback_data='exit_to_adm_menu')
)


users_config = types.InlineKeyboardMarkup(row_width=1)
users_config.add(
    types.InlineKeyboardButton(text='🔓 Выдать админа',callback_data='add_adm'),
    types.InlineKeyboardButton(text='🔒 Забрать админа',callback_data='remove_adm')
#    types.InlineKeyboardButton(text='🔓 Выдать охрану',callback_data='add_ohr'),
#    types.InlineKeyboardButton(text='🔒 Забрать охрану',callback_data='remove_ohr')
)
users_config.add(types.InlineKeyboardButton(text='↩️ Назад',callback_data='exit_to_adm_menu'))


adm_menu = types.InlineKeyboardMarkup(row_width=2)
adm_menu.add(
    #types.InlineKeyboardButton(text='🔐 Управление замками  🔐',callback_data='keyimaginer'),
    types.InlineKeyboardButton(text='🔑 ',callback_data='zamokopen'),
    types.InlineKeyboardButton(text='🔒',callback_data='zamokclose'),
    types.InlineKeyboardButton(text='📸',callback_data='glazok'),
    types.InlineKeyboardButton(text='🚰',callback_data='cran_off')
)
adm_menu.add(types.InlineKeyboardButton(text='⚙️ Администрирование',callback_data='users_config'))
adm_menu.add(types.InlineKeyboardButton(text='Версия',callback_data='info'))

#adm_menu.add(types.InlineKeyboardButton(text='❌ Выйти',callback_data='exit_to_menu'))


funcs_config = types.InlineKeyboardMarkup(row_width=1)
funcs_config.add(
    types.InlineKeyboardButton(text='▶ FUNCS',callback_data='on_off_lock'),
    types.InlineKeyboardButton(text='↩️ Назад',callback_data='exit_to_adm_menu')
)


ohr_menu = types.InlineKeyboardMarkup()
ohr_menu.add(
    types.InlineKeyboardButton(text='🔐 Управление замками',callback_data='keyimaginer'),
    #types.InlineKeyboardButton(text='📷 Управление камерами',callback_data='cameramanager'),
    #types.InlineKeyboardButton(text='😺   Покормить киску',callback_data='secdoneyes')
)
#ohr_menu.add(
#    types.InlineKeyboardButton(text='↩️ Выйти',callback_data='exit_to_menu')



zamok1_config =types.InlineKeyboardMarkup(row_width=1)
zamok1_config.add(
    types.InlineKeyboardButton(text='LOCK/UNLOCK',callback_data='on_off_lock'),
    types.InlineKeyboardButton(text='↩Назад',callback_data='exit_to_adm_menu')
)

cansel_button = types.InlineKeyboardMarkup()
cansel_button.add(types.InlineKeyboardButton(text='❌ Отмена',callback_data='cansel_button'))



def on_off_lock():
    if db.get_value('need_func1') == 1:
        func1_text = '🟢 FUNC1'
    else:
        func1_text = '🔴 FUNC1'
    if db.get_value('need_func2') == 1:
        func2_text = '🟢 FUNC2'
    else:
        func2_text = '🔴FUNC2'
    on_off_lock = types.InlineKeyboardMarkup(row_width=2)
    on_off_lock.add(
        types.InlineKeyboardButton(text=func1_text, callback_data='func1_config'),
        types.InlineKeyboardButton(text=func2_text, callback_data='func2_config'),
        types.InlineKeyboardButton(text='↩ Назад', callback_data='exit_to_adm_menu')
    )
    return on_off_lock
