from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo

lang = InlineKeyboardMarkup(row_width=3)

us_bttn = InlineKeyboardButton(text='🇺🇸', callback_data='btn_us')
uz_bttn = InlineKeyboardButton(text='🇺🇿', callback_data='btn_uz')
ru_bttn = InlineKeyboardButton(text='🇷🇺', callback_data='btn_ru')

ikb = InlineKeyboardMarkup(row_width=2)
post_button = InlineKeyboardButton(text="Post Vacancy",
                                   web_app=WebAppInfo(url='https://oneapp.ly/dashboard/jobs/create-vacancy'))
desc_button = InlineKeyboardButton(text="Instructions", url='https://telegra.ph/How-to-post-your-job-in-OneApp-06-08')
help_button = InlineKeyboardButton(text="Help", url='https://t.me/oneappsupport2')
back_button = InlineKeyboardButton(text="Back", callback_data='btn_back')
ikb.add(post_button, desc_button, help_button, back_button)

ru_ikb = InlineKeyboardMarkup(row_width=2)
post_button_ru = InlineKeyboardButton(text="Добавить Вакансию",
                                      web_app=WebAppInfo(url='https://oneapp.ly/ru/dashboard/jobs/create-vacancy'))
desc_button_ru = InlineKeyboardButton(text="Инструкции",
                                      url='https://telegra.ph/Kak-razmestit-svoyu-vakansiyu-v-OneApp-06-08')
help_button_ru = InlineKeyboardButton(text="Помощь", url='https://t.me/oneappsupport2')
back_button_ru = InlineKeyboardButton(text="Назад", callback_data='btn_back')
ru_ikb.add(post_button_ru, desc_button_ru, help_button_ru, back_button_ru)

uz_ikb = InlineKeyboardMarkup(row_width=2)
post_button_uz = InlineKeyboardButton(text="Vakansiya Joylash",
                                      web_app=WebAppInfo(url='https://oneapp.ly/uz/dashboard/jobs/create-vacancy'))
desc_button_uz = InlineKeyboardButton(text="Koʻrsatma",
                                      url='https://telegra.ph/Kak-razmestit-svoyu-vakansiyu-v-OneApp-06-08')
help_button_uz = InlineKeyboardButton(text="Yordam", url='https://t.me/oneappsupport2')
back_button_uz = InlineKeyboardButton(text="Qaytish", callback_data='btn_back')
uz_ikb.add(post_button_uz, desc_button_uz, help_button_uz, back_button_uz)

lang.add(us_bttn, uz_bttn, ru_bttn)
# ikb.add(login_button, signup_button)
