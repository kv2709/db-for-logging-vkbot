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


# con = get_conn_db()
# cur = con.cursor()

# cur.execute('''ALTER TABLE event RENAME TO log;''')
# cur.execute('''ALTER TABLE log ADD COLUMN level_name TEXT NOT NULL;''')
# cur.execute('''DROP TABLE error;''')
# cur.execute('''ALTER TABLE log RENAME COLUMN name_logger TO logger_name;''')
# cur.execute('''
#     INSERT INTO event (body) VALUES ('Тест insert');
#     ''')

# cur.execute('''
#         SELECT body
#         FROM event;
#         ''')

# cur.execute('''
#     CREATE SEQUENCE log_ids;
#     ''')
#
# cur.execute('''
#     CREATE TABLE log (
#      id INTEGER PRIMARY KEY DEFAULT NEXTVAL('log_ids'),
#      created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#      time_created TEXT NOT NULL,
#      logger_name TEXT NOT NULL,
#      level_name TEXT NOT NULL
#      file_name TEXT NOT NULL,
#      func_name TEXT NOT NULL,
#      line_number TEXT NOT NULL,
#      msg TEXT NOT NULL);
#      ''')

# post_cur = cur.fetchall()
# # print("Взяли список КОРТЕЖЕЙ в которых содержатся значения строк таблицы из курсора")
# print(post_cur)
# print("===================================")
# lst_bd = list_tp_to_list_dict(post_cur, cur)
# # print("Сделали список словарей")
# print(lst_bd)
#
# cur.close()
# con.commit()
# con.close()
"""
time_created, logger_name, level_name, file_name, func_name, line_number, msg
"""