import json
import datetime
from flask import Flask, request
from api.db import list_tp_to_list_dict, get_conn_db
from api.utils import json_response

app = Flask(__name__)


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
                    REST-Full Flask API для записи в БД Postgres лог информаци от ВК-бота <br>
                    Используются следующие URL:
                </h2><br>
                    <h3><a href="https://db-for-logging-vkbot.herokuapp.com/api/logs/">/api/logs/</a>
                        - возвращает последние десять записей логов 
                    </h3><br>
                    <h3>/api/log/ methods 'POST' - добавляет в БД новую строку лога</h3><br>
                    <h3> <a href="https://github.com/kv2709/db-for-logging-vkbot.git" target="_blank"> 
                        Исходнки на GitHub </a>
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
            SELECT * FROM log
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
    Добавляет новую запись в БД, с содержанием,
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


# List of URL resource
# "/api/logs/"
# "/api/logs/", methods=['POST']
