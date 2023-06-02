#!/usr/bin/python3

#########LIBS##########################
import re, json
import sqlite3, random, os, datetime, time, subprocess
import uuid
import telebot
import config, menu, func, db, os
from config import BOT_TOKEN
from telebot import types
import RPi.GPIO as GPIO
#######################################
white = 20
yellow = 26
red = 19
green = 16
#######################################
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#LED White
GPIO.setup(white, GPIO.OUT)
GPIO.output(white, 1) #Off initially
#LED Yellow
GPIO.setup(yellow, GPIO.OUT)
GPIO.output(yellow, 1) #Off initially
#LED Red
GPIO.setup(red, GPIO.OUT)
GPIO.output(red, 1) #Off initially
#LED green
GPIO.setup(green, GPIO.OUT)
GPIO.output(green, 1) #Off initially

###############START-FUNCTION###########
def start_bot():
    print(f'Telegram cлужба успешно запущена! : {datetime.datetime.now()}\n')
    db.db()
    bot = telebot.TeleBot(config.BOT_TOKEN)


    @bot.message_handler(commands=['start'])
    def handler_start(message):
        chat_id = message.chat.id
        name = message.from_user.username
        func.first_start(chat_id,name)
        user = func.get_user(chat_id)

        if func.is_adm(chat_id):
            bot.send_photo(chat_id=message.chat.id,caption=f'Привет {name}. Я к твоим услугам',reply_markup=menu.adm_menu,photo=open('welcome.jpeg','rb'))
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        elif func.is_ohr(chat_id):
            bot.send_photo(chat_id=message.chat.id,caption=f'Привет {name}. Я к твоим услугам',reply_markup=menu.adm_menu,photo=open('welcome.jpeg','rb'))
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        else:
            bot.send_message(chat_id=message.chat.id,text=f'Проваливай, или я щас охрану вызову!',reply_markup=menu.main_menu)
            bot.delete_message(chat_id=chat_id, message_id=message.message_id)
################LOCK-FUNCTION##############
    @bot.callback_query_handler(func=lambda call: True)
    def handler_call(call):
        message_id = call.message.message_id
        chat_id = call.message.chat.id

        if call.data == 'keyimaginer':
            user = func.get_user(chat_id)
            try:
                if func.is_adm(chat_id):
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=f'Меню управления замками',reply_markup=menu.adm_zamok1)
                elif func.is_ohr(chat_id):
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=f'Меню управления замками',reply_markup=menu.ohr_zamok1)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'Вы не имеете права управлять замками',reply_markup=menu.main_zamok1)
            except Exception as e:
                print(e)
######################OTMENA############
        if call.data == 'cansel_button':
            bot.delete_message(chat_id=chat_id, message_id=message_id)
            bot.clear_step_handler(call.message)
############ADMIN/OHRANA MENU###########
        if call.data == 'exit_to_adm_menu':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                          caption='Ты вернулся в главное меню. Я к твоим услугам', reply_markup=menu.adm_menu)
                except Exception as e:
                    print(e)
########################################
        if call.data == 'on_off_lock':
            if func.is_adm(call.message.chat.id):

                try:
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id,caption='OPEN/CLOSE',reply_markup=menu.on_off_lock())
                except Exception as e:
                    print(e)
########################################

        if call.data == 'add_adm':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, кому выдать админку ',reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_adm)

        if call.data == 'remove_adm':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, у кого забрать админку ',reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_adm)

        if call.data == 'add_ohr':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, кому выдать охрану ',reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.add_kur)

        if call.data == 'remove_ohr':
            if func.is_adm(call.message.chat.id):
                msg = bot.send_message(chat_id=chat_id, text='➕Введи ID\ссылку пользователя, у кого забрать охрану ',reply_markup=menu.cansel_button)
                bot.register_next_step_handler(msg, func.remove_kur)



        if call.data == 'funcs_config':
            if func.is_adm(call.message.chat.id):
                db.set_funcs_value('need_func1')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Включение / выключение функций', reply_markup=menu.on_off_lock())




        if call.data == 'func1_config':
            if func.is_adm(call.message.chat.id):
                db.set_funcs_value('need_func1')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Включение / выключение функций', reply_markup=menu.on_off_lock())


        if call.data == 'func2_config':
            if func.is_adm(call.message.chat.id):
                db.set_funcs_value('need_func2')
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Включение / выключение функций', reply_markup=menu.on_off_lock())

        if call.data == 'on_off_lock':
            if func.is_adm(call.message.chat.id):
                # db.set_payments_value()
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='▶Включение\\выключение ФУНКЦИЙ', reply_markup=menu.on_off_lock())

################################
        if call.data == 'exit_to_ohr_menu':
            if func.is_kur(call.message.chat.id):
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id,text='♻️ Привет, охрана. Что мне нужно сделать ?', reply_markup=menu.ohr_menu, parse_mode='HTML')
                except Exception as e:
                    print(e)
###############################
        if call.data == 'users_config':
            if func.is_adm(call.message.chat.id):
                try:
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                          caption='Вы перешли к настройке пользователей!',reply_markup=menu.users_config)
                except:
                    pass


###############################
        if call.data == 'exit_to_menu':
                bot.clear_step_handler(call.message)

                if func.is_adm(chat_id):
                    bot.send_message(chat_id=chat_id, text='ADMINTEXT',reply_markup=menu.adm_main_menu)
                    bot.delete_message(chat_id=chat_id,message_id=message_id)
                elif func.is_ohr(chat_id):
                    bot.send_message(chat_id=chat_id, text='OHRANATEXT',reply_markup=menu.ohr_main_menu)
                    bot.delete_message(chat_id=chat_id,message_id=message_id)
                else:
                    bot.send_message(chat_id=chat_id,text='BOMZHTEXT',reply_markup=menu.main_menu)
                    bot.delete_message(chat_id=chat_id,message_id=message_id)


###############################
        if call.data == 'info':
            try:
                if func.is_adm(chat_id):
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=db.get_value('info_message'),
                                          reply_markup=menu.adm_menu)
                elif func.is_kur(chat_id):
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=db.get_value('info_message'),
                                          reply_markup=menu.ohr_menu)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=db.get_value('info_message'),
                                          reply_markup=menu.main_menu)
            except:
                pass


###############################
        if call.data == 'glazok':
            print(f'Фото с глазка! : {datetime.datetime.now()}')
            try:
                if func.is_adm(chat_id):
                        
                        cmd = 'raspistill -o /home/main/unlocker/photo.jpg'
                        
                        bot.send_photo(chat_id=chat_id, reply_markup=menu.adm_menu, photo=open('photo.jpg','rb'),caption='Фото с глазка')
                        bot.delete_message(chat_id=chat_id,message_id=message_id)
                        #bot.delete_message(chat_id=chat_id,message_id=message_id -1)
                        #bot.delete_message(chat_id=chat_id,message_id=message_id)
                elif func.is_ohr(chat_id):
                        bot.edit_message_text(chat_id=chat_id,message_id=message_id, text='Фото с глазка <string>',reply_markup=menu.ohr_main_menu)

                else:
                        bot.edit_message_text(chat_id=chat_id,message_id=message_id,text='У вас нет необходимых полномочий!',reply_markup=menu.main_menu)

            except Exception as e:
                raise e
            finally:
                GPIO.output(red, 0) #Эмуляция концевика
                pass #
###############################
        if call.data == 'cran_off':
            print(f'Водопровод закрытый! : {datetime.datetime.now()}')
            try:
                if func.is_adm(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Вода перекрыта',reply_markup=menu.adm_menu)
                elif func.is_ohr(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Вода перекрыта',reply_markup=menu.ohr_main_menu)
                        bot.delete_message(chat_id=chat_id,message_id=message_id)
                else:
                        bot.edit_message_text(chat_id=chat_id,message_id=message_id,text='У вас нет необходимых полномочий!',reply_markup=menu.main_menu)
            except Exception as e:
                raise e
            finally:
                GPIO.output(green, 0) #Эмуляция концевика
###############################
        if call.data == 'zamokopen':
            print(f'Дверь открыта! : {datetime.datetime.now()}')
            try:
                if func.is_adm(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Дверь открыта',reply_markup=menu.adm_menu)
                        GPIO.output(white, 0)
                        GPIO.output(yellow, 0)
                        time.sleep(0.25)
                        GPIO.output(white, 1)
                        GPIO.output(yellow, 1)
                elif func.is_ohr(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Дверь открыта',reply_markup=menu.ohr_main_menu)
                        GPIO.output(white, 0)
                        GPIO.output(yellow, 0)
                        time.sleep(0.25)
                        GPIO.output(white, 1)
                        GPIO.output(yellow, 1)
                else:
                        bot.edit_message_text(chat_id=chat_id,message_id=message_id,text='У вас нет необходимых полномочий!',reply_markup=menu.main_menu)
            except Exception as e:
                raise e
################################
        if call.data == 'zamokclose':
            print(f'Дверь закрыта! : {datetime.datetime.now()}')
            try:
                if func.is_adm(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Дверь закрыта',reply_markup=menu.adm_menu)
                        GPIO.output(red, 0)
                        GPIO.output(green, 0)
                        time.sleep(0.2)
                        GPIO.output(red, 1)
                        GPIO.output(green, 1)
                elif func.is_ohr(chat_id):
                        bot.edit_message_caption(chat_id=chat_id,message_id=message_id, caption='Дверь закрыта',reply_markup=menu.ohr_main_menu)
                        GPIO.output(red, 0)
                        GPIO.output(green, 0)
                        time.sleep(0.2)
                        GPIO.output(red, 1)
                        GPIO.output(green, 1)
                else:
                        bot.edit_message_text(chat_id=chat_id,message_id=message_id,text='У вас нет необходимых полномочий!',reply_markup=menu.main_menu)
            except Exception as e:
                raise e
##############################
    def telegram_polling():
        try:
            bot.polling(none_stop=True, timeout=60)  # constantly get messages from Telegram
        except Exception as e:
            print(f'\n---------------------------\nВремя ошибки: {datetime.datetime.now()}\n{e}\n-------------------------\n')
            bot.stop_polling()
            time.sleep(10)
            telegram_polling()

    telegram_polling()
start_bot()
