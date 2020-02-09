from psycopg2 import connect


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
    db_name = 'd769313ahct159'
    user_name = 'abezsrfdejeaeh'
    host_name = 'ec2-184-72-235-159.compute-1.amazonaws.com'
    passwd = '156b579cde2a6797646c770fbaadb99cc9ddffe845a0befbeead8795a54fa65d'
    port_num = '5432'
    conn = connect(dbname=db_name, user=user_name, host=host_name, password=passwd, port=port_num)

    return conn


"""
Host
ec2-184-72-235-159.compute-1.amazonaws.com
Database
d769313ahct159
User
abezsrfdejeaeh
Port
5432
Password
156b579cde2a6797646c770fbaadb99cc9ddffe845a0befbeead8795a54fa65d
URI
postgres://abezsrfdejeaeh:156b579cde2a6797646c770fbaadb99cc9ddffe845a0befbeead8795a54fa65d@ec2-184-72-235-159.compute-1.amazonaws.com:5432/d769313ahct159
Heroku CLI
heroku pg:psql postgresql-elliptical-50522 --app db-for-logging-vkbot
"""
con = get_conn_db()
cur = con.cursor()

# cur.execute('''
#     CREATE SEQUENCE author_ids;
#     ''')
#
# cur.execute('''
#     CREATE TABLE author (
#     id INTEGER PRIMARY KEY DEFAULT NEXTVAL('author_ids'),
#     username TEXT UNIQUE NOT NULL,
#     password TEXT NOT NULL);
#     ''')
#
# cur.execute('''
#     CREATE SEQUENCE post_ids;
#     ''')
#
# cur.execute('''
#     CREATE TABLE post (
#      id INTEGER PRIMARY KEY DEFAULT NEXTVAL('post_ids'),
#      author_id INTEGER NOT NULL,
#      created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#      title TEXT NOT NULL,
#      body TEXT NOT NULL,
#      FOREIGN KEY (author_id) REFERENCES author (id));
#      ''')
#
#

# cur.execute('''
#     INSERT INTO author (username, password) VALUES ('Киреев Юрий','123456');
#     ''')
#
# cur.execute('''
#     INSERT INTO author (username, password) VALUES ('Киреев Толик','098765');
#     ''')


# cur.execute('''
#         INSERT INTO post (author_id, title, body)
#         VALUES (1, 'Первый пост неизвестного юзера', 'Сожержание  поста ');
#             ''')

# cur.execute('''
#     SELECT * FROM author;
#     ''')

# cur.execute('''
#         SELECT post.id, title, body, created, author_id, username
#         FROM post JOIN author ON post.author_id = author.id
#         ORDER BY created DESC;
#         ''')

# post_cur = cur.fetchall()
# print("Взяли список КОРТЕЖЕЙ в которых содержатся значения строк таблицы из курсора")
#
# print(post_cur)
# print("===================================")
#
# lst_bd = list_tp_to_list_dict(post_cur, cur)
# print("Сделали список словарей")
# print(lst_bd)
#
cur.close()
con.commit()
con.close()


