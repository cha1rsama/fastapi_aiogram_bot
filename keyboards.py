from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto
from aiogram.types.web_app_info import WebAppInfo

lang = InlineKeyboardMarkup(row_width=2)

uz_bttn = InlineKeyboardButton(text='🇺🇿', callback_data='uz')
ru_bttn = InlineKeyboardButton(text='🇷🇺', callback_data='ru')
lang.add(uz_bttn, ru_bttn)

uz_ikb = InlineKeyboardMarkup(row_width=2)
post_button_uz = InlineKeyboardButton(text="Vakansiya Joylash",
                                      web_app=WebAppInfo(url='https://oneapp.ly/uz/dashboard/jobs/create-vacancy'))
desc_button_uz = InlineKeyboardButton(text="Koʻrsatma",
                                      url='https://telegra.ph/Kak-razmestit-svoyu-vakansiyu-v-OneApp-06-08')
help_button_uz = InlineKeyboardButton(text="Yordam", url='https://t.me/oneappsupport2')
back_button_uz = InlineKeyboardButton(text="Qaytish", callback_data='btn_back')
uz_ikb.add(post_button_uz, desc_button_uz, help_button_uz, back_button_uz)

signinmrkp = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
loginbtn = KeyboardButton(text='Войти', web_app=WebAppInfo(url='https://one-app-login.netlify.app'))
signupbtn = KeyboardButton(text='Зарегистрироваться',
                           web_app=WebAppInfo(url='https://oneapp.ly/ru/signup/organization'))
signinmrkp.add(loginbtn, signupbtn)


async def ru_btn(callback):
    await callback.message.edit_media(media=InputMediaPhoto(media="https://i.ibb.co/D8M0JY1/photo-2023-07-14-16-18-39.jpg"))
    await callback.message.edit_caption('Спасибо за выбор 🇷🇺\n'
                                        'Давайте разместим вашу вакансию 🧾\n'
                                        'Вам нужно будет всего лишь авторизоваться ниже🔐')
    await callback.message.answer(text='<em>Если вы не зарегистрированы пожалуйста нажмите на кнопку регистарции '
                                       'и потратьте 2-3 минуты на создание аккаунта и добавление нужной '
                                       'информации</em>', parse_mode='HTML', reply_markup=signinmrkp)


async def uz_btn(callback):
    await callback.message.edit_media(media=InputMediaPhoto(media="https://oneapp.ly/_next/static/media/howWorksEmp1.726b8e51.png"))
    await callback.message.edit_caption('Tanlaganiz uchun rahmat 🇺🇿\n'
                                        'Sizga yordam beraman, shu yerda o\'z Vakansiyangizni joylashingiz '
                                        'mumkin🧾\n'
                                        'Siz faqatgina pastdagi tugmasini bosishiz kerak🔽\n\n'
                                        '🤔Agar esa butunlay koʻrsatma bilan tanishmoqchi boʻlsangiz Koʻrsatma '
                                        'tugmasini bosing')
    await callback.message.edit_reply_markup(uz_ikb)
