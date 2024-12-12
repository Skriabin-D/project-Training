import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message
from app.handlers import start, Reg, register, reg_exp, reg_age, reg_level, reg_goal, reg_type, reg_quantity, reg_zones
import app.keyboads as kb  # Замените на ваш правильный путь
from aiogram.types import ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import app.handlers as handlers


@pytest.mark.asyncio
async def test_start():
    # Положительный тест
    # Мокаем объект Message
    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = AsyncMock()  # Убеждаемся, что есть from_user
    mock_message.from_user.id = 12345  # Пример ID пользователя

    # Мокаем метод answer
    mock_message.answer = AsyncMock()

    # Вызов функции start
    await start(mock_message)

    # Проверяем, что метод answer вызван один раз с правильными аргументами
    mock_message.answer.assert_called_once_with(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )

    # Отрицательный тест
    # Задаем ошибку для метода answer
    mock_message.answer.side_effect = Exception("Ошибка при отправке сообщения")

    # Проверяем, что вызов функции start с этой ошибкой выбрасывает исключение
    with pytest.raises(Exception, match="Ошибка при отправке сообщения"):
        await start(mock_message)

    # Проверяем, что метод answer был вызван даже в случае ошибки
    mock_message.answer.assert_called()



@pytest.mark.asyncio
async def test_register():
    # Положительный тест
    # Мокаем объект Message
    mock_message = AsyncMock(spec=Message)
    mock_message.from_user = AsyncMock()  # Убеждаемся, что есть from_user
    mock_message.from_user.id = 12345  # Пример ID пользователя

    # Мокаем методы для message
    mock_message.answer = AsyncMock()

    # Мокаем FSMContext
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.set_state = AsyncMock()
    mock_state.update_data = AsyncMock()

    # Вызов функции register
    await register(mock_message, mock_state)

    # Проверяем, что message.answer был вызван с правильными параметрами
    mock_message.answer.assert_any_call(
        'Хорошо, давай начнем!',
        reply_markup=ReplyKeyboardRemove()  # Проверка, что клавиатура была удалена
    )

    mock_message.answer.assert_any_call(
        'Укажи свой возраст',
        reply_markup=kb.age_keyboard  # Проверка, что клавиатура с возрастом передана
    )

    # Проверяем, что set_state и update_data были вызваны с правильными параметрами
    mock_state.set_state.assert_any_call(Reg.tg_id)
    mock_state.set_state.assert_any_call(Reg.age)

    mock_state.update_data.assert_called_once_with(tg_id=mock_message.from_user.id)

    # Отрицательный тест
    # Мокаем ошибку при вызове set_state или update_data
    mock_state.set_state.side_effect = Exception("Ошибка при установке состояния")

    # Проверяем, что при ошибке будет выброшено исключение
    with pytest.raises(Exception):
        await register(mock_message, mock_state)

        # Проверяем, что методы set_state и update_data были вызваны
        mock_state.set_state.assert_any_call(Reg.tg_id)
        mock_state.set_state.assert_any_call(Reg.age)
        mock_state.update_data.assert_called_once_with(tg_id=mock_message.from_user.id)

        # Проверяем, что answer не был вызван после ошибки
        mock_message.answer.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("25", True, True, True),  # Положительный тест
    ]
)
async def test_reg_age(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_age(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(age=callback_data)
    else:
        state.update_data.assert_not_called()

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.experience)
    else:
        state.set_state.assert_not_called()

    # Проверяем, был ли вызов callback.message.edit_text
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
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_exp(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(experience=callback_data)

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.level)

    # Проверяем, был ли вызов callback.message.edit_text
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
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_level(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(level=callback_data)

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.goal)


    # Проверяем, был ли вызов callback.message.edit_text
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
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_goal(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(goal=callback_data)

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.type_tr)

    # Проверяем, был ли вызов callback.message.edit_text
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
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_type(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(type_tr=callback_data)

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.quantity)

    # Проверяем, был ли вызов callback.message.edit_text
    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Выберите количество тренировок в неделю', reply_markup=kb.quantity_keyboard
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback_data, expected_update_called, expected_state_called, expected_edit_text_called",
    [
        ("5", True, True, True),  # Положительный тест: данные передаются корректно

    ]
)
async def test_reg_quantity(callback_data, expected_update_called, expected_state_called, expected_edit_text_called):
    # Мокаем необходимые объекты
    callback = AsyncMock(spec=CallbackQuery)
    callback.data = callback_data  # Устанавливаем данные для теста

    # Мокаем объект message и добавляем его в callback
    callback.message = AsyncMock()
    callback.message.edit_text = AsyncMock()

    # Мокаем состояние
    state = AsyncMock(spec=FSMContext)
    state.update_data = AsyncMock()
    state.set_state = AsyncMock()

    # Вызов тестируемой функции
    await reg_quantity(callback, state)

    # Проверяем, был ли вызов state.update_data
    if expected_update_called:
        state.update_data.assert_called_once_with(quantity=callback_data)

    # Проверяем, был ли вызов state.set_state
    if expected_state_called:
        state.set_state.assert_called_once_with(Reg.zones)

    # Проверяем, был ли вызов callback.message.edit_text
    if expected_edit_text_called:
        callback.message.edit_text.assert_called_once_with(
            'Выберите зоны, на которых вы хотите сосредоточить внимание', reply_markup=kb.zones_keyboard
        )


@pytest.mark.asyncio
async def test_reg_zones():
    # Настраиваем mock для CallbackQuery
    mock_callback = AsyncMock(spec=CallbackQuery)
    mock_callback.data = "zone1"
    mock_callback.message = AsyncMock()
    mock_callback.message.edit_text = AsyncMock()
    mock_callback.message.answer = AsyncMock()

    # Настраиваем mock для FSMContext
    mock_state = AsyncMock(spec=FSMContext)
    mock_state.update_data = AsyncMock()
    mock_state.get_data = AsyncMock(return_value={
        "age": 25,
        "experience": "beginner",
        "level": "low",
        "goal": "fitness",
        "type_tr": "cardio",
        "quantity": 3,
        "zones": "zone1"
    })
    mock_state.set_state = AsyncMock()

    # Mock для generate (замените на настоящую реализацию, если нужно)
    async def mock_generate(age, experience, level, goal, type_tr, quantity, zones):
        if age == 25 and zones == "zone1":
            return "Программа тренировок готова"
        raise ValueError("Некорректные данные")

    # Заменяем реальную функцию generate на mock
    from app.handlers import generate
    original_generate = generate
    handlers.generate = mock_generate

    try:
        # Позитивный тест
        await reg_zones(mock_callback, mock_state)

        mock_state.update_data.assert_called_once_with(zones="zone1")
        mock_callback.message.edit_text.assert_awaited_once_with(
            "Секунду, программа тренировок составляется по заданным параметрам..."
        )
        mock_callback.message.answer.assert_awaited_with("Программа тренировок готова")
        mock_state.set_state.assert_called_once_with("Reg.abonement")

        # Негативный тест (некорректные данные)
        mock_state.get_data = AsyncMock(return_value={
            "age": 25,
            "experience": "beginner",
            "level": "low",
            "goal": "fitness",
            "type_tr": "cardio",
            "quantity": 3,
            "zones": "invalid_zone"
        })

        with pytest.raises(ValueError, match="Некорректные данные"):
            await reg_zones(mock_callback, mock_state)
    finally:
        # Возвращаем оригинальную функцию generate
        handlers.generate = original_generate
