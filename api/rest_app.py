import json
import datetime
from flask import Flask, request
from api.db import list_tp_to_list_dict, tp_to_dict, get_conn_db
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
                    REST-Full Flask API записи в БД Postgres лог информаци от ВК-бота <br>
                    Используются следующие URL:</h2><br>
                    <h3>/api/post/ methods 'POST' - добавляет в БД новую строку лога</h3><br>
                   
                    <h3> <a href="https://github.com/kv2709/db_for_logging_vkbot.git" target="_blank"> Исходнки на GitHub </a></h3><br> 
                              
            </body> 
        </html>'''


@app.route("/api/posts/")
def get_posts():
    """
    :return: json со всеми записями.
    """
    conn = get_conn_db()
    cur = conn.cursor()

    cur.execute('''
            SELECT post.id, title, body, created, author_id, username
            FROM post JOIN author ON post.author_id = author.id
            ORDER BY created DESC;
            ''')

    post_cur = cur.fetchall()
    tp_bd = list_tp_to_list_dict(post_cur, cur)
    cur.close()
    conn.commit()
    conn.close()
    return json_response(json.dumps(tp_bd, default=convert_dt))


@app.route("/api/posts/", methods=['POST'])
def create_post():
    """
    Добавляет новый пост в БД, с содержанием, полученным в теле запроса
        title
        body
    :return: dictionary {"code_error": "Created_new_post"}
    """
    req = request.json
    title = req["title"]
    body = req["body"]
    author_id = req["author_id"]
    conn = get_conn_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO post (title, body, author_id)" " VALUES (%s, %s, %s)",
        (title, body, author_id),
    )
    cur.close()
    conn.commit()
    conn.close()

    return json_response(json.dumps({"code_error": "Created_new_post"}))


# List of URL resource
# "/api/posts/"

# "/api/posts/", methods=['POST']
