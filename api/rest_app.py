# -*- coding: utf-8 -*-
import json
import datetime
from flask import Flask, request
from api.db import *
from pony.orm import *
from api.utils import json_response

app = Flask(__name__)
# TODO заменить интерпретатор pyyhon на 3.8.5
# обновление


def convert_dt(o):
    """
    Выдает строковое представление даты из типа datetime.datetime
    :param o:
    :return: строка с датой
    """
    if isinstance(o, datetime.datetime):
        return o.__str__()


@app.route('/')
def index_page():
    title_dic = {"title_text": "REST-Full API для записи в БД лог информаци от ВК-бота"}
    return '''
        <html>
            <head>
                <title>''' + title_dic["title_text"] + '''</title>
            <style>
               #cmd {
                    font-family: 'Times New Roman', Times, serif; 
                    font-size: 110%;
                    font-style: italic; 
                    color: navy;
               }
            </style>

            </head>
            <body>
                <h2>
                    REST-Full Flask API для записи в БД Postgres лог информаци от ВК-Бота <br>
                    Используются следующие URL:
                </h2><br>
                    <h3><a href="https://db-for-logging-vkbot.herokuapp.com/api/logs/">/api/logs/</a>, 
                        methods=['GET'] - возвращает последние десять записей логов Бота
                    </h3>
                    <h3>/api/log/, methods=['POST'] - добавляет в таблицу log новую строку лога
                    </h3>
                    <h3><a href="https://db-for-logging-vkbot.herokuapp.com/api/user_state/">/api/user_state/</a>, 
                        methods=['GET'] - возвращает из таблицы userstate записи состояний пользователей Бота, 
                        если они есть 
                    </h3>
                    <h3>/api/user_state/&lt;user_id&gt;, methods=['GET'] - возвращает запись user_state из таблицы 
                        userstate для запрашиваемого user_id
                    </h3>
                    <h3>/api/user_state/&lt;user_id&gt;, methods=['PUT'] - записывает в таблицу userstate измененный 
                        user_state для указанного user_id
                    </h3>
                    <h3>/api/user_state/&lt;user_id&gt;, methods=['DELETE'] - удаляет из таблицы userstate запись user_state 
                        для указанного user_id
                    </h3>
                    <h3>/api/user_registration/, methods=['POST'] - добавляет новую запись о зарегистрированном 
                        пользователе в таблицу registrationuser
                    </h3>
                    <h3><a href="https://db-for-logging-vkbot.herokuapp.com/api/user_registration/">
                        /api/user_registration/</a>, methods=['GET'] - возвращает из таблицы registrationuser записи 
                        последних десяти зарегистрированных на конференцию пользователей  
                    </h3><br>
                    
                    <h3> <a href="https://github.com/kv2709/db-for-logging-vkbot.git" target="_blank"> 
                        Исходнки API на GitHub </a>
                    </h3><br> 
                    <h3> <a href="https://github.com/kv2709/vk-bot.git" target="_blank"> 
                        Исходнки Бота на GitHub </a>
                    </h3><br> 
            </body> 
        </html>'''


@app.route("/api/logs/")
def get_logs():
    """
    :return: json с десятью последними записями.
    """
    conn = get_conn_db()
    cur = conn.cursor()

    cur.execute('''
            SELECT time_created, logger_name, level_name, file_name, func_name, line_number, msg FROM log
            ORDER BY created DESC
            LIMIT 10;
            ''')

    post_cur = cur.fetchall()
    tp_bd = list_tp_to_list_dict(post_cur, cur)
    cur.close()
    conn.commit()
    conn.close()
    return json_response(json.dumps(tp_bd, default=convert_dt))


@app.route("/api/log/", methods=['POST'])
def create_log_record():
    """
    Добавляет новую запись лога в таблицу log, с содержанием,
    полученным в теле запроса
    :return: dictionary {"code_error": "Created_new_log_record"}
    """
    req = request.json
    time_created = req["time_created"]
    logger_name = req["logger_name"]
    level_name = req["level_name"]
    file_name = req["file_name"]
    func_name = req["func_name"]
    line_number = req["line_number"]
    msg = req["msg"]
    conn = get_conn_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO log (time_created, logger_name, level_name, file_name, func_name, line_number, msg)"
        " VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (time_created, logger_name, level_name, file_name, func_name, line_number, msg),
    )
    cur.close()
    conn.commit()
    conn.close()

    return json_response(json.dumps({"code_error": "Created_new_log_record"}))


# =============================== PonyORM for user_sate ===================================
@db_session
@app.route("/api/user_state/", methods=['POST'])
def create_user_state_record():
    """
    Добавляет новую запись user_state в таблицу userstate, с содержанием,
    полученным в теле запроса
    :return: Словарь {"response": Created new user_state record for user_id {user_id}"}
    """
    req = request.json
    user_id = req["user_id"]
    scenario_name = req["scenario_name"]
    step_name = req["step_name"]
    context = req["context"]

    with db_session:
        user_state = UserState.get(user_id=user_id)
        if user_state is None:
            us_st = UserState(user_id=user_id,
                              scenario_name=scenario_name,
                              step_name=step_name,
                              context=context)
            response = f"Created new user_state record for user_id {user_id}"
        else:
            response = f"Record for user_id {user_id} already exist"
    return json_response(json.dumps({"response": response}))


@db_session
@app.route("/api/user_state/")
def all_user_state_records():
    """
    Отдает все записи user_state из таблицы userstate
    :return: Словарь {"response": "Records not found"}
             в случае ошибки или список словарей со всеми записями
    """

    with db_session:
        user_state_rec = select((item.user_id,
                                 item.scenario_name,
                                 item.step_name,
                                 item.context) for item in UserState)
        if user_state_rec is not None:
            response_list = []
            for item in user_state_rec:
                dict_for_response = {"user_id": item[0],
                                     "scenario_name": item[1],
                                     "step_name": item[2],
                                     "context": item[3]
                                     }
                response_list.append(dict_for_response)
        else:
            response_list = {"response": "Records not found"}
    return json_response(json.dumps(response_list))


@db_session
@app.route("/api/user_state/<user_id>")
def user_state_record(user_id):
    """
    Отдает запись user_state для запрашиваемого user_id из таблицы userstate
    :return: Словарь {"response": "Record for {user_id} not found"}
             в случае ошибки или словарь с найденной записью
    """

    with db_session:
        user_state_rec = select((item.user_id,
                                 item.scenario_name,
                                 item.step_name,
                                 item.context) for item in UserState if item.user_id == user_id).first()
    if user_state_rec is not None:
        dict_for_response = {"user_id": user_state_rec[0],
                             "scenario_name": user_state_rec[1],
                             "step_name": user_state_rec[2],
                             "context": user_state_rec[3]
                             }
    else:
        dict_for_response = {"response": f"Record for {user_id} not found"}
    return json_response(json.dumps(dict_for_response))


@db_session
@app.route("/api/user_state/<user_id>", methods=['PUT'])
def update_user_state(user_id):
    """
    Записывает в БД измененный  user_state for user_id
    :param user_id:
    :return: Словарь {"response": "Record for user_id {user_id} updated"}
    """

    req = request.get_json()
    user_id = req["user_id"]
    scenario_name = req["scenario_name"]
    step_name = req["step_name"]
    context = req["context"]

    with db_session:
        user_state = UserState.get(user_id=user_id)
        if user_state is not None:
            user_state.set(scenario_name=scenario_name,
                           step_name=step_name,
                           context=context)
            response = f"Record for user_id {user_id} updated"
        else:
            response = f"Record for user_id {user_id} not found"
    return json_response(json.dumps({"response": response}))


@db_session
@app.route("/api/user_state/<user_id>", methods=['DELETE'])
def delete_user_state(user_id):
    """
    Удаляет из БД  user_state for user_id
    :param user_id:
    :return: Словарь {"response": "Record for user_id {user_id} deleted"}
    """

    with db_session:
        user_state = UserState.get(user_id=user_id)
        if user_state is not None:
            user_state.delete()
            response = f"Record for user_id {user_id} deleted"
        else:
            response = f"Record for user_id {user_id} not found"

    return json_response(json.dumps({"response": response}))


@db_session
@app.route("/api/user_registration/", methods=['POST'])
def create_user_registration_record():
    """
    Добавляет новую запись о зарегистрированном пользователе в таблицу RegistrationUser,
    с содержанием, полученным в теле запроса (name, email)
    :return: Словрь {"response": "Created new registration record for {name} with email:{email}"}
    """
    req = request.json
    name = req["name"]
    email = req["email"]

    with db_session:
        user_registration = RegistrationUser.get(name=name, email=email)
        if user_registration is None:
            us_rg = RegistrationUser(name=name, email=email)
            response = f"Created new registration record for {name} with email:{email}"
        else:
            response = f"Record for user_id {name} with email:{email} already exist"
    return json_response(json.dumps({"response": response}))


@db_session
@app.route("/api/user_registration/")
def all_user_registration_records():
    """
    Отдает 10 записей о зарегистрированных пользователях из таблицы RegistrationUser,
    :return: Список словрей [{"created": datetime, "user_name": name, "user_email": email}] или
                            {"response": "Records not found"}
    """
    with db_session:
        user_reg_rec = select(item for item in RegistrationUser).order_by(lambda item: desc(item.created))[:10]

        if user_reg_rec is not None:
            response_list = []
            for item in user_reg_rec:
                time_created = str(item.created)
                dict_for_response = {"created": time_created,
                                     "user_name": item.name,
                                     "user_email": item.email
                                     }
                response_list.append(dict_for_response)
        else:
            response_list = {"response": "Records not found"}
    return json_response(json.dumps(response_list))

# List of URL resource
# "/api/logs/" methods=['GET']
# "/api/log/", methods=['POST']
# "/api/user_state/", methods=['POST']
# "/api/user_state/<user_id>", methods=['GET']
# "/api/user_state/<user_id>", methods=['PUT']
# "/api/user_state/<user_id>", methods=['DELETE']
# "/api/user_registration/", methods=['POST']
# "/api/user_registration/", methods=['GET']
