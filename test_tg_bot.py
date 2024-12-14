import pytest

from app.handlers import start, Reg, register, reg_exp, reg_age, reg_level, reg_goal, reg_type, reg_quantity, reg_zones

import app.keyboads as kb

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import app.database.requests as rq

from unittest.mock import create_autospec

from aiogram.types import Message, ReplyKeyboardRemove
from unittest.mock import AsyncMock, MagicMock

from app.handlers import check


@pytest.mark.asyncio
async def test_start_positive():
    """Тест успешного выполнения команды /start."""
    message = AsyncMock(spec=Message)
    message.answer = AsyncMock()
    await start(message)
    message.answer.assert_called_once_with(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )

@pytest.mark.asyncio
async def test_start_negative():
    """Тест неуспешного выполнения команды /start с отсутствующим сообщением."""
    with pytest.raises(AttributeError):
        await start(None)


@pytest.mark.asyncio
async def test_reg_age_positive():
    state = AsyncMock(spec=FSMContext)
    callback = AsyncMock(spec=CallbackQuery)

    callback.data = "25"
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    await reg_age(callback, state)

    state.update_data.assert_called_once_with(age=callback.data)

    state.set_state.assert_called_once_with(Reg.experience)

    callback.message.edit_text.assert_called_once_with('Укажи свой опыт тренировок', reply_markup=kb.experience_keyboard)


@pytest.mark.asyncio
async def test_reg_age_negative():
    state = AsyncMock(spec=FSMContext)
    callback = AsyncMock(spec=CallbackQuery)

    state.update_data = AsyncMock()
    state.set_state = AsyncMock()
    callback.data = AsyncMock()
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    with pytest.raises(AttributeError):
        await reg_age(None, state)

    state.update_data.assert_not_called()
    state.set_state.assert_not_called()
    callback.message.edit_text.assert_not_called()

@pytest.mark.asyncio
async def test_reg_zones_positive():
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.get_data = AsyncMock()
    state.set_state = AsyncMock()

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = AsyncMock()
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    await reg_zones(callback, state)
    state.update_data.assert_called_once()
    state.get_data.assert_called_once()

    callback.message.edit_text.assert_called_once_with(
        'Секунду, программа тренировок составляется по заданным параметрам...')
    callback.message.answer.assert_called()

    state.set_state.assert_called_once()

@pytest.mark.asyncio
async def test_reg_zones_negative():
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.get_data = AsyncMock()
    state.set_state = AsyncMock()

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = AsyncMock()
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()
    callback.message.answer = AsyncMock()

    with pytest.raises(AttributeError):
        await reg_zones(None, state)
    state.update_data.assert_not_called()
    state.get_data.assert_not_called()

    callback.message.edit_text.assert_not_called()
    callback.message.answer.assert_not_called()

    state.set_state.assert_not_called()



@pytest.mark.asyncio
async def test_check_positive_end_date():
    """Тестируем положительный сценарий, когда абонемент еще действителен."""

    message = create_autospec(Message)
    message.from_user = MagicMock()
    message.from_user.id = 12345
    message.answer = AsyncMock()

    state = AsyncMock()


    rq.get_info = AsyncMock(return_value=10)

    await check(message, state)


    message.answer.assert_called_once_with(
        'Ваш абонемент действителен еще 10 дней!', reply_markup=kb.check_keyboard
    )

    state.set_state.assert_not_called()
    state.update_data.assert_not_called()

@pytest.mark.asyncio
async def test_check_no_end_date():
    """Тестируем сценарий, когда абонемент отсутствует."""
    message = create_autospec(Message)
    message.from_user = MagicMock()
    message.from_user.id = 12345
    message.answer = AsyncMock()

    state = AsyncMock()


    rq.get_info = AsyncMock(return_value=None)


    await check(message, state)


    assert message.answer.call_count == 2
    message.answer.assert_any_call('Проверяю....', reply_markup=ReplyKeyboardRemove())
    message.answer.assert_any_call(
        'К сожалению, вашего абонемента не существует, желаете записаться?',
        reply_markup=kb.smaller_abonement_keyboard,
    )


    state.set_state.assert_called_with(Reg.abonement)
    state.update_data.assert_called_once_with(tg_id=12345)

@pytest.mark.asyncio
async def test_register():

    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = AsyncMock()
    mock_message.from_user.id = 12345


    mock_message.answer = AsyncMock()


    mock_state = AsyncMock(spec=FSMContext)
    mock_state.set_state = AsyncMock()
    mock_state.update_data = AsyncMock()


    await register(mock_message, mock_state)


    mock_message.answer.assert_any_call(
        'Хорошо, давай начнем!',
        reply_markup=ReplyKeyboardRemove()
    )

    mock_message.answer.assert_any_call(
        'Укажи свой возраст',
        reply_markup=kb.age_keyboard
    )


    mock_state.set_state.assert_any_call(Reg.tg_id)
    mock_state.set_state.assert_any_call(Reg.age)

    mock_state.update_data.assert_called_once_with(tg_id=mock_message.from_user.id)


    mock_state.set_state.side_effect = Exception("Ошибка при установке состояния")


    with pytest.raises(Exception):
        await register(mock_message, mock_state)


        mock_state.set_state.assert_any_call(Reg.tg_id)
        mock_state.set_state.assert_any_call(Reg.age)
        mock_state.update_data.assert_called_once_with(tg_id=mock_message.from_user.id)


        mock_message.answer.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("25", True, True, True),  # Положительный тест
    ]
)
async def test_reg_age(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data


    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()


    await reg_age(callback, state)


    if expected_update_called:
        state.update_data.assert_called_once_with(age=callback_data)
    else:
        state.update_data.assert_not_called()


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.experience)
    else:
        state.set_state.assert_not_called()


    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Укажи свой опыт тренировок', reply_markup=kb.experience_keyboard
        )
    else:
        callback.message.edit_text.assert_not_called()

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("Intermediate", True, True, True)
    ]
)
async def test_reg_exp(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data


    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()


    await reg_exp(callback, state)


    if expected_update_called:
        state.update_data.assert_called_once_with(experience=callback_data)


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.level)


    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Укажи свой уровень физической подготовки', reply_markup=kb.level_keyboard
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("Advanced", True, True, True)
    ]
)
async def test_reg_level(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data


    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()


    await reg_level(callback, state)


    if expected_update_called:
        state.update_data.assert_called_once_with(level=callback_data)


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.goal)



    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Укажи свою цель', reply_markup=kb.goal_keyboard
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("Weight Loss", True, True, True)
    ]
)
async def test_reg_goal(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data


    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    await reg_goal(callback, state)

    if expected_update_called:
        state.update_data.assert_called_once_with(goal=callback_data)


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.type_tr)

    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Выберите тип тренировок', reply_markup=kb.type_keyboard
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("3", True, True, True)
    ]
)
async def test_reg_type(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data


    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()


    await reg_type(callback, state)


    if expected_update_called:
        state.update_data.assert_called_once_with(type_tr=callback_data)


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.quantity)


    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Выберите количество тренировок в неделю', reply_markup=kb.quantity_keyboard
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("5", True, True, True),

    ]
)
async def test_reg_quantity(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):

    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()


    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()


    await reg_quantity(callback, state)


    if expected_update_called:
        state.update_data.assert_called_once_with(quantity=callback_data)


    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.zones)


    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Выберите зоны, на которых вы хотите сосредоточить внимание', reply_markup=kb.zones_keyboard
        )

@pytest.mark.asyncio
async def test_check_positive_end_date():
    """Тестируем положительный сценарий, когда абонемент еще действителен."""

    message = MagicMock(spec=Message)
    message.from_user = MagicMock()
    message.from_user.id = 12345
    message.answer = AsyncMock()

    state = AsyncMock()


    rq.get_info = AsyncMock(return_value=10)


    await check(message, state)


    message.answer.assert_called_once_with(
        'Ваш абонемент действителен еще 10 дней!', reply_markup=kb.check_keyboard
    )

    state.set_state.assert_not_called()
    state.update_data.assert_not_called()
