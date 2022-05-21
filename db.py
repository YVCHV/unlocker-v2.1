import sqlite3, datetime, time


def connect():
    conn = sqlite3.connect('stat.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def db():
    conn, cursor = connect()
    try:
        cursor.execute("create table users ('user_id' integer,'name' text,'date' text)")
        conn.commit()
    except:
        pass
    try:
        info_message = '⚠️ UNLOCKERBOT v2.1 BETA. Coded by DMYTRO YEVCHEV'
        func1_text = 'Управление цепочкой 1'
        func2_text = 'Управление цепочкой 2'
        cursor.execute("""create table config (bot_url text,info_message text,need_func1 integer,need_func2 integer, func1_text text, func2_text text)""")
        conn.commit()
        cursor.execute('insert into config values(0,?,1,0,?,?)',
                        (info_message, func1_text, func2_text,))
        conn.commit()
    except:
        pass
    try:
        cursor.execute("""create table adm_id (value integer)""")
        conn.commit()
        cursor.execute('create table ohr_id (value integer)')
        conn.commit()
        cursor.execute('create table channel_id (value text)')
        conn.commit()
        cursor.execute('create table func1 (value integer)')
        conn.commit()
        cursor.execute('create table func2 (value integer)')
        conn.commit()
    except:
        pass
    cursor.close()
    conn.close()


def set_funcs_value(type='need_func1'):
    conn, cursor = connect()
    if get_value(type) == 1:
        try:
            cursor.execute(f'update config set {type}=0')
            conn.commit()
        except Exception as e:
            print(e)
    else:
        try:
            cursor.execute(f'update config set {type}=1')
            conn.commit()
        except:
            pass
    cursor.close()
    conn.close()


def add_adm(id):
    conn, cursor = connect()
    cursor.execute('insert into adm_id values(?)', (id,))
    conn.commit()
    cursor.close()
    conn.close()


def remove_adm(id):
    conn, cursor = connect()
    try:
        cursor.execute('delete from adm_id where value=?', (id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def add_ohr(id):
    conn, cursor = connect()
    cursor.execute('insert into ohr_id values(?)', (id,))
    conn.commit()
    cursor.close()
    conn.close()


def remove_ohr(id):
    conn, cursor = connect()
    try:
        cursor.execute('delete from ohr_id where value=?', (id,))
        conn.commit()
    except Exception as e:
        print(e)
    cursor.close()
    conn.close()


def get_value(text, where="none", are="none", base='config'):
    conn, cursor = connect()
    try:
        if where == "none" and are == "none":
            message = cursor.execute(f'select {text} from {base}').fetchone()[0]
            return message
        elif where != 'none' and are != 'none':
            msg = cursor.execute(f'select {text} from {base} where {where}="{are}"').fetchone()[0]
            return msg
        else:
            m = cursor.execute(text).fetchone()[0]
            return m
    except:
        pass
    cursor.close()
    conn.close()


def get_valuedata(text):
    conn, cursor = connect()
    try:
        m = cursor.execute(text).fetchone()[0]
        return m
    except:
        pass
    cursor.close()
    conn.close()




def get_value_long(text):
    conn, cursor = connect()
    try:
        return cursor.execute(text).fetchone()[0]
    except:
        pass
    cursor.close()
    conn.close()


def get_values(text, where="none", are="none", base='config'):
    conn, cursor = connect()
    try:
        if where == "none" and are == "none":
            message = cursor.execute(f'select {text} from {base}').fetchall()
            return message
        elif where != 'none' and are != 'none':
            return cursor.execute(f'select {text} from {base} where {where}={are}').fetchall()
        else:
            pass
    except:
        pass
    cursor.close()
    conn.close()


def get_values_long(text):
    conn, cursor = connect()
    try:
        return cursor.execute(text).fetchall()
    except:
        pass
    cursor.close()
    conn.close()


def update_value(set, value):
    conn, cursor = connect()
    cursor.execute(f'update config set {set}="{value}"')
    conn.commit()
    cursor.close()
    conn.close()
