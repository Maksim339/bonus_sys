#!/usr/bin/env python3
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import bot_tools
import os
from database import insert_value
import pathlib

try:
    class Test(StatesGroup):
        Q1 = State()
        Q2 = State()
        Q3 = State()
        Q4 = State()


    bot = Bot(token='1159723951:AAERSFZUMT5m-ngOCm6-aRb7rXzo7xDmqTE', parse_mode=types.ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    path = r'/home/maksim/PycharmProjects/bonus_sys/for_bonus/'
    print(path)


    @dp.message_handler(Command("start"), state=None)
    async def enter_test(message: types.Message):
        await bot.send_message(message.chat.id, 'Привет, готов?')
        await Test.Q1.set()


    @dp.message_handler(state=Test.Q1)
    async def answer_q1(message: types.Message, state: FSMContext):
        user_id = message.chat.id
        files = os.listdir(path)
        try:
            file = files[0]
            file_id = file.split('.jpg')[0]
            ops = bot_tools.check(user_id, file_id)
            if ops[0] == 'ok':
                del_mac()
                # file = open(path + ops[-1] + '.jpg', 'rb')
                with open(path + ops[-1] + '.jpg', 'rb') as file:
                    fi = ops[-1]
                    del_mac()
                    await bot.send_photo(user_id, file, caption='Что изображено на фото?')
                    async with state.proxy() as data:
                        data["file_id"] = fi
                bot_tools.insert_sql(user_id, ops[-1])
                bot_tools.remove_file(file_id)

                await Test.Q2.set()
            elif ops == 'finish':
                await bot.send_message(user_id, 'На сегодня фото закончились, попробуйте позже оптравить мне "/start"!')
                bot_tools.remove_file(file_id)

                await Test.Q1.set()
                # await state.finish()
        except:
            await bot.send_message(user_id, 'На сегодня фото закончились, попробуйте позже оптравить мне "/start"!')
            await Test.Q1.set()


    @dp.message_handler(state=Test.Q2)
    async def answer_q2(message: types.Message, state: FSMContext):
        answer = message.text
        user_id = message.chat.id
        async with state.proxy() as data:
            data["answer1"] = answer
            data["user_id"] = user_id

        try:
            insert_value(user_id=int(data.get('user_id')),
                                   file_id=str(data.get('file_id')),
                                   value=data.get('answer1'))  # Запись в БД формат user_id | file_id | value
        except:
            insert_value(user_id=int(data.get('user_id')),
                                   file_id=str(data.get('file_id')),
                                   value='invalid')
        answer1 = data.get('answer1')
        text = str(data.get('user_id')) + ':' + str(data.get('file_id')) + ':' + str(data.get('answer1') + '\n')
        with open('dataset.txt', 'a') as f:
            f.write(text)

        await message.answer("Вы уверены, что на изображении {}?".format(answer1), reply_markup=keyboard())
        await Test.Q3.set()


    @dp.callback_query_handler(state=Test.Q3)
    async def inlin(call: types.CallbackQuery, state: FSMContext):
        if call.data == 'yes':
            await bot.send_message(call.message.chat.id, 'Приступим к следующей фотографии?', reply_markup=keyboard2())
        elif call.data == 'no':
            await bot.send_message(call.message.chat.id, 'Введите значения заново!')
            await Test.Q4.set()
        elif call.data == 'yes2':
            # await Test.Q1.set()
            await answer_q1(message=call.message, state=state)
        elif call.data == 'no2':
            await bot.send_message(call.message.chat.id,
                                   'Спасибо за ответы!\nКак будешь готов - просто отправь мне "/start"')
            await state.finish()


    @dp.message_handler(state=Test.Q4)
    async def answer_q3(message: types.Message, state: FSMContext):
        await bot.send_message(message.chat.id, "Спасибо за ваши ответы!")
        await bot.send_message(message.chat.id, "Приступим к следующей фотографии?", reply_markup=keyboard2())
        answer = message.text
        async with state.proxy() as data:
            data["answer1"] = answer

        try:
            insert_value(user_id=int(data.get('user_id')),
                                   file_id=str(data.get('file_id')),
                                   value=data.get('answer1'))
        except:
            insert_value(user_id=int(data.get('user_id')),
                                   file_id=str(data.get('file_id')),
                                   value='invalid')
        await Test.Q3.set()


    def keyboard():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Да', callback_data='yes')
        button2 = types.InlineKeyboardButton(text='Нет', callback_data='no')
        markup.add(button1)
        markup.add(button2)
        return markup


    def keyboard2():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Да, поехали дальше!', callback_data='yes2')
        button2 = types.InlineKeyboardButton(text='Нет, оставим на потом...', callback_data='no2')
        # button3 = types.InlineKeyboardButton(text='Не корректное изображение', callback_data='no2')
        markup.add(button1)
        markup.add(button2)
        # markup.add(button3)
        return markup


    def del_mac():
        if os.path.exists(path + ".DS_Store"):
            os.remove(path + ".DS_Store")


    executor.start_polling(dp, skip_updates=True)
except Exception as e:
    l = [str(e)]
    f = open('text.txt', 'w')
    for index in l:
        f.write(index + '\n')
        f.close()

