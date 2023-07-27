import json
import requests
from aiogram.utils import exceptions
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
from db import get_token, database
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
storage = MemoryStorage()


class Users(StatesGroup):
    unauthorized = State()
    authorized = State()
    vacancies = State()
    my_applicants = State()


async def vacancies(callback):

    global title
    try:
        del database[callback.from_user.id]
    except KeyError:
        pass
    await callback.answer(text='Грузим ваши вакансии ⏳...')
    user_get = await get_token(callback.message.chat.id)
    token = user_get['token']
    get_vacancies = requests.get(url='https://api.oneapp.ly/api/organizations/jobs',
                                 headers={'Authorization': f'Bearer {token}'}).content.decode('utf-8')
    parsed = json.loads(get_vacancies)
    jobs = []
    # this is for
    markup = InlineKeyboardMarkup()
    for index, item in enumerate(parsed['data']['jobs']):
        try:
            title = item['title']
            slug = item['slug']
        except (Exception,):
            await callback.message.edit_text('У вас еще нет опубликованных вакансий🥺, давайте разместим ее вместе,'
                                             '\nНажмие на "Разместить вакансию"',
                                             reply_markup=InlineKeyboardMarkup().
                                             add(InlineKeyboardButton('Назад', callback_data='btn_back')))
            break
        if item['status'] == 'archived':
            jobs.append(f'{title}:{slug}')
            markup.add(InlineKeyboardButton(text=f'{title} [ARCHIVED]', callback_data=f'${slug}'))
        elif item['status'] == 'deleted':
            pass
        else:
            jobs.append(f'{title}:{slug}')
            markup.add(InlineKeyboardButton(text=title, callback_data=f'${slug}'))
    markup.add(InlineKeyboardButton("Закрыть список", callback_data='btn_c'))
    await callback.message.answer(text='Список ваших вакансий :', reply_markup=markup)


text = []


async def main_page(token, message):
    ikb = InlineKeyboardMarkup(row_width=3)
    url = CREATE_VACANCY
    post_button = InlineKeyboardButton(text="Разместить вакансию",
                                       web_app=WebAppInfo(url=f'{url}{token}'))
    applicants_button = InlineKeyboardButton(text="Мои публикации", callback_data='btn_v')
    desc_button = InlineKeyboardButton(text="Инструкции",
                                       url='https://telegra.ph/Kak-razmestit-svoyu-vakansiyu-v-OneApp'
                                           '-06-08')
    help_button = InlineKeyboardButton(text="Помощь", url='https://t.me/oneappsupport2')
    back_button = InlineKeyboardButton(text="Сменить язык", callback_data='btn_lc')
    ikb.add(desc_button, help_button, back_button, post_button, applicants_button)
    await message.answer_photo(photo="https://i.ibb.co/xLz57JW/set.png",
                               caption='Пожалуйста выберите что будем делать дальше 🔽',
                               reply_markup=ikb)


async def applicants_get(callback, slug):
    global name, applicant_id, skills
    user_get = await get_token(callback.message.chat.id)
    token = user_get['token']
    url = requests.get(url=f'https://api.oneapp.ly/api/jobs/{slug[1:]}/applicants',
                       headers={'Authorization': f'Bearer {token}'}).content.decode('utf-8')
    parsed = json.loads(url)
    database.update({callback.from_user.id: []})
    message = []
    for index, item in enumerate(parsed['data']['apply']):
        try:
            name = item['applicant']['name']
            applicant_id = item['applicant']['_id']
            skills = []
            for num, i in enumerate(item['application']['skills']):
                skill = i['name']
                skills.append(skill)
            i = f'<a href="https://oneapp.ly/dashboard/job-applicants/' \
                f'{applicant_id}?token_bot={token}">{name}</a>,  skills: {str(skills).strip("[]")}\n\n'
            message.append(i)
        except (Exception,):
            message.append('error')
            pass
    return message


async def applicants_list(applicants, callback):
    slug = callback.data[1:]
    token = await get_token(callback.message.chat.id)
    url = f"https://oneapp.ly/dashboard/jobs/{slug}/applicants?token_bot={token['token']}"
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Обратно", callback_data="btn_b"),
        InlineKeyboardButton(text="Web View 📖",
                             web_app=WebAppInfo(
                                 url=url)),
        InlineKeyboardButton("Вперед", callback_data=f"next:0")
    )
    message = ""
    for applicant in applicants[slice(0, 10)]:
        message += applicant

    # for i in range(0, len(applicants) + 1, 10):
    #     text.append(applicants[slice(i, i + 10)])
    for i in range(0, len(applicants) + 1, 10):
        database[callback.from_user.id].append(applicants[slice(i, i + 10)])
    # ({f'{callback.from_user.id}': applicants[slice(i, i + 10)]})
    await callback.message.edit_text(text=message, parse_mode='HTML', disable_web_page_preview=True,
                                     reply_markup=markup)


async def next_page(callback):
    data = int(callback.data.split(":")[1]) + 1
    next_text = ""
    try:
        applicants = database[callback.from_user.id]
        if data >= len(applicants):
            await to_init_page(0, callback, applicants)

        else:
            for applicant in applicants[slice(data, data + 1)]:
                for i in applicant:
                    next_text += i
            markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton("Назад", callback_data=f"prev:{data}"),
                InlineKeyboardButton('Закрыть', callback_data="btn_c"),
                InlineKeyboardButton("Вперед", callback_data=f"next:{data}"),
            )
            await callback.message.edit_text(next_text, reply_markup=markup,
                                             parse_mode='HTML', disable_web_page_preview=True)
    except (exceptions.MessageTextIsEmpty, KeyError):
        await callback.answer(text='Сессия была прекращена, начинаем новую ⏳...')
        await callback.message.delete()
        await vacancies(callback)


async def return_page(data, callback, applicants):
    prev_text = ""
    for applicant in applicants[slice(data, data + 1)]:
        for i in applicant:
            prev_text += i
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Назад", callback_data=f"prev:{data}"),
        InlineKeyboardButton('Закрыть', callback_data="btn_c"),
        InlineKeyboardButton("Вперед", callback_data=f"next:{data}"),
    )
    await callback.message.edit_text(prev_text, reply_markup=markup,
                                     parse_mode='HTML', disable_web_page_preview=True)


async def to_init_page(data, callback, applicants):
    prev_text = ""
    for applicant in applicants[slice(data, data + 1)]:
        for i in applicant:
            prev_text += i
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Назад", callback_data=f"prev:{data}"),
        InlineKeyboardButton('Закрыть', callback_data="btn_c"),
        InlineKeyboardButton("Вперед", callback_data=f"next:{data}"),
    )
    await callback.message.edit_text(prev_text, reply_markup=markup,
                                     parse_mode='HTML', disable_web_page_preview=True)


async def prev_page(callback):
    data = int(callback.data.split(":")[1]) - 1
    try:
        applicants = database[callback.from_user.id]
        if data <= -1:
            length = len(applicants) - 1
            await return_page(length, callback, database[callback.from_user.id])
        elif data >= 0:
            next_text = ""
            for applicant in applicants[slice(data, data + 1)]:
                for i in applicant:
                    next_text += i
            markup = InlineKeyboardMarkup().add(
                InlineKeyboardButton("Назад", callback_data=f"prev:{data}"),
                InlineKeyboardButton('Закрыть', callback_data="btn_c"),
                InlineKeyboardButton("Вперед", callback_data=f"next:{data}"),
            )
            await callback.message.edit_text(next_text, reply_markup=markup,
                                             parse_mode='HTML', disable_web_page_preview=True)
    except (exceptions.MessageTextIsEmpty, KeyError):
        await callback.answer(text='Сессия была прекращена, начинаем новую ⏳...')
        await callback.message.delete()
        await vacancies(callback)
