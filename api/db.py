# -*- coding: utf-8 -*-
import datetime

from psycopg2 import connect
from pony.orm import *


DB_NAME = 'd769313ahct159'
USER_NAME = 'abezsrfdejeaeh'
HOST_NAME = 'ec2-184-72-235-159.compute-1.amazonaws.com'
PASSWD = '156b579cde2a6797646c770fbaadb99cc9ddffe845a0befbeead8795a54fa65d'
PORT_NUM = '5432'


def tp_to_dict(fetch_cur_in, cursor_in):
    """ Преобразуем полученный из базы кортежей fetch_cur_in, взяв
        дескриптор куросра базы cursor_in в словарь, ключами которого
        являются имена полей, а значениями - значания полей базы
    """
    descr = cursor_in.description
    rec = fetch_cur_in
    d = {}
    enu = enumerate(descr)
    for idx, colum in enu:
        d[colum[0]] = rec[idx]
    return d


def list_tp_to_list_dict(fetch_cur_in, cursor_in, key="lst"):
    """ Преобразуем полученный из базы список кортежей или
        кортеж fetch_cur_in, взяв дескриптор куросра базы cursor_in
        в список словарей, ключами которого являются имена полей,
        а значениями - значания полей базы. Работает как для fetchall
        так и для fetchone
    """
    descr = cursor_in.description
    dict_lst = []
    cur_lst_in = []
    if type(fetch_cur_in) == tuple:
        cur_lst_in.append(fetch_cur_in)
    else:
        cur_lst_in = fetch_cur_in
    for rec in cur_lst_in:
        d = {}
        enu = enumerate(descr)
        for idxt, colum in enu:
            d[colum[0]] = rec[idxt]
        dict_lst.append(d)
    if key != "lst":
        dict_lst = tuple(dict_lst)

    return dict_lst


def get_conn_db():
    conn = connect(dbname=DB_NAME, user=USER_NAME, host=HOST_NAME, password=PASSWD, port=PORT_NUM)
    return conn


# -------------------------- Обработка сохранения userState через Pony ORM------------------------------------
db = Database()
db.bind(provider='postgres', user=USER_NAME, password=PASSWD,
        host=HOST_NAME, port=PORT_NUM, database=DB_NAME)


class UserState(db.Entity):
    """
    Состояние пользователя внутри сценария
    """
    user_id = Required(str, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class RegistrationUser(db.Entity):
    """
    Данные на зарегистрированого пользователя
    """
    created = Required(datetime)
    name = Required(str)
    email = Required(str)


db.generate_mapping(create_tables=True)
