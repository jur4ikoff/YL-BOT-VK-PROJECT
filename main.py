import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tokens import main_token

import datetime
from flask import Flask, render_template, redirect, request, make_response, url_for, abort, jsonify
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from flask.sessions import *
from flask_restful import reqparse, abort, Api, Resource
from wtforms.validators import DataRequired
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from data import db_session

vk_session = vk_api.VkApi(token=main_token)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

def db_create():
    db_session.global_init("db/Vk_bot.db")


def sender(text, id):
    vk_session.method('messages.send', {'user_id': id, 'message': text, 'random_id': 0})


def if_msg_hello(msg, id):
    if msg.lower() == 'привет':
        sender(id=id, text='И тебе привет!')

db_create()

for event in longpool.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text
            id = event.user_id
            if_msg_hello(id=id, msg=msg)


