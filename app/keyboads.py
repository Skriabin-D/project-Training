from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton

check_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='/create')],
    [KeyboardButton(text='Проверить, сколько времени осталось от абонемента')]
    ],
    resize_keyboard=True
)

age_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='до 30 лет', callback_data='less than 30 years'),
    InlineKeyboardButton(text='30-40 лет', callback_data='30-40 years')],
    [InlineKeyboardButton(text='больше 40 лет', callback_data='more than 40 years')]
])

experience_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Никогда не занимался или занимался меньше 2-х месяцев',
                          callback_data='has never visited gym'),
    InlineKeyboardButton(text='От 2-х месяцев до года', callback_data='has been visiting gym for 2 months - 1 year')],
    [InlineKeyboardButton(text='Более года', callback_data='has been visiting gym for more than a year')]
])

level_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Не занимался спортом', callback_data='has never done sport'),
    InlineKeyboardButton(text='Занимался раньше', callback_data='used to do sports earlier')],
    [InlineKeyboardButton(text='Занимаюсь сейчас', callback_data='is doing sports now')]
])

goal_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Повышение силовых показателей', callback_data='to improve muscle strength'),
    InlineKeyboardButton(text='Набор мышечной массы', callback_data='to bulk_up')],
    [InlineKeyboardButton(text='Поддержание текущей формы', callback_data='to keep fit')]
])

type_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Силовые + кардио', callback_data='powerlifting and cardio'),
    InlineKeyboardButton(text='Силовые', callback_data='powerlifting')]
])

quantity_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='3', callback_data='3'), InlineKeyboardButton(text='2', callback_data='2')]
])

zones_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Фулл-бади', callback_data='full body'), InlineKeyboardButton(text='Ноги', callback_data='legs')],
    [InlineKeyboardButton(text='Руки', callback_data='arms'), InlineKeyboardButton(text='Грудь', callback_data='chest')],
    [InlineKeyboardButton(text='Спина', callback_data='back')]
])

abonement_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ДА🦾', callback_data='agree'), InlineKeyboardButton(text='НЕТ🤓', callback_data='disagree')],
    [InlineKeyboardButton(text='Я уже записан😎',callback_data='have already')]
])

smaller_abonement_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='ДА🦾', callback_data='agree'), InlineKeyboardButton(text='НЕТ🤓', callback_data='disagree')]
])

time_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='30 дней', callback_data='1'), InlineKeyboardButton(text='90 дней', callback_data='3')],
     [InlineKeyboardButton(text='Полгода', callback_data='-6'), InlineKeyboardButton(text='1 год', callback_data='12')]
])


