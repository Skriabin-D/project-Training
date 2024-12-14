'''
Файл, содержащий в себе все обработчики событий, заданных пользователем.
'''
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
    '''
    Класс состояний для регистрации пользователя в системе.
    '''
    tg_id = State()
    '''
    Телеграмм id пользователя
    '''
    age = State()
    '''
    Возраст пользователя
    '''
    experience = State()
    '''
    Опыт пользователя в зале
    '''
    level = State()
    '''
    Уровень  спортивной подготовки
    '''
    goal = State()
    '''
    Цель, которую пользователь хочет достичь при помощи тренировок в зале
    '''
    type_tr = State()
    '''
    Наиболее подходящий тип тренировок для пользователя
    '''
    quantity = State()
    '''
    Желаемое количество тренировок в зале в неделю
    '''
    zones = State()
    '''
    Зоны, на которые пользователь хочет сделать упор
    '''
    abonement = State()
    '''
    Согласен ли пользователь записаться
    '''
    time = State()
    '''
    Время, в течение которого будет действителен абонемент
    '''
@router.message(CommandStart())
async def start(message: Message):
    """
       Обрабатывает команду /start и приветствует пользователя.

       Args:
           message (Message): Объект сообщения, отправленного пользователем.

       UI Обновления:
           - Отправляет пользователю сообщение с приветствием и инструкциями.
           - Предлагает клавиатуру с кнопками для выбора дальнейших действий.

       Возвращаемое значение:
           Coroutine
       """
    await message.answer(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )

@router.message(Command('create'))
async def register(message: Message, state: FSMContext):
    '''
        Обрабатывает команду /create, инициирует процесс регистрации пользователя и
        переводит его в состояние age.

        Аргументы:
            message (Message): объект Message
            state (FSMContex): Текущее состояние FSMContext

        UI-обновления:
            - Отправляет сообщение с приветствием и удаляет текущую клавиатуру.
            - Отправляет новое сообщение с запросом возраста и клавиатурой с возрастными опциями.

        Возвращает:
            Coroutine
    '''
    await message.answer(
        'Хорошо, давай начнем!',
        reply_markup=ReplyKeyboardRemove()  # Удаляем клавиатуру
    )
    await state.set_state(Reg.tg_id)
    await state.update_data(tg_id=message.from_user.id)
    await state.set_state(Reg.age)
    await message.answer('Укажи свой возраст', reply_markup=kb.age_keyboard)

@router.callback_query(Reg.age)
async def reg_age(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает запрос обратного вызова для выбора возраста во время регистрации и переводит
        состояние в experience.

        Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

        UI обновления:
            - Удаляет предыдущее сообщение
            - Выводит клавиатуру с выбором опыта

        Возвращает:
            Coroutine
    '''
    await state.update_data(age=callback.data)
    await state.set_state(Reg.experience)
    await callback.message.edit_text('Укажи свой опыт тренировок', reply_markup=kb.experience_keyboard)

@router.callback_query(Reg.experience)
async def reg_exp(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает запрос обратного вызова для выбора опыта во время регистрации и переводит
        состояние в level.

        Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

        UI обновления:
            - Удаляет предыдущее сообщение
            - Выводит клавиатуру с выбором уровня

        Возвращает:
            Coroutine
    '''
    await state.update_data(experience=callback.data)
    await state.set_state(Reg.level)
    await callback.message.edit_text('Укажи свой уровень физической подготовки', reply_markup=kb.level_keyboard)

@router.callback_query(Reg.level)
async def reg_level(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает запрос обратного вызова для выбора уровня во время регистрации и переводит
        состояние в goal.

        Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

        UI обновления:
            - Удаляет предыдущее сообщение
            - Выводит клавиатуру с выбором цели

        Возвращает:
            Coroutine
    '''
    await state.update_data(level=callback.data)
    await state.set_state(Reg.goal)
    await callback.message.edit_text('Укажи свою цель', reply_markup=kb.goal_keyboard)

@router.callback_query(Reg.goal)
async def reg_goal(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает запрос обратного вызова для выбора цели во время регистрации и переводит
        состояние в type_tr.

        Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

        UI обновления:
            - Удаляет предыдущее сообщение
            - Выводит клавиатуру с выбором типа тренировок

        Возвращает:
            Coroutine
    '''
    await state.update_data(goal=callback.data)
    await state.set_state(Reg.type_tr)
    await callback.message.edit_text('Выберите тип тренировок', reply_markup=kb.type_keyboard)

@router.callback_query(Reg.type_tr)
async def reg_type(callback: CallbackQuery, state: FSMContext):
    '''
       Обрабатывает запрос обратного вызова для выбора типа тренировок во время регистрации и переводит
       состояние в quantity.

       Аргументы:
           callback (CallbackQuery): объект CallbackQuery
           state (FSMContex): Текущее состояние FSMContext

       UI обновления:
           - Удаляет предыдущее сообщение
           - Выводит клавиатуру с выбором количества тренировок в неделю

       Возвращает:
           Coroutine
    '''
    await state.update_data(type_tr=callback.data)
    await state.set_state(Reg.quantity)
    await callback.message.edit_text('Выберите количество тренировок в неделю', reply_markup=kb.quantity_keyboard)

@router.callback_query(Reg.quantity)
async def reg_quantity(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает запрос обратного вызова для выбора количества тренировок во время регистрации и переводит
        состояние в zones.

        Аргументы:
           callback (CallbackQuery): объект CallbackQuery
           state (FSMContex): Текущее состояние FSMContext

        UI обновления:
           - Удаляет предыдущее сообщение
           - Выводит клавиатуру с выбором зон, на которых пользователь хочет сосредоточить внимание

        Возвращает:
           Coroutine
    '''
    await state.update_data(quantity=callback.data)
    await state.set_state(Reg.zones)
    await callback.message.edit_text('Выберите зоны, на которых вы хотите сосредоточить внимание',
                                     reply_markup=kb.zones_keyboard)

@router.callback_query(Reg.zones)
async def reg_zones(callback: CallbackQuery, state: FSMContext):
    '''
      Обрабатывает запрос обратного вызова для зон, на которых пользователь хочет сосредоточить внимание во время регистрации и
      генерирует программу тренировок на основе введённых данных.

      Аргументы:
          callback (CallbackQuery): объект CallbackQuery
          state (FSMContex): Текущее состояние FSMContext

      UI обновления:
          - Удаляет предыдущее сообщение
          - Выводит пользователю информацию, что программа в процессе составления
          - Отправляет пользователю сгенерированную нейросетью программу тренировок
          - Отправляет сообщение с предложением записаться в зал и клавиатуру с множественным выбором

      Возвращает:
          Coroutine
    '''
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

@router.callback_query(Reg.abonement)
async def abonement(callback: CallbackQuery, state: FSMContext):
    '''
        Обрабатывает выбор абонемента, предоставляя соответствующие варианты действий в зависимости от состояния пользователя.

        Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

        Поведение:
            - Если пользователь выбрал "disagree":
                - Выводит сообщение о том, что пользователь отказался от абонемента.
                - Запрашивает, что ещё можно сделать для пользователя.
                - Очищает состояние.
            - Если пользователь выбрал "have already":
                - Проверяет информацию об абонементе пользователя.
                - Если абонемент действителен, выводит количество оставшихся дней.
                - Если абонемент истёк, предлагает оформить новый.
                - Если абонемента нет, предлагает оформить новый.
            - Если пользователь выбрал "agree":
                - Проверяет наличие активного абонемента.
                - Если абонемент есть, уведомляет об этом.
                - Если абонемента нет, предлагает выбрать срок нового абонемента.

        UI-обновления:
            - В зависимости от действий пользователя обновляет сообщения и предлагает соответствующие варианты действий.

        Возвращает:
            Coroutine
    '''
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

@router.callback_query(Reg.time)
async def time(callback: CallbackQuery, state: FSMContext):
    '''
    Обрабатывает выбор времени абонемента и завершает процесс записи пользователя.

    Аргументы:
            callback (CallbackQuery): объект CallbackQuery
            state (FSMContex): Текущее состояние FSMContext

    Действия:
        - Сохраняет информацию пользователя о времени окончания абонемента в базе данных через `rq.set_user`.
        - Получает информацию об окончании срока действия абонемента через `rq.get_info`.
        - Отправляет сообщение о подтверждении успешной записи.
        - Предлагает пользователю выбор дополнительных действий через клавиатуру.
        - Очищает состояние.

    UI-обновления:
        - Удаляет предыдущее сообщение
        - Отправляет новое сообщение с подтверждением успешной записи
        - Отправляет новое сообщение с побуждением к дополнительным действям и клавиатурой.

    Возвращает:
        Coroutine
    '''
    await state.update_data(time=callback.data)
    data = await state.get_data()
    await rq.set_user(tg_id=data["tg_id"], time=data["time"])
    end_date = await rq.get_info(data["tg_id"])
    await callback.message.edit_text(f'Отлично! Вы записаны, ваш абонемент действителен еще {end_date} дней')
    await callback.message.answer('Что-то еще?', reply_markup=kb.check_keyboard)
    await state.clear()

@router.message(F.text == 'Проверить, сколько времени осталось от абонемента')
async def check(message: Message, state: FSMContext):
    '''
    Функция для проверки оставшегося времени действия абонемента пользователя.

    Аргументы:
        message (Message): объект Message
        state (FSMContex): Текущее состояние FSMContext

    Действия:
        - Если абонемент ещё действителен:
            Отправляется сообщение с информацией о количестве оставшихся дней.
        - Если абонемент истёк:
            Пользователю предлагается записаться на новый абонемент, и его данные обновляются в базе данных, его состояние обновляется.
        - Если абонемент не существует:
            Пользователю предлагается записаться на новый абонемент, его состояние обновляется.

    UI-изменения:
        - Пользователю выводится сообщение, что производится проверка
        - Пользователю выводится сообщение о состоянии его абонемента
        - Если абонемент истек или отсутствует, пользователю выводится клавиатура с выбором, записаться в зал или нет

    Возвращает:
        Coroutine
    '''
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
