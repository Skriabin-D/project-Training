from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.ai import generate

import app.database.requests as rq
import app.keyboads as kb

router = Router()

class Reg(StatesGroup):
    tg_id = State()
    age = State()
    experience = State()
    level = State()
    goal = State()
    type_tr = State()
    quantity = State()
    zones = State()
    abonement = State()
    time = State()

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )

@router.message(Command('create'))
async def register(message: Message, state: FSMContext):
    await message.answer(
        'Хорошо, давай начнем!',
        reply_markup=ReplyKeyboardRemove()  # Удаляем клавиатуру
    )
    await state.set_state(Reg.tg_id)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(Reg.age)
    await message.answer('Укажи свой возраст', reply_markup=kb.age_keyboard)

@router.callback_query(Reg.age, F.data)
async def reg_age(callback: CallbackQuery, state: FSMContext):
    await state.update_data(age=callback.data)
    await state.set_state(Reg.experience)
    await callback.message.edit_text('Укажи свой опыт тренировок', reply_markup=kb.experience_keyboard)

@router.callback_query(Reg.experience, F.data)
async def reg_exp(callback: CallbackQuery, state: FSMContext):
    await state.update_data(experience=callback.data)
    await state.set_state(Reg.level)
    await callback.message.edit_text('Укажи свой уровень физической подготовки', reply_markup=kb.level_keyboard)

@router.callback_query(Reg.level, F.data)
async def reg_level(callback: CallbackQuery, state: FSMContext):
    await state.update_data(level=callback.data)
    await state.set_state(Reg.goal)
    await callback.message.edit_text('Укажи свою цель', reply_markup=kb.goal_keyboard)

@router.callback_query(Reg.goal, F.data)
async def reg_goal(callback: CallbackQuery, state: FSMContext):
    await state.update_data(goal=callback.data)
    await state.set_state(Reg.type_tr)
    await callback.message.edit_text('Выберите тип тренировок', reply_markup=kb.type_keyboard)

@router.callback_query(Reg.type_tr, F.data)
async def reg_type(callback: CallbackQuery, state: FSMContext):
    await state.update_data(type_tr=callback.data)
    await state.set_state(Reg.quantity)
    await callback.message.edit_text('Выберите количество тренировок в неделю', reply_markup=kb.quantity_keyboard)

@router.callback_query(Reg.quantity, F.data)
async def reg_quantity(callback: CallbackQuery, state: FSMContext):
    await state.update_data(quantity=callback.data)
    await state.set_state(Reg.zones)
    await callback.message.edit_text('Выберите зоны, на которых вы хотите сосредоточить внимание',
                                     reply_markup=kb.zones_keyboard)

@router.callback_query(Reg.zones, F.data)
async def reg_zones(callback: CallbackQuery, state: FSMContext):
    await state.update_data(zones=callback.data)
    data = await state.get_data()
    await callback.message.edit_text('Секунду, программа тренировок составляется по заданным параметрам...')
    ans = await generate(
        age=data["age"],
        experience=data["experience"],
        level=data["level"],
        goal=data["goal"],
        type_tr=data["type_tr"],
        quantity=data["quantity"],
        zones=data["zones"]
    )
    await callback.message.answer(ans)
    await state.set_state(Reg.abonement)
    await callback.message.answer('Желаете ли записаться в зал?', reply_markup=kb.abonement_keyboard)

@router.callback_query(Reg.abonement, F.data)
async def abonement(callback: CallbackQuery, state: FSMContext):
    await state.update_data(abonement=callback.data)
    data = await state.get_data()
    if data["abonement"] == "disagree":
        await callback.answer('')
        await callback.message.edit_text('Очень жаль(')
        await callback.message.answer('Что еще могу для вас сделать?', reply_markup=kb.check_keyboard)
        await state.clear()
    elif data["abonement"] == "have already":
        end_date = await rq.get_info(data["tg_id"])
        if end_date:
            if end_date > 0:
                await callback.message.edit_text(f'Отлично! Ваш абонемент действителен еще {end_date} дней!')
                await callback.message.answer('Что-то еще?', reply_markup=kb.check_keyboard)
                await state.clear()
            else:
                await rq.del_user(data["tg_id"])
                await callback.message.edit_text('К сожалению, ваш абонемент истек, желаете записаться?',
                                              reply_markup= kb.smaller_abonement_keyboard)
                await state.set_state(Reg.abonement)
        else:
            await callback.message.edit_text('К сожалению, вашего абонемента не существует, желаете записаться?',
                                             reply_markup= kb.smaller_abonement_keyboard)
            await state.set_state(Reg.abonement)
    elif data["abonement"] == "agree":
        await callback.answer('')
        end_date = await rq.get_info(data["tg_id"])
        if end_date and end_date > 0:
            await callback.message.edit_text('У вас уже есть абонемент')
            await callback.message.answer('Что-то еще?', reply_markup=kb.check_keyboard)
        else:
            await callback.message.edit_text('Отлично! Укажите, на какое время хотите взять абонемент.',
                                             reply_markup=kb.time_keyboard)
            await state.set_state(Reg.time)

@router.callback_query(Reg.time, F.data)
async def time(callback: CallbackQuery, state: FSMContext):
    await state.update_data(time=callback.data)
    data = await state.get_data()
    await rq.set_user(tg_id=data["tg_id"], time=data["time"])
    end_date = await rq.get_info(data["tg_id"])
    await callback.message.edit_text(f'Отлично! Вы записаны, ваш абонемент действителен еще {end_date} дней')
    await callback.message.answer('Что-то еще?', reply_markup=kb.check_keyboard)
    await state.clear()

@router.message(F.text == 'Проверить, сколько времени осталось от абонемента')
async def check(message: Message, state: FSMContext):
    end_date = await rq.get_info(message.from_user.id)
    if end_date:
        if end_date > 0:
            await message.answer(f'Ваш абонемент действителен еще {end_date} дней!', reply_markup=kb.check_keyboard)
        else:
            await rq.del_user(message.from_user.id)
            await message.answer('Проверяю....', reply_markup=ReplyKeyboardRemove())
            await message.answer('К сожалению, ваш абонемент истек, желаете записаться?',
                                 reply_markup=kb.smaller_abonement_keyboard)
            await state.set_state(Reg.tg_id)
            await state.update_data(tg_id=message.from_user.id)
            await state.set_state(Reg.abonement)
    else:
        await message.answer('Проверяю....', reply_markup=ReplyKeyboardRemove())
        await message.answer('К сожалению, вашего абонемента не существует, желаете записаться?',
                             reply_markup=kb.smaller_abonement_keyboard)
        await state.set_state(Reg.tg_id)
        await state.update_data(tg_id=message.from_user.id)
        await state.set_state(Reg.abonement)
