from vk_api.longpoll import VkLongPoll, VkEventType
from tokens import bot_token as TOKEN
from tokens import user_token
from data.users import User
import vk_api
import random
import datetime
from flask.sessions import *
from data import db_session
import wikipedia

from flask import Flask, render_template, redirect, request, make_response, url_for, abort, jsonify
from flask_wtf import FlaskForm
from flask_restful import reqparse, abort, Api, Resource
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)


def db_create():
    db_session.global_init("db/Vk_bot.db")


def add_db(id, first_name, last_name, sex, bdate, city):  # Добавление в Дб
    db_session.global_init("db/Vk_bot.db")
    user = User()
    user.vk_id = id
    user.name = first_name
    user.surname = last_name
    user.city = city
    user.bdate = bdate
    user.sex = sex
    db_sess = db_session.create_session()
    db_sess.add(user)
    db_sess.commit()


def main():
    db_session.global_init("db/Vk_bot.db")
    db_sess = db_session.create_session()
    user_id = 363431143
    group_id = 211995313
    album_id = 285867774
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                user_name = None  # Заглушка
                user_surname = None
                is_first_msg = True  # Проеверка на первое сообщение
                for user in db_sess.query(User).all():
                    if user.vk_id == id:
                        user_name = user.name  # Берем ФИО из Дб
                        user_surname = user.surname
                        is_first_msg = False
                if is_first_msg:
                    # Если первое сообщение >>> Приветствие
                    vk.messages.send(peer_id=id, random_id=0, message='Привет, это бот для проекта. \n'
                                                                      'Ниже прикреплены команды бота ')
                    first_name, last_name, sex, bdate, city = get_info(vk, vk_session, id)  # Получаем информацию
                    add_db(id, first_name, last_name, sex, bdate, city)  # Добавляем в дб
                else:
                    # Если есть в базе данных >>>
                    vk.messages.send(peer_id=id, random_id=0,
                                     message=f'Я тебя помню, тебя зовут - {user_name} {user_surname} . \n'
                                             'чтобы узнать о командах напишите "/help" ')


def get_info(vk, vk_session, id):
    responce = vk.users.get(user_ids=id, fields='city,bdate,city,sex')
    firstname, last_name, sex, bdate, city = None, None, None, None, None
    if responce:
        responce_1 = responce[0]
        firstname = responce_1["first_name"]  # имя
        last_name = responce_1["last_name"]  # Фамилия
        sex1 = responce_1["sex"]
        if sex1 == 2:
            sex = 'Man'
        if sex1 == 1:
            sex = 'Woman'  # Пол
        try:
            bdate = responce_1["bdate"]
            city = responce_1["city"]["title"]

        except KeyError:
            pass
    return firstname, last_name, sex, bdate, city


def get_photos(album_id, group_id, id, vk):
    photos = []
    vk_user_session = vk_api.VkApi(token=user_token)
    vk_user = vk_user_session.get_api()
    response = vk_user.photos.get(album_id=album_id, group_id=group_id)
    if response["items"]:
        for i in range(int(response["count"])):
            photos_id = f'https://vk.com/photo{response["items"][i]["owner_id"]}_{response["items"][i]["id"]}'
            photos.append(photos_id)
    attachment = photos[random.randint(0, len(photos) - 1)]
    attachment = attachment.split('/')
    attachment = attachment[3]
    print(attachment)
    vk.messages.send(peer_id=id, random_id=0, attachment=attachment)


def send_time_now(event, vk, id, time_flag):
    weekday = ['понедельник', 'вторник', "среда", "четверг", "пятница", "суббота", "воскресенье"]
    msc = datetime.datetime.now()
    if time_flag:
        vk.messages.send(user_id=id,
                         message=f"Дата: {msc.day}.{msc.month}.{msc.year}, время: {msc.hour}:{msc.minute},"
                                 f" день недели: {weekday[msc.weekday()]}",
                         random_id=random.randint(0, 2 ** 64))
    else:
        vk.messages.send(user_id=id,
                         message=f'вы можете увидеть время по ключевым словам: «время», «число», «дата», «день»',
                         random_id=random.randint(0, 2 ** 64))


def wiki_search(vk, id, msg):
    global count_1
    wikipedia.set_lang('ru')
    try:
        a = wikipedia.summary(msg)
        vk.messages.send(user_id=id,
                         message=a,
                         random_id=random.randint(0, 2 ** 64))
        vk.messages.send(user_id=id,
                         message=f'Новый поисковый запрос:',
                         random_id=random.randint(0, 2 ** 64))
    except Exception:
        vk.messages.send(user_id=id,
                         message=f'Ошибка, Введите заново:',
                         random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
