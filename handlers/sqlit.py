import sqlite3
def reg_user(id,ref):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_list (
            name,
            number
            ) """)
    db.commit()

    sql.execute(""" CREATE TABLE IF NOT EXISTS user_time ( 
        id BIGINT,
        status_ref
        ) """)
    db.commit()
    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik (
            chanel,
            parametr,
            person
            ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel1','odnous_cinema',100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel2', 'odnous_cinema',100))
        sql.execute(f"INSERT INTO trafik VALUES (?,?,?)", ('channel3', 'Alitopprodaj',100))
        db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik_person(
                chanel,
                parametr,
                person
                ) """)
    db.commit()

    sql.execute(f"SELECT chanel FROM trafik_person WHERE chanel == 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik_person VALUES (?,?,?)", ('channel1',100,0))
        db.commit()


    sql.execute(""" CREATE TABLE IF NOT EXISTS trafik2 (
                chanel,
                parametr,
                person
                ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM trafik2 WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO trafik2 VALUES (?,?,?)", ('channel1', 'odnous_cinema', 100))
        sql.execute(f"INSERT INTO trafik2 VALUES (?,?,?)", ('channel2', 'odnous_cinema', 100))
        sql.execute(f"INSERT INTO trafik2 VALUES (?,?,?)", ('channel3', 'Alitopprodaj', 100))
        db.commit()


    sql.execute(f"SELECT id FROM user_time WHERE id ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO user_time VALUES (?,?)", (id, ref))
        db.commit()

    #Создание данных об админах
    sql.execute(""" CREATE TABLE IF NOT EXISTS admin_list (
                username,
                channel_onov,
                channel1,
                channel2,
                channel3,
                status
                ) """)
    db.commit()


    # Cоздание отслеживания подписчиков
    sql.execute(""" CREATE TABLE IF NOT EXISTS stata_parthers ( 
            id BIGINT,
            channel_ref
            ) """)
    db.commit()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{0}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (0,0))
        db.commit()


    # НАСТРОЙКА КАНАЛОВ ДЕНА
    sql.execute(""" CREATE TABLE IF NOT EXISTS channel_den(
                    chanel,
                    parametr,
                    person
                    ) """)
    db.commit()
    sql.execute(f"SELECT chanel FROM channel_den WHERE chanel = 'channel1'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_den VALUES (?,?,?)", ('channel1', 'chyornaya_vdova', 100))
        sql.execute(f"INSERT INTO channel_den VALUES (?,?,?)", ('channel2', 'hd_filmy7', 0))
        db.commit()


# ИНФО О ПАРТНЕРАХ ЧТО БЫ ПРИКРУТИТЬ ИМ СЧЕТЧИК
    sql.execute(""" CREATE TABLE IF NOT EXISTS parthers( 
                id_partn,
                name_channel,
                schet
                ) """)
    db.commit()

def cheach_channel_par(id): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers WHERE id_partn ={id}").fetchall()
    return r

def cheach_all_par(): #Возвращает 0 - если человек не работает с нами. имя его канала - если все хорошо
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    r = sql.execute(f"SELECT name_channel FROM parthers").fetchall()
    return r

def info(channel): #Возвращает количество подписок на канал
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = '{channel}'").fetchone()[0]
    return a


def reg_partners_schet(id,channel): #Регистрация партнера и его канала и отслеживание счетчика
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id_partn FROM parthers WHERE name_channel ='{channel}' and id_partn ='{id}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO parthers VALUES (?,?,?)", (id, channel, 0))
        db.commit()

def cheak_person_den():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    p = sql.execute(f"SELECT * FROM channel_den").fetchone()
    return p[2]

def cheak_channel_den(): # ВОЗВРАЩАЕТ 1 КАНАЛ ДЛЯ ЗАМЕНЯ
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    p = sql.execute(f"SELECT * FROM channel_den").fetchall()
    return p[1][1]

def cheak_channel_den2(): # ВОЗВРАЩАЕТ 2 КАНАЛА
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    p = sql.execute(f"SELECT * FROM channel_den").fetchall()
    return p[0][1],p[1][1]


###### Количество подписок на каналы партнеров
def reg_pod(id,channel):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT id FROM stata_parthers WHERE id ='{id}' and channel_ref ='{channel}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO stata_parthers VALUES (?,?)", (id, channel))
        db.commit()




#Просмотр трафика
def info_chyornaya_vdova(): # Трафик Дена
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'chyornaya_vdova'").fetchone()[0]
    b = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'hd_filmy7'").fetchone()[0]
    return a,b



#def info_filmyshd(): # Трафик Фаина
#    db = sqlite3.connect('server.db')
#    sql = db.cursor()
#    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'filmyshd'").fetchone()[0]
#    return a

def info_good_film1(): # Трафик Алексея
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'good_film1'").fetchone()[0]
    return a

def info_films_online_everyday(): # Трафик ЮЛИ
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT COUNT(*) FROM stata_parthers WHERE channel_ref = 'films_online_everyday'").fetchone()[0]
    return a


#### РАБОТА С %
def obnova_pers(p1,p2):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik_person SET parametr = '{p1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik_person SET person = '{p2}' WHERE chanel = 'channel1'")
    db.commit()

def obnova_pers_den(p1,p2):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE channel_den SET person = '{p1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE channel_den SET person = '{p1}' WHERE chanel = 'channel2'")
    db.commit()


def cheak_person():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    p = sql.execute(f"SELECT * FROM trafik_person").fetchone()
    p1 = p[1]
    p2 = p[2]
    return p1,p2


#####
def reg_admin(channel_osnov,username,status): #Регистрация админа
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"SELECT channel_onov FROM admin_list WHERE channel_onov ='{channel_osnov}' or username = '{username}'")
    if status != '9': #Одновление или добавление
        if sql.fetchone() is None: #Добавление
            sql.execute(f"INSERT INTO admin_list VALUES (?,?,?,?,?,?)", (username,channel_osnov,0,0,0,status))
            db.commit()
        else: #Обновление
            sql.execute(f"UPDATE admin_list SET status = {status} WHERE channel_onov ='{channel_osnov}' and username ='{username}'")
            db.commit()

    else: #Удаление
        sql.execute(f"DELETE FROM admin_list WHERE channel_onov ='{channel_osnov}' and username ='{username}'")
        db.commit()
    db.commit()


def proverka_admina(username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT username FROM admin_list WHERE username ='{username}'").fetchone()
    if a is None:
        return 0
    else:
        return 1


def proverka_channel_admin(username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT channel1,channel2,channel3 FROM admin_list WHERE username ='{username}'").fetchone()
    return a


def obnovatrafika_adminam(channel1,channel2,channel3,username): #3 lvl
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"UPDATE admin_list SET channel1= '{channel1}' WHERE username = '{username}'")
    sql.execute(f"UPDATE admin_list SET channel2= '{channel2}' WHERE username = '{username}'")
    sql.execute(f"UPDATE admin_list SET channel3= '{channel3}' WHERE username = '{username}'")
    db.commit()


def obnovatrafika_adminam2(channel2,channel3,username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"UPDATE admin_list SET channel2= '{channel2}' WHERE username = '{username}'")
    sql.execute(f"UPDATE admin_list SET channel3= '{channel3}' WHERE username = '{username}'")
    db.commit()


def obnovatrafika_adminam1(channel2,username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    sql.execute(f"UPDATE admin_list SET channel2= '{channel2}' WHERE username = '{username}'")

    db.commit()


def proverka_status_admina(username):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT status FROM admin_list WHERE username ='{username}'").fetchone()
    return a[0]


def info_members():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f'SELECT COUNT(*) FROM user_time').fetchone()[0]
    return a


def reg_one_channel(name): #Регистрация одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (name, 1))
        db.commit()
    db.commit()


def reg_channels(text): #Регистрация списка каналов
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    text = text.split()
    for i in text:
        i = i[1:]
        sql.execute(f"SELECT name FROM channel_list WHERE name ='{i}'")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO channel_list VALUES (?,?)", (i, 1))
            db.commit()
        db.commit()


def proverka_channel(channel_name):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    a = sql.execute(f"SELECT name FROM channel_list WHERE name ='{channel_name}'").fetchone()
    if a is None:
        return 0
    else:
        return 1


def del_one_channel(name): #Удаление одного канала
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    name = name[1:]
    sql.execute(f"SELECT name FROM channel_list WHERE name ='{name}'")
    if sql.fetchone() is None:
        pass
    else:
        sql.execute(f'DELETE FROM channel_list WHERE name ="{name}"')
        db.commit()


def cheak_traf():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik WHERE chanel = 'channel3'").fetchone()[0]
    list = [c1,c2,c3]
    return list


def cheak_traf2():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    c1 = sql.execute(f"SELECT parametr FROM trafik2 WHERE chanel = 'channel1'").fetchone()[0]
    c2 = sql.execute(f"SELECT parametr FROM trafik2 WHERE chanel = 'channel2'").fetchone()[0]
    c3 = sql.execute(f"SELECT parametr FROM trafik2 WHERE chanel = 'channel3'").fetchone()[0]
    list = [c1,c2,c3]
    return list


def obnovatrafika(channel1,channel2,channel3):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik SET parametr= '{channel1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel2}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik SET parametr= '{channel3}' WHERE chanel = 'channel3'")
    db.commit()


def obnovatrafika2(channel1,channel2,channel3):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE trafik2 SET parametr= '{channel1}' WHERE chanel = 'channel1'")
    sql.execute(f"UPDATE trafik2 SET parametr= '{channel2}' WHERE chanel = 'channel2'")
    sql.execute(f"UPDATE trafik2 SET parametr= '{channel3}' WHERE chanel = 'channel3'")
    db.commit()


def list_adminov():
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    a = sql.execute("SELECT * FROM admin_list").fetchall()
    k = sql.execute(f'SELECT COUNT(*) FROM admin_list').fetchone()[0]
    return a, k



def cheach_status_and_channel(channel_osnov):
    db = sqlite3.connect('server.db')
    sql = db.cursor()

    channel_osnov = '@'+channel_osnov


    try:
        a = (sql.execute(f"SELECT * FROM admin_list WHERE channel_onov ='{channel_osnov}'").fetchall())[0]
        status = a[5]
        cha1= a[2]
        cha2 = a[3]
        cha3 = a[4]

        return (status,cha1,cha2,cha3)

    except:
        return 616