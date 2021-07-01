from aiogram import types
from misc import dp, bot
import sqlite3
import asyncio

from .sqlit import info_chyornaya_vdova,info_good_film1,info_films_online_everyday,cheak_channel_den2,cheak_person_den,obnova_pers_den,cheach_channel_par,info

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

ADMIN_ID_1 = 494588959 #Cаня

PARTNERS1 = 430142587 #ДЕНИС
PARTNERS2 = 984418306 #Игорь
#ФАИН PARTNERS3 = 519072406
PARTNERS4 = 921818240 #Юля
PARTNERS5 = 1013231983 # АЛЕКС

class st_person_den(StatesGroup):
    st_1 = State()
    st_2 = State()


@dp.message_handler(commands=['info'],state='*')
async def cheak_traaf(message: types.Message):
    q  = cheach_channel_par(message.chat.id)
    if q != []: #Если зарегистрирован в базе для просмотра
        for i in q:
            s = (info(i[0]))
            await bot.send_message(message.chat.id, f'Счетчик @{i[0]}: {s}')



@dp.message_handler(commands=['traf'],state='*')
async def cheak_traaf(message: types.Message):
    if message.chat.id == PARTNERS1 or message.chat.id == PARTNERS2 or ADMIN_ID_1:  # ДЕНИС
        markup = types.InlineKeyboardMarkup()
        bat_setin0 = types.InlineKeyboardButton(text='Настройка % между 2 каналами',
                                                callback_data='settings_person_den')  # Настройка %
        markup.add(bat_setin0)

        a, b = info_chyornaya_vdova()  # Вызов функции из файла sqlit
        c1, c2 = cheak_channel_den2()

        p = int(cheak_person_den())
        await bot.send_message(message.chat.id, f'Счетчик @chyornaya_vdova: {a}\n'
                                                     f'Счетчик @hd_filmy7: {b}\n'
                                                     f'<b>Общий счетчик: {a + b}\n\n'
                                                f'⚙РАСПРЕДЕЛЕНИЯ ТРАФИКА:\n'
                                                f'@{c1}-@{c2}\n'
                                                f'{p}-{100-p} </b>', parse_mode='html',reply_markup=markup)


    if message.chat.id == PARTNERS5:  # АЛЕКС
        a = info_good_film1()  # Вызов функции из файла sqlit
        await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                f'Канал : @good_film1')

    if message.chat.id == PARTNERS4:  # ЮЛЯ
        a = info_films_online_everyday()  # Вызов функции из файла sqlit
        await bot.send_message(message.chat.id, f'Счетчик подписок: {a}\n'
                                                f'Канал : @films_online_everyday')




# НАСТРОЙКА ПРОЦЕНТОВ ДЕНИСУ
@dp.callback_query_handler(text='settings_person_den',state='*')
async def set_person_den(call: types.callback_query):
    markup_traf1 = types.InlineKeyboardMarkup()
    bat_b = types.InlineKeyboardButton(text='ОТМЕНА', callback_data='otemena')
    markup_traf1.add(bat_b)
    await bot.send_message(call.message.chat.id, text=f'Введи новое соотношение трафика через тире без пробелов!',reply_markup=markup_traf1)
    await st_person_den.st_1.set()




@dp.message_handler(state=st_person_den.st_1, content_types='text')
async def person_obnovlenie_den(message: types.Message, state: FSMContext):
    p = (message.text).split('-')
    try:
        p1 = int(p[0])
        p2 = int(p[1])
        if p1 + p2 == 100:
            obnova_pers_den(p1,p2)
            await state.finish()
            await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
            await bot.send_message(chat_id=message.chat.id,text='Успешно')
        else:
            await bot.send_message(message.chat.id,text='Сумма процентов должна быть равна 100, повторите попытку')

    except:
        await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        await bot.send_message(chat_id=message.chat.id,text='Ошибка попробуйте снова')
        await state.finish()