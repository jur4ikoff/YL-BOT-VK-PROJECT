from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from tokens import bot_token as TOKEN
from find_spn import check_spn
from data.users import User
import vk_api
import requests
import random
from io import BytesIO
from PIL import Image
from data import db_session
import sys
import wikipedia

vk_session = vk_api.VkApi(token=TOKEN)
session_api = vk_session.get_api()
longpool = VkLongPoll(vk_session)

lang_flag = False


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


def help(vk, id):
    vk.messages.send(peer_id=id, random_id=0,
                     message=f'"/info" - Получить информацию о адрессе \n'
                             f'"/org" - Информация об организации \n'
                             f'"/map" - Получить информацию по координатам \n'
                             f'"/metro" - Поиск ближайшего метро \n'
                             f'"/wiki" - Поиск по запросу \n'
                             f'/get_vk_info - Поиск информации о юзере вк. \n')


def main():
    global lang_flag
    global wiki_msg
    global commands_history
    db_session.global_init("db/Vk_bot.db")
    db_sess = db_session.create_session()
    user_id = 363431143
    group_id = 211995313
    album_id = 285867774
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    hello_count = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                id = event.user_id
                user_name = None  # Заглушка
                user_surname = None
                is_first_msg = True  # Проверка на первое сообщение
                for user in db_sess.query(User).all():
                    if user.vk_id == id:
                        user_name = user.name  # Берем ФИО из Дб
                        user_surname = user.surname
                        is_first_msg = False
                msg = event.text.lower()
                print(user_name, msg)
                if hello_count == 0:
                    if is_first_msg:
                        # Если первое сообщение >>> Приветствие
                        vk.messages.send(peer_id=id, random_id=0, message='Привет, это бот для проекта. \n'
                                                                          'Ниже прикреплены команды бота ')
                        first_name, last_name, sex, bdate, city = get_info(vk, id)  # Получаем информацию
                        add_db(id, first_name, last_name, sex, bdate, city)  # Добавляем в дб
                        help(vk, id)
                        hello_count += 1
                    else:
                        # Если есть в базе данных >>>
                        vk.messages.send(peer_id=id, random_id=0,
                                         message=f'Я тебя помню, тебя зовут - {user_name} {user_surname} . \n'
                                                 'чтобы узнать о командах напишите "/help" ')
                        hello_count += 1
                if msg == '/help':
                    help(vk, id)
                    get_keyboard_1(vk, id)
                if '/wiki' == msg:
                    wiki_dilog(vk, id, event, vk_session)
                if '/info' == msg:
                    get_geo(vk, id, vk_session)
                if '/org' == msg:
                    get_org(vk, id, vk_session)
                if '/map' == msg:
                    map(vk, id, vk_session)
                if '/metro' == msg:
                    metro(vk, id, vk_session)
                if '/get_vk_info' == msg:
                    vk_info(vk, id, vk_session)


def get_keyboard_1(vk, id):
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button(label='/wiki', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/info', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/org', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/map', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='/metro', color=VkKeyboardColor.PRIMARY)
    # keyboard.add_button(label='/get_vk_info', color=VkKeyboardColor.PRIMARY)
    vk.messages.send(peer_id=id, random_id=0, message='Клавиатура с возможными командами',
                     keyboard=keyboard.get_keyboard())


def get_info(vk, id):
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


def vk_info(vk, id, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите запрос:')
    sys_count = 0
    wikipedia.set_lang('ru')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                find_id = event.text
                firstname, last_name, sex, bdate, city = get_info(vk, find_id)
                print(firstname, last_name, sex, bdate, city)
                vk.messages.send(peer_id=id, random_id=0, message=f'Имя: {firstname} \n'
                                                                  f'Фамилия: {last_name} \n'
                                                                  f'Город: {city} \n'
                                                                  f'Пол: {sex} \n'
                                                                  f'Дата рождения: {bdate} \n')
                if sys_count == 0:
                    vk.messages.send(peer_id=id, random_id=0, message=f'чтобы выйти пропишите /main')


def wiki_dilog(vk, id, event, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите запрос:')
    # time.sleep(5)
    sys_count = 0
    wikipedia.set_lang('ru')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                wiki_msg = event.text
                try:
                    a = wikipedia.summary(wiki_msg)
                    vk.messages.send(user_id=id,
                                     message=a,
                                     random_id=random.randint(0, 2 ** 64))
                    if sys_count == 0:
                        vk.messages.send(user_id=id,
                                         message=f'Чтобы выйти в меню"/main" \n',
                                         random_id=random.randint(0, 2 ** 64))
                        sys_count += 1
                except Exception:
                    if wiki_msg == '/main':
                        help(vk, id)
                        break
                    vk.messages.send(user_id=id,
                                     message=f'Ошибка, Введите заново:',
                                     random_id=random.randint(0, 2 ** 64))

                    continue


def get_geo(vk, id, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите запрос:')
    sys_count = 0
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                city, lower_coords, upper_coords, district = None, None, None, None
                geocode_msg = event.text
                api_server = "http://geocode-maps.yandex.ru/1.x/"
                if geocode_msg == '/main':
                    help(vk, id)
                    break
                params = {
                    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                    "geocode": geocode_msg,
                    "format": "json"
                }
                response = requests.get(api_server, params=params)
                if response:
                    json_response = response.json()
                    try:
                        lower_coords = json_response["response"]["GeoObjectCollection"]["metaDataProperty"][
                            "GeocoderResponseMetaData"]["boundedBy"]["Envelope"]["lowerCorner"]
                        upper_coords = json_response["response"]["GeoObjectCollection"]["metaDataProperty"][
                            "GeocoderResponseMetaData"]["boundedBy"]["Envelope"]["lowerCorner"]
                        city = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                            "metaDataProperty"]["GeocoderMetaData"]["text"]
                        district = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                            "metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][1]["name"]
                    except KeyError:
                        vk.messages.send(user_id=id,
                                         message=f'Ошибка, Введите заново:\n'
                                                 f'Чтобы выйти в меню"/main" \n',
                                         random_id=random.randint(0, 2 ** 64))
                    try:
                        if city:
                            vk.messages.send(user_id=id,
                                             message=f'Город - {city}, координаты - {lower_coords, upper_coords}, \n'
                                                     f'Административный округ - {district}',
                                             random_id=random.randint(0, 2 ** 64))
                        else:
                            vk.messages.send(user_id=id,
                                             message=f'Ничего не найдено',
                                             random_id=random.randint(0, 2 ** 64))
                        if sys_count == 0:
                            vk.messages.send(user_id=id,
                                             message=f'Вы можете повторить запрос в чате.'
                                                     f'Чтобы выйти в меню"/main" \n',
                                             random_id=random.randint(0, 2 ** 64))
                            sys_count += 1
                    except Exception:
                        if geocode_msg == '/main':
                            help(vk, id)
                            break
                        vk.messages.send(user_id=id,
                                         message=f'Ошибка, Введите заново:',
                                         random_id=random.randint(0, 2 ** 64))

                        continue


def get_org(vk, id, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите запрос: Адрес + название заведения')
    sys_count = 0
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    org_msg = event.text
                    search_api_server = "https://search-maps.yandex.ru/v1/"
                    api_key = "8e405774-72a5-4bc5-8061-c703891b2a5f"
                    if org_msg == '/main':
                        help(vk, id)
                        break

                    search_params = {
                        "apikey": api_key,
                        "text": org_msg,
                        "lang": "ru_RU",
                        "type": "biz"
                    }

                    response = requests.get(search_api_server, params=search_params)
                    if response:
                        site2 = None
                        site = None
                        json_response = response.json()
                        org_name = json_response["features"][0]["properties"]["CompanyMetaData"]["name"]
                        org_address = json_response["features"][0]["properties"]["CompanyMetaData"]["address"]
                        try:
                            if json_response["features"][0]["properties"]["CompanyMetaData"]["url"]:
                                site = json_response["features"][0]["properties"]["CompanyMetaData"]["url"]
                        except KeyError:
                            pass
                        phone = json_response["features"][0]["properties"]["CompanyMetaData"]["Phones"][0]["formatted"]

                        org_name2 = json_response["features"][1]["properties"]["CompanyMetaData"]["name"]
                        org_address2 = json_response["features"][1]["properties"]["CompanyMetaData"]["address"]
                        try:
                            if json_response["features"][1]["properties"]["CompanyMetaData"]["url"]:
                                site2 = json_response["features"][1]["properties"]["CompanyMetaData"]["url"]
                        except KeyError:
                            pass
                        phone2 = json_response["features"][1]["properties"]["CompanyMetaData"]["Phones"][0]["formatted"]
                        if site:
                            vk.messages.send(user_id=id,
                                             message=f'Самый ликвидный вариант: \n'
                                                     f'Название: {org_name}, адрес: {org_address} \n'
                                                     f'Сайт: {site} \n'
                                                     f'Телефон: {phone}',
                                             random_id=random.randint(0, 2 ** 64))
                        if not site:
                            vk.messages.send(user_id=id,
                                             message=f'Самый ликвидный вариант: \n'
                                                     f'Название: {org_name}, адрес: {org_address} \n'
                                                     f'Телефон: {phone}',
                                             random_id=random.randint(0, 2 ** 64))

                        if site2:
                            vk.messages.send(user_id=id,
                                             message=f'Второй ближайший магазин: \n'
                                                     f'Название: {org_name2}, адрес: {org_address2} \n'
                                                     f'Сайт: {site2} \n'
                                                     f'Телефон: {phone2}',
                                             random_id=random.randint(0, 2 ** 64))
                        if not site2:
                            vk.messages.send(user_id=id,
                                             message=f'Второй ближайший магазин: \n'
                                                     f'Название: {org_name2}, адрес: {org_address2} \n'
                                                     f'Телефон: {phone2}',
                                             random_id=random.randint(0, 2 ** 64))
                        if sys_count == 0:
                            vk.messages.send(user_id=id,
                                             message=f'Вы можете повторить запрос в чате.  '
                                                     f'Чтобы выйти в меню"/main" \n',
                                             random_id=random.randint(0, 2 ** 64))
                            sys_count += 1
                    else:
                        print("Ошибка выполнения запроса:")
                        print("Http статус:", response.status_code, "(", response.reason, ")")
    except Exception as e:
        vk.messages.send(user_id=id,
                         message=f'Упсс. Ничего не нашлось',
                         random_id=random.randint(0, 2 ** 64))
        print(e)


def map(vk, id, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите координаты: широта долгота \n'
                                                      'Пример: 38.518067 55.419967')
    sys_count = 0
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    coords = event.text
                    if coords == '/main':
                        help(vk, id)
                        break
                    crds = ','.join(coords.split(' '))
                    text = None
                    api_server = "http://geocode-maps.yandex.ru/1.x/"
                    params = {
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "format": "json",
                        "geocode": ','.join(coords.split(' '))
                    }
                    response = requests.get(api_server, params=params)
                    if response:
                        json_response = response.json()
                        rsp = json_response["response"]["GeoObjectCollection"]["featureMember"][0]
                        text = rsp["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                        toponym1 = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                            "boundedBy"]["Envelope"]
                        low_corn, upper_corn = toponym1["lowerCorner"], toponym1["upperCorner"]  # размеры объекта
                        delta1, delta2 = check_spn(low_corn, upper_corn)

                        map_params = {
                            "ll": crds,
                            "spn": ",".join([str(delta1), str(delta2)]),
                            "l": "map"
                        }

                        map_api_server = "http://static-maps.yandex.ru/1.x/"
                        response2 = requests.get(map_api_server, params=map_params)
                        im = Image.open(BytesIO(response2.content))
                        im.save("temp.png")
                        upload = vk_api.VkUpload(vk)
                        photo = upload.photo_messages('temp.png')
                        owner_id = photo[0]['owner_id']
                        photo_id = photo[0]['id']
                        access_key = photo[0]['access_key']
                        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                        vk.messages.send(user_id=id,
                                         message=f'Найдено по запросу: {crds} \n'
                                                 f'Описание: {text}\n',
                                         attachment=attachment,
                                         random_id=random.randint(0, 2 ** 64))
                    else:
                        vk.messages.send(user_id=id,
                                         message=f'Ошибка',
                                         random_id=random.randint(0, 2 ** 64))
                    if sys_count == 0:
                        vk.messages.send(user_id=id,
                                         message=f'Вы можете повторить запрос в чате.  '
                                                 f'Чтобы выйти в меню"/main" \n',
                                         random_id=random.randint(0, 2 ** 64))
                        sys_count += 1
    except Exception:
        vk.messages.send(user_id=id,
                         message=f'Упс, ничего не нашлось...',
                         random_id=random.randint(0, 2 ** 64))

        map(vk, id, vk_session)


def metro(vk, id, vk_session):
    longpoll = VkLongPoll(vk_session)
    vk.messages.send(peer_id=id, random_id=0, message='Введите адрес:')
    sys_count = 0
    wikipedia.set_lang('ru')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                metro_msg = event.text
                if metro_msg == '/main':
                    help(vk, id)
                    return
                try:
                    req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
                          + str(find_coord(metro_msg)) + "&format=json&kind=metro"
                    response = requests.get(req)
                    if response:
                        json_response = response.json()
                        try:
                            metro1 = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                                "GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
                            if 'метро' in metro1[4]["name"]:
                                vk.messages.send(user_id=id,
                                                 message=f'{metro1[4]["name"]}',
                                                 random_id=random.randint(0, 2 ** 64))
                                print(metro1[4]["name"])
                                continue
                            if 'метро' in metro1[5]["name"]:
                                print(metro1[5]["name"])
                                vk.messages.send(user_id=id,
                                                 message=f'{metro1[5]["name"]}',
                                                 random_id=random.randint(0, 2 ** 64))
                                continue
                        except IndexError:
                            vk.messages.send(user_id=id,
                                             message=f'Упсс, ничего не найдено. Попробуйте снова.',
                                             random_id=random.randint(0, 2 ** 64))
                        if sys_count == 0:
                            vk.messages.send(user_id=id,
                                             message=f'Вы можете повторить запрос в чате.  '
                                                     f'Чтобы выйти в меню"/main" \n',
                                             random_id=random.randint(0, 2 ** 64))
                            sys_count += 1
                except Exception:
                    vk.messages.send(user_id=id,
                                     message=f'Ошибка...',
                                     random_id=random.randint(0, 2 ** 64))


def find_coord(n):
    req = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
          + str(n) + "&format=json"
    resp = requests.get(req)
    try:
        if resp:
            json_resp = resp.json()
            find_coord = json_resp["response"]["GeoObjectCollection"]["featureMember"][0][
                "GeoObject"]["boundedBy"]["Envelope"]["lowerCorner"]
            return find_coord
    except Exception:
        return None


if __name__ == '__main__':
    main()
