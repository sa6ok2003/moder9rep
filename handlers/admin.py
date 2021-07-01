from aiogram import types
from misc import dp, bot
import sqlite3
from .sqlit import info_members, reg_one_channel, reg_channels,del_one_channel,cheak_traf,obnovatrafika,reg_admin,list_adminov,obnovatrafika2,cheak_traf2,cheak_person,obnova_pers,info_chyornaya_vdova,info_good_film1,info_films_online_everyday,reg_partners_schet,cheach_all_par,info
from .callbak_data import obnovlenie
import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


ADMIN_ID_1 = 494588959 #Cаня
ADMIN_ID_2 = 44520977 #Коля
ADMIN_ID_3 = 678623761 #Бекир
ADMIN_ID_4 = 941730379 #Джейсон


MODERN_ID_5 = 807911349 #Байзат


PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
#ФАИН PARTNERS3 = 519072406
PARTNERS4 = 921818240 #Юля
PARTNERS5 = 1013231983 # АЛЕКС

ADMIN_ID =[ADMIN_ID_1,ADMIN_ID_2,ADMIN_ID_3, ADMIN_ID_4]
MODERN = [MODERN_ID_5]

class reg(StatesGroup):
    name = State()
    fname = State()

class st_reg(StatesGroup):
    st_name = State()
    st_fname = State()
    step_q = State()
    step_regbutton = State()

class st_person(StatesGroup):
    st_1 = State()
    st_2 = State()

class del_user(StatesGroup):
    del_name = State()
    del_fname = State()

class reg_trafik(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_trafik2(StatesGroup):
    traf1 = State()
    traf2 = State()

class reg_admink(StatesGroup):
    adm1 = State()
    adm2 = State()

class partners12(StatesGroup):
    step1 = State()
    step2 = State()

@dp.message_handler(commands=['admin'])
async def admin_ka(message: types.Message):
    id = message.from_user.id
    if id in ADMIN_ID:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        bat_e = types.InlineKeyboardButton(text='Рассылка', callback_data='write_message')
        bat_j = types.InlineKeyboardButton(text='Скачать базу', callback_data='baza')
        bat_setin0 = types.InlineKeyboardButton(text='Настройка % между группами', callback_data='settings_person')
        bat_setin = types.InlineKeyboardButton(text='1 группа', callback_data='settings')
        bat_setin2 = types.InlineKeyboardButton(text='2 группа', callback_data='settings2')
        bat_modern = types.InlineKeyboardButton(text='Права администраторов', callback_data='but_adm')
        tup1 = types.InlineKeyboardButton(text='НАСТРОИТЬ ТИП 1', callback_data='t1')
        tup2 = types.InlineKeyboardButton(text='НАСТРОЙКА ТИП 2', callback_data='t2')
        den_but = types.InlineKeyboardButton(text='Ден', callback_data='chyornaya_vdova')
        alex_but = types.InlineKeyboardButton(text='Алекс', callback_data='good_film1')
        yulya_but = types.InlineKeyboardButton(text='Юля', callback_data='films_online_everyday')
        reg_new_partners = types.InlineKeyboardButton(text='РЕГИСТРАЦИЯ НОВОГО ПАРТНЕРА', callback_data='reg_new_partners')
        vienw_partners = types.InlineKeyboardButton(text='СТАТИСТИКА ВСЕХ ПАРТНЕРОВ',callback_data='vienw_partners')


        markup.add(bat_a,bat_e,bat_j)
        markup.add(den_but,alex_but,yulya_but) #Инфо о партнерах
        markup.add(bat_modern)
        markup.add(bat_setin0)
        markup.add(bat_setin)
        markup.add(bat_setin2)
        markup.add(tup1,tup2)
        markup.add(reg_new_partners)
        markup.add(vienw_partners)
        await bot.send_message(message.chat.id,'Выполнен вход в админ панель',reply_markup=markup)

    if id in MODERN:
        markup = types.InlineKeyboardMarkup()
        bat_a = types.InlineKeyboardButton(text='Трафик', callback_data='list_members')
        tup1 = types.InlineKeyboardButton(text='НАСТРОИТЬ ТИП 1', callback_data= 't1')
        tup2 = types.InlineKeyboardButton(text='НАСТРОЙКА ТИП 2', callback_data= 't2')
        markup.add(bat_a)
        #   markup.add   (tup1, tup2)   БЫСТРАЯ   НАСТРОЙКА   ТИПОВ
        await bot.send_message(message.chat.id, 'Выполнен вход в админ панель', reply_markup=markup)



#ПРОСМОТР ВСЕХ ПАРТНЕРОВ
@dp.callback_query_handler(text='vienw_partners')  #ПРОСМОТР ВСЕХ ПАРТНЕРОВ
async def vienw_partners(call: types.callback_query):
    q = cheach_all_par()
    if q != []:  # Если зарегистрирован в базе для просмотра
        for i in q:
            s = (info(i[0]))
            await bot.send_message(call.message.chat.id, f'Счетчик @{i[0]}: {s}')



#МЕНЮ НОВЫХ ПАРТНЕРОВ
@dp.callback_query_handler(text='reg_new_partners')  #МЕНЮ
async def check_all_partners(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(chat_id=call.message.chat.id,text = 'Перешлите сообщение от партнера',reply_markup=markup)
    await partners12.step1.set()


@dp.message_handler(state=partners12.step1, content_types='text')
async def get_id_partners(message: types.Message, state: FSMContext):
    try:
        id = message.forward_from.id
        await state.update_data(id_partners = id)
        await bot.send_message(chat_id=message.chat.id, text='ID получен! \n'
                                                             'Введите имя канала слитно без пробелов, через @')
        await partners12.step2.set()

    except:
        await bot.send_message(chat_id=message.chat.id, text='У партнера скрытый аккаунт!\n'
                                                             'Повторите попытку')


@dp.message_handler(state=partners12.step2, content_types='text')
async def get_channel_partners(message: types.Message, state: FSMContext):
    chennel = message.text
    if chennel[0] == '@':
        await bot.send_message(chat_id=message.chat.id, text='Канал зарегистрирован')
        text_id = (await state.get_data())['id_partners']
        reg_partners_schet(channel=chennel[1:],id = text_id)
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id, text='Повторите попытку')


#Трафик партнеров
@dp.callback_query_handler(text='chyornaya_vdova')  # ТРАФИК У ДЕНИСА
async def check_chyornaya_vdova(call: types.callback_query):
    a,b = info_chyornaya_vdova() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик @chyornaya_vdova: {a}\n'
                                                 f'Счетчик @hd_filmy7: {b}\n'
                                                 f'<b>Общий счетчик: {a+b}</b>',parse_mode='html')

@dp.callback_query_handler(text='good_film1')  # ТРАФИК У АЛЕКСА
async def good_film1(call: types.callback_query):
    a = info_good_film1() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик подписок: {a}\n'
                                                 f'Канал : @good_film1')

@dp.callback_query_handler(text='films_online_everyday')  # ТРАФИК У ЮЛИ
async def films_online_everyday(call: types.callback_query):
    a = info_films_online_everyday() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Счетчик подписок: {a}\n'
                                                 f'Канал : @films_online_everyday')



#Быстрая настройка
@dp.callback_query_handler(text='t1')
async def t1(call: types.callback_query): # Подтверждение настройки типа 1
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat_b = types.InlineKeyboardButton(text='Подтвердить', callback_data='set_1')
    markup.add(bat_b)
    markup.add(bat_a)
    await bot.send_message(chat_id=call.message.chat.id, text= '<b>Быстрая настройка тип 1</b>\n\n'
                                                               '<b>Описание:</b> Увеличить трафик в @nikolacinema',reply_markup=markup,parse_mode='html')

@dp.callback_query_handler(text='set_1')
async def set_1(call: types.callback_query): # Настройка типа 1 (Есть реклама)
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    obnova_pers(55, 45) #Обновление процентов
    obnovatrafika('nikolacinema','chyornaya_vdova','filmyshd') #Обнова первой группы (55%)
    obnovatrafika2('nikolacinema','filmyshd','chyornaya_vdova') #Обнова второй группы (45%)
    await bot.send_message(call.message.chat.id,text='Успешно')

@dp.callback_query_handler(text='t2')
async def t2(call: types.callback_query): # Подтверждение настройки типа 2
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat_b = types.InlineKeyboardButton(text='Подтвердить', callback_data='set_2')
    markup.add(bat_b)
    markup.add(bat_a)
    await bot.send_message(chat_id=call.message.chat.id, text= '<b>Быстрая настройка тип 2</b>\n\n'
                                                               '<b>Описание:</b> Уменьшить трафик в @nikolacinema',reply_markup=markup,parse_mode='html')

@dp.callback_query_handler(text='set_2')
async def set_2(call: types.callback_query): # Настройка типа 2 (Нет реклама)
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    obnova_pers(87, 13) #Обновление процентов
    obnovatrafika('filmyshd','nikolacinema','chyornaya_vdova') #Обнова первой группы (87%)
    obnovatrafika2('filmyshd','chyornaya_vdova','nikolacinema') #Обнова второй группы (13%)
    await bot.send_message(call.message.chat.id,text='Успешно')




# Урезанные админы
@dp.callback_query_handler(text='but_adm')
async def but_adm12(call: types.callback_query):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    markup = types.InlineKeyboardMarkup()
    bat_1 = types.InlineKeyboardButton(text='Список админов', callback_data='cheack_admin')
    bat_2 = types.InlineKeyboardButton(text='Изменить | Добавить ', callback_data='add_admin')
    bat_3 = types.InlineKeyboardButton(text='Выход', callback_data='c3')
    markup.add(bat_1,bat_2)
    markup.add(bat_3)

    await bot.send_message(chat_id=call.message.chat.id,text='Панель управления урезанной админкой',reply_markup=markup)

@dp.callback_query_handler(text='c3')
async def add_adm333(call: types.callback_query):
    await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)


@dp.callback_query_handler(text='cheack_admin')
async def add_adm335646453(call: types.callback_query):
    adm = list_adminov()
    kol = adm[1] # Количество админов
    arr = adm[0]

    massiv = []

    for i in arr:
        a,b,c,d,e,w = map(str,i)
        massiv.append(a + ' ' + b + ' ' + w)

    lis = ("\n\n".join(massiv))
    messa = (f"<b>Количество учеников: {kol}\n</b>"
               f"Пары <b>Юзер - Канал - Статус</b>:\n\n"
               f"{lis}")
    await bot.send_message(chat_id=call.message.chat.id,text=messa,parse_mode='html')


@dp.callback_query_handler(text='add_admin')
async def add_adm12(call: types.callback_query,state: FSMContext):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    q = await bot.send_message(call.message.chat.id, text='Что бы изменить права текущего админа или добавить нового, вводи :\n\n'
                                                      '@namechannel-@username-0\n'
                                                      '<b>Вводи без пробелов!\n\n'
                                                      '0 - Разрешено работать\n'
                                                      '1 - Разрешено менять 1 канал\n'
                                                      '2 - Разрешено менять 2 канала\n'
                                                      '3 - Разрешено менять 3 канала\n\n'
                                                      '9 - Удалить из админов</b>',parse_mode='html',reply_markup=markup)
    await state.update_data(mess1=q.message_id)
    await reg_admink.adm1.set()


@dp.message_handler(state=reg_admink.adm1, content_types='text')
async def adm_obnovlenie(message: types.Message, state: FSMContext):
    try:
        array = message.text.split('-')
        channel_osnov = array[0]
        username = array[1]
        status = array[2]

        if array[2] != '9': #Если не равно 9, то регистрируем в списке разрешенных
            reg_one_channel(array[0]) #Регистрация канала в списке
            reg_admin(channel_osnov,username,status)

        else:
            reg_admin(channel_osnov, username, status)
            del_one_channel(channel_osnov) # Удаление из разрешенных

        await bot.send_message(chat_id=message.chat.id,text='Успешно')
        data = await state.get_data()
        mess1 = data['mess1']
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=mess1)
        await state.finish()

    except:
        data = await state.get_data()
        mess1 = data['mess1']
        await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=mess1)
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()

### НАСТРОЙКА ТРАФИКА 1


# НАСТРОЙКА ПРОЦЕНТОВ
@dp.callback_query_handler(text='settings_person')
async def baza_person(call: types.callback_query):
    markup_traf1 = types.InlineKeyboardMarkup()
    bat_b = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup_traf1.add(bat_b)
    q = cheak_person()
    await bot.send_message(call.message.chat.id, text='Отношение процентов\n'
                                                      '1 группа / 2 группа\n\n'
                                                      f'{q[0]} - {q[1]}\n\n'
                                                      f'Введи новое соотношение трафика через тире без пробелов!',reply_markup=markup_traf1)
    await st_person.st_1.set()




@dp.message_handler(state=st_person.st_1, content_types='text')
async def person_obnovlenie(message: types.Message, state: FSMContext):
    p = (message.text).split('-')
    try:
        p1 = int(p[0])
        p2 = int(p[1])
        if p1 + p2 == 100:
            obnova_pers(p1,p2)
            await state.finish()
            await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id,text='Успешно')
        else:
            await bot.send_message(message.chat.id,text='Сумма процентов должна быть равна 100, повторите попытку')

    except:
        await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,text='Ошибка попробуйте снова')
        await state.finish()
#

@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 1 Группу⚙️', callback_data='change_trafik')
    bat_b = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup_traf.add(bat_a)
    markup_traf.add(bat_b)
    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов 1 группы на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]


        obnovatrafika(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()



@dp.callback_query_handler(text='settings')
async def baza12(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 1 Группу⚙️', callback_data='change_trafik')
    markup_traf.add(bat_a)
    list = cheak_traf()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов 1 группы на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik') # Изменение каналов, на которые нужно подписаться
async def baza12342(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik.traf1.set()


@dp.message_handler(state=reg_trafik.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        obnovatrafika(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()

#Настройка трафика 2
@dp.callback_query_handler(text='settings2')
async def baza122(call: types.callback_query):
    markup_traf = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ИЗМЕНИТЬ 2 Группу⚙️', callback_data='change_trafik2')
    bat_b = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup_traf.add(bat_a)
    markup_traf.add(bat_b)
    list = cheak_traf2()
    await bot.send_message(call.message.chat.id, text=f'Список активный каналов 1 группы на данный момент:\n\n'
                                                      f'1. @{list[0]}\n'
                                                      f'2. @{list[1]}\n'
                                                      f'3. @{list[2]}\n\n'
                                                      f'<b>Внимание! Первый по счету канал , должен быть обязательно с кино-тематикой</b>\n'
                                                      f'Для изменения жми кнопку',parse_mode='html',reply_markup=markup_traf)


@dp.callback_query_handler(text='change_trafik2') # Изменение каналов, на которые нужно подписаться
async def baza123422(call: types.callback_query):
    markup = types.InlineKeyboardMarkup()
    bat_a = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup.add(bat_a)

    await bot.send_message(call.message.chat.id, text='Введите новый список каналов\n<b>ПЕРВЫЙ КАНАЛ ДОЛЖЕН БЫТЬ ОБЯЗАТЕЛЬНО С КИНО-ТЕМАТИКОЙ!</b>\n\n'
                                                      'Список каналов вводи в строчку, пример:\n'
                                                      '@channel1 @channel2 @channel3',parse_mode='html',reply_markup=markup)
    await reg_trafik2.traf1.set()


@dp.message_handler(state=reg_trafik2.traf1, content_types='text')
async def traf_obnovlenie(message: types.Message, state: FSMContext):
    mas = message.text.split()
    if (len(mas) == 3 and mas[0][0] == '@' and mas[1][0] == '@' and mas[2][0] == '@'):
        # Список новых каналов
        channel1 = mas[0][1:]
        channel2 = mas[1][1:]
        channel3 = mas[2][1:]

        obnovatrafika2(channel1,channel2,channel3) # Внесение новых каналов в базу данных
        obnovlenie()
        await bot.send_message(chat_id=message.chat.id,text='Обновление успешно')
        await state.finish()

    else:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка! Вы сделали что-то неправильное. ТЕбе необходимо снова зайти в админ панель и выбрать нужный пункт.'
                                                            'Сообщение со списком каналом мне отсылать сейчас бессмыслено - я тебя буду игнорить, поэтому делай по новой все')
        await state.finish()
##############################################



@dp.callback_query_handler(text='baza')
async def baza(call: types.callback_query):
    a = open('server.db','rb')
    await bot.send_document(chat_id=call.message.chat.id, document=a)


############################  DELITE CHANNEL  ###################################
@dp.callback_query_handler(text='delite_channel')
async def del_channel(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название канала для удаления в формате\n'
                                                 '@name_channel')
    await del_user.del_name.set()


@dp.message_handler(state=del_user.del_name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        await state.finish()
        del_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Удаление завершено')


############################  REG ONE CHANNEL  ###################################
@dp.callback_query_handler(text='new_channel')  # АДМИН КНОПКА Добавления нового трафика
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь название нового канала в формате\n'
                                                 '@name_channel')
    await reg.name.set()


@dp.message_handler(state=reg.name, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    check_dog = message.text[:1]
    if check_dog != '@':
        await bot.send_message(message.chat.id, 'Ты неправильно ввел имя группы!\nПовтори попытку!')
    else:
        reg_one_channel(message.text)
        await bot.send_message(message.chat.id, 'Регистрация успешна')
        await state.finish()


################################    REG MANY CHANNELS    ###########################

@dp.callback_query_handler(text='new_channels')  # АДМИН КНОПКА Добавления новые телеграмм каналы
async def check(call: types.callback_query):
    await bot.send_message(call.message.chat.id, 'Отправь список каналов в формате\n'
                                                 '@name1 @name2 @name3 ')
    await reg.fname.set()


@dp.message_handler(state=reg.fname, content_types='text')
async def name_channel(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Каналы зарегистрированы')
    reg_channels(message.text)
    await state.finish()

#####################################################################################


@dp.callback_query_handler(text='list_members')  # АДМИН КНОПКА ТРАФИКА
async def check(call: types.callback_query):
    a = info_members() # Вызов функции из файла sqlit
    await bot.send_message(call.message.chat.id, f'Количество пользователей: {a}')


########################  Рассылка  ################################

@dp.callback_query_handler(text='write_message')  # АДМИН КНОПКА Рассылка пользователям
async def check(call: types.callback_query, state: FSMContext):
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    murkap.add(bat0)
    await bot.send_message(call.message.chat.id, 'Перешли мне уже готовый пост и я разошлю его всем юзерам',
                           reply_markup=murkap)
    await st_reg.step_q.set()


@dp.callback_query_handler(text='otemena',state='*')
async def otmena_12(call: types.callback_query, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Отменено')
    await state.finish()
    try:
        await bot.delete_message(call.message.chat.id,message_id=call.message.message_id)
    except: pass



@dp.message_handler(state=st_reg.step_q,content_types=['text','photo','video','video_note']) # Предосмотр поста
async def redarkt_post(message: types.Message, state: FSMContext):
    await st_reg.st_name.set()
    murkap = types.InlineKeyboardMarkup()
    bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
    bat2 = types.InlineKeyboardButton(text='Добавить кнопки', callback_data='add_but')
    murkap.add(bat1)
    murkap.add(bat2)
    murkap.add(bat0)

    await message.copy_to(chat_id=message.chat.id)
    q = message
    await state.update_data(q=q)

    await bot.send_message(chat_id=message.chat.id,text='Пост сейчас выглядит так 👆',reply_markup=murkap)



# НАСТРОЙКА КНОПОК
@dp.callback_query_handler(text='add_but',state=st_reg.st_name) # Добавление кнопок
async def addbutton(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
    await bot.send_message(call.message.chat.id,text='Отправляй мне кнопки по принципу Controller Bot\n\n'
                                                     'Пока можно добавить только одну кнопку')
    await st_reg.step_regbutton.set()


@dp.message_handler(state=st_reg.step_regbutton,content_types=['text']) # Текст кнопок в неформате
async def redarkt_button(message: types.Message, state: FSMContext):
    arr2 = message.text.split('-')

    k = -1  # Убираем пробелы из кнопок
    for i in arr2:
        k+=1
        if i[0] == ' ':
            if i[-1] == ' ':
                arr2[k] = (i[1:-1])
            else:
                arr2[k] = (i[1:])

        else:
            if i[-1] == ' ':

                arr2[0] = (i[:-1])
            else:
                pass

    # arr2 - Массив с данными


    try:
        murkap = types.InlineKeyboardMarkup() #Клавиатура с кнопками
        bat = types.InlineKeyboardButton(text= arr2[0], url=arr2[1])
        murkap.add(bat)

        data = await state.get_data()
        mess = data['q']  # ID сообщения для рассылки

        await bot.copy_message(chat_id=message.chat.id, from_chat_id=message.chat.id,message_id=mess.message_id,reply_markup=murkap)

        await state.update_data(text_but =arr2[0]) # Обновление Сета
        await state.update_data(url_but=arr2[1])  # Обновление Сета

        murkap2 = types.InlineKeyboardMarkup() # Клавиатура - меню
        bat0 = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
        bat1 = types.InlineKeyboardButton(text='РАЗОСЛАТЬ', callback_data='send_ras')
        murkap2.add(bat1)
        murkap2.add(bat0)

        await bot.send_message(chat_id=message.chat.id,text='Теперь твой пост выглядит так☝',reply_markup=murkap2)


    except:
        await bot.send_message(chat_id=message.chat.id,text='Ошибка. Отменено')
        await state.finish()


# КОНЕЦ НАСТРОЙКИ КНОПОК


@dp.callback_query_handler(text='send_ras',state="*") # Рассылка
async def fname_step(call: types.callback_query, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

    data = await state.get_data()
    mess = data['q'] # Сообщения для рассылки

    murkap = types.InlineKeyboardMarkup()  # Клавиатура с кнопками

    try: #Пытаемся добавить кнопки. Если их нету оставляем клаву пустой
        text_but = data['text_but']
        url_but = data['url_but']
        bat = types.InlineKeyboardButton(text=text_but, url=url_but)
        murkap.add(bat)
    except: pass


    db = sqlite3.connect('server.db')
    sql = db.cursor()
    await state.finish()
    users = sql.execute("SELECT id FROM user_time").fetchall()
    bad = 0
    good = 0
    await bot.send_message(call.message.chat.id, f"<b>Всего пользователей: <code>{len(users)}</code></b>\n\n<b>Расслыка начата!</b>",
                           parse_mode="html")
    for i in users:
        await asyncio.sleep(1)
        try:
            await mess.copy_to(i[0],reply_markup=murkap)
            good += 1
        except:
            bad += 1

    await bot.send_message(
        call.message.chat.id,
        "<u>Рассылка окончена\n\n</u>"
        f"<b>Всего пользователей:</b> <code>{len(users)}</code>\n"
        f"<b>Отправлено:</b> <code>{good}</code>\n"
        f"<b>Не удалось отправить:</b> <code>{bad}</code>",
        parse_mode="html"
    )
#########################################################