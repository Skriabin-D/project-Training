import pytest
from unittest.mock import MagicMock
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.handlers import start  # Функция для тестирования
import app.keyboads as kb  # Для проверки клавиатуры


@pytest.mark.asyncio
async def test_start_positive():
    # Мокаем message и state
    message = MagicMock(Message)
    state = MagicMock(FSMContext)

    # Мокаем ответ от state.set_state
    state.set_state = MagicMock()

    # Мокаем метод answer
    message.answer = MagicMock()

    # Вызываем тестируемую функцию
    await start(message, state)

    # Проверяем, что set_state был вызван с нужным состоянием
    state.set_state.assert_called_once_with(Reg.tg_id)

    # Проверяем, что отправлено сообщение с правильным текстом и клавиатурой
    message.answer.assert_called_once_with(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )


@pytest.mark.asyncio
async def test_start_negative_state_error():
    # Мокаем message и state
    message = MagicMock(Message)
    state = MagicMock(FSMContext)

    # Мокаем ошибку при вызове set_state
    state.set_state = MagicMock(side_effect=Exception("Failed to set state"))

    # Мокаем метод answer
    message.answer = MagicMock()

    # Проверяем, что ошибка происходит при вызове set_state
    with pytest.raises(Exception, match="Failed to set state"):
        await start(message, state)

    # Убедимся, что message.answer не был вызван
    message.answer.assert_not_called()


@pytest.mark.asyncio
async def test_start_negative_message_error():
    # Мокаем message и state
    message = MagicMock(Message)
    state = MagicMock(FSMContext)

    # Мокаем успешное выполнение set_state
    state.set_state = MagicMock()

    # Мокаем ошибку при отправке сообщения
    message.answer = MagicMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что ошибка происходит при отправке сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await start(message, state)

    # Убедимся, что set_state был вызван
    state.set_state.assert_called_once_with(Reg.tg_id)
