import pytest
from app.handlers import start, register, Reg # Импортируем тестируемую функцию
from app.handlers import reg_age  # Импортируем тестируемую функцию
from aiogram.types import CallbackQuery, User
from app.handlers import reg_exp  # Импортируем тестируемую функцию
from app.handlers import reg_level  # Импортируем тестируемую функцию
from app.handlers import reg_goal  # Импортируем тестируемую функцию
from app.handlers import reg_type  # Импортируем тестируемую функцию
import app.keyboads as kb  # Для проверки клавиатуры
from app.handlers import reg_quantity  # Импортируем тестируемую функцию
from app.handlers import abonement
from app.keyboads import time_keyboard  # Клавиатура для проверки
from app.handlers import reg_zones  # Импортируем функцию, которую тестируем
from app.keyboads import abonement_keyboard  # Импортируем клавиатуру для проверки
from aiogram.fsm.context import FSMContext
from app.handlers import time  # Импортируем функцию, которую тестируем

from unittest.mock import MagicMock, AsyncMock
from aiogram.types import Message
import app.database.requests as rq  # Импортируем внешнюю зависимость
from app.handlers import check  # Импортируем тестируемую функцию

@pytest.mark.asyncio
async def test_start():
    # Мокаем message и state
    message = MagicMock(Message)
    state = MagicMock(FSMContext)

    # Положительный тест:
    # Мокаем успешный ответ от метода answer, используя AsyncMock
    message.answer = AsyncMock()

    # Выполняем вызов тестируемой функции
    await start(message, state)

    # Проверяем, что был вызван метод answer с нужными параметрами
    message.answer.assert_called_once_with(
        text='Здарова, давай начнем составлять программу тренировок. Жми кнопку /create, чтобы сделать это, либо, если у тебя уже есть абонемент, жми на эту кнопку',
        reply_markup=kb.check_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при отправке сообщения, используя AsyncMock
    message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await start(message, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    message.answer.assert_called_once()

@pytest.mark.asyncio
async def test_register():
    # Мокаем объекты message и state
    message = MagicMock(Message)
    state = MagicMock(FSMContext)

    # Мокаем атрибут from_user в message
    message.from_user = MagicMock(User)
    message.from_user.id = 12345  # Устанавливаем ID пользователя

    # Мокаем методы, которые должны быть асинхронными
    message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    # Мокаем успешный ответ от метода answer и успешное обновление состояния
    await register(message, state)

    # Проверяем, что метод set_state был вызван дважды с правильными параметрами
    state.set_state.assert_any_call(Reg.tg_id)
    state.set_state.assert_any_call(Reg.age)

    # Проверяем, что метод update_data был вызван с правильными данными
    state.update_data.assert_called_once_with(tg_id=message.from_user.id)

    # Проверяем, что был вызван метод answer с правильными параметрами
    message.answer.assert_called_once_with(
        'Укажи свой возраст', reply_markup=kb.age_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await register(message, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await register(message, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_any_call(Reg.tg_id)

@pytest.mark.asyncio
async def test_reg_age():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = '25'  # Пример значения для возраста
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    # Мокаем успешный ответ от методов answer, update_data и set_state
    await reg_age(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(age=callback.data)
    state.set_state.assert_called_once_with(Reg.experience)
    callback.message.answer.assert_called_once_with(
        'Укажи свой опыт тренировок', reply_markup=kb.experience_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_age(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_age(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.experience)

@pytest.mark.asyncio
async def test_reg_exp():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'Beginner'  # Пример значения для опыта
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    # Мокаем успешный ответ от методов answer, update_data и set_state
    await reg_exp(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(experience=callback.data)
    state.set_state.assert_called_once_with(Reg.level)
    callback.message.answer.assert_called_once_with(
        'Укажи свой уровень физической подготовки', reply_markup=kb.level_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_exp(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_exp(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.level)


@pytest.mark.asyncio
async def test_reg_level():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'Intermediate'  # Пример значения для уровня
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    # Мокаем успешный ответ от методов answer, update_data и set_state
    await reg_level(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(level=callback.data)
    state.set_state.assert_called_once_with(Reg.goal)
    callback.message.answer.assert_called_once_with(
        'Укажи свою цель', reply_markup=kb.goal_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_level(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_level(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.goal)

@pytest.mark.asyncio
async def test_reg_goal():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'weight_loss'  # Пример значения для цели
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    await reg_goal(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(goal=callback.data)
    state.set_state.assert_called_once_with(Reg.type_tr)
    callback.message.answer.assert_called_once_with(
        'Выберите тип тренировок', reply_markup=kb.type_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_goal(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_goal(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.type_tr)


@pytest.mark.asyncio
async def test_reg_type():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'strength'  # Пример значения для типа тренировок
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    await reg_type(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(type_tr=callback.data)
    state.set_state.assert_called_once_with(Reg.quantity)
    callback.message.answer.assert_called_once_with(
        'Выберите количество тренировок в неделю', reply_markup=kb.quantity_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_type(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_type(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.quantity)



@pytest.mark.asyncio
async def test_reg_quantity():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = '3'  # Пример значения для количества тренировок в неделю
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()

    # Положительный тест:
    await reg_quantity(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(quantity=callback.data)
    state.set_state.assert_called_once_with(Reg.zones)
    callback.message.answer.assert_called_once_with(
        'Выберите зоны, на которых вы хотите сосредоточить внимание', reply_markup=kb.zones_keyboard
    )

    # Отрицательный тест:
    # Мокаем ошибку при вызове метода answer
    callback.message.answer = AsyncMock(side_effect=Exception("Failed to send message"))

    # Проверяем, что выбрасывается исключение при ошибке отправки сообщения
    with pytest.raises(Exception, match="Failed to send message"):
        await reg_quantity(callback, state)

    # Проверяем, что метод answer был вызван хотя бы один раз
    callback.message.answer.assert_called_once()

    # Мокаем ошибку при set_state
    state.set_state = AsyncMock(side_effect=Exception("Failed to set state"))

    # Проверяем, что выбрасывается исключение при ошибке обновления состояния
    with pytest.raises(Exception, match="Failed to set state"):
        await reg_quantity(callback, state)

    # Проверяем, что метод set_state был вызван хотя бы один раз
    state.set_state.assert_called_once_with(Reg.zones)




@pytest.mark.asyncio
async def test_reg_zones():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'chest'  # Пример данных (зона)
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={
        "age": "25",
        "experience": "beginner",
        "level": "intermediate",
        "goal": "lose_weight",
        "type_tr": "strength",
        "quantity": "3",
        "zones": "chest"
    })

    # Положительный тест:
    await reg_zones(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(zones=callback.data)
    state.get_data.assert_called_once()

    # Проверяем, что callback.message.answer был вызван с нужными аргументами
    callback.message.answer.assert_any_call('Секунду, программа тренировок составляется по заданным параметрам...')

    # Проверяем, что callback.message.answer был вызван с вопросом о записи в зал
    callback.message.answer.assert_any_call('Желаете ли записаться в зал?', reply_markup=abonement_keyboard)

    # Проверяем, что state.set_state был вызван с правильным параметром
    state.set_state.assert_called_once_with(Reg.abonement)

@pytest.mark.asyncio
async def test_abonement():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = 'disagree'  # Сценарий, когда пользователь не согласен с абонементом
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.clear = AsyncMock()
    state.get_data = AsyncMock(return_value={"abonement": "disagree"})  # Возвращаем значение disagree

    # Положительный тест:
    await abonement(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    state.update_data.assert_called_once_with(abonement=callback.data)
    state.get_data.assert_called_once()
    callback.message.answer.assert_any_call('Очень жаль, до свидания(')
    state.clear.assert_called_once()

    # Тест для ситуации, когда пользователь соглашается на абонемент:
    callback.data = 'agree'  # Меняем выбор пользователя на agree
    state.get_data = AsyncMock(return_value={"abonement": "agree"})  # Возвращаем значение agree

    # Проверяем положительный сценарий, когда абонемент согласен
    await abonement(callback, state)

    # Проверяем, что методы были вызваны с правильными параметрами
    callback.message.answer.assert_any_call('Отлично! Укажите, на какое время хотите взять абонемент.',
                                            reply_markup=time_keyboard)
    state.set_state.assert_called_once_with(Reg.time)

    # Отрицательный тест:
    # Мокаем ошибку при вызове state.get_data
    state.get_data = AsyncMock(side_effect=Exception("Ошибка при получении данных"))

    with pytest.raises(Exception, match="Ошибка при получении данных"):
        await abonement(callback, state)

    # Проверяем, что метод answer был вызван с правильными параметрами
    callback.message.answer.assert_any_call('Очень жаль, до свидания(')


@pytest.mark.asyncio
async def test_time():
    # Мокаем объекты callback и state
    callback = MagicMock(CallbackQuery)
    state = MagicMock(FSMContext)

    # Мокаем атрибуты в callback
    callback.data = '12:00'  # Пример данных (время)
    callback.message = MagicMock(Message)

    # Мокаем асинхронные методы
    callback.message.answer = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_data = AsyncMock(return_value={
        "tg_id": 123456789,
        "time": "12:00"
    })

    # Мокаем методы из rq
    rq.set_user = AsyncMock()
    rq.get_info = AsyncMock(return_value=30)  # Возвращаем 30 дней для абонемента

    # Положительный тест:
    await time(callback, state)

    # Проверяем, что state.update_data был вызван с правильным параметром
    state.update_data.assert_called_once_with(time=callback.data)

    # Проверяем, что state.get_data был вызван
    state.get_data.assert_called_once()

    # Проверяем, что set_user был вызван с правильными параметрами
    rq.set_user.assert_called_once_with(tg_id=123456789, time="12:00")

    # Проверяем, что get_info был вызван с правильным tg_id
    rq.get_info.assert_called_once_with(123456789)

    # Проверяем, что callback.message.answer был вызван с ожидаемым сообщением
    callback.message.answer.assert_any_call('Отлично! Вы записаны, ваш абонемент действителен еще 30 дней')

    # Проверяем, что state.clear был вызван для очистки состояния
    state.clear.assert_called_once()

    # Отрицательный тест: имитируем ошибку при получении информации о пользователе
    rq.get_info.side_effect = Exception("Ошибка при получении информации")

    # Проверяем, что исключение будет обработано
    with pytest.raises(Exception, match="Ошибка при получении информации"):
        await time(callback, state)

    # Проверяем, что метод answer был вызван до ошибки
    callback.message.answer.assert_any_call('Отлично! Вы записаны, ваш абонемент действителен еще 30 дней')
@pytest.mark.asyncio
async def test_check():
    # Мокаем объекты
    message = MagicMock(Message)
    message.from_user = MagicMock(id=123456789)  # Добавляем атрибут from_user с id
    message.answer = AsyncMock()  # Мокаем метод для отправки сообщений

    # Положительный тест: абонемент действителен, например, 30 дней
    rq.get_info = AsyncMock(return_value=30)  # Мокаем get_info для возврата 30 дней
    await check(message)

    # Проверяем, что метод answer был вызван с правильным сообщением
    message.answer.assert_called_once_with(
        'Ваш абонемент действителен еще 30 дней!', reply_markup=kb.check_keyboard
    )

    # Сбросим моки перед следующим тестом
    message.answer.reset_mock()

    # Отрицательный тест: абонемент истек
    rq.get_info = AsyncMock(return_value=0)  # Мокаем get_info для возврата 0 дней
    await check(message)

    # Проверяем, что метод answer был вызван с сообщением об истечении абонемента
    message.answer.assert_called_once_with(
        'К сожалению, ваш абонемент истек', reply_markup=kb.check_keyboard
    )

    # Проверяем, что del_user был вызван с правильным id
    # Подсмотрим, что за объект делаем мок для del_user
    del_user_mock = AsyncMock()  # Убедитесь, что вы мокаете эту функцию
    del_user_mock.assert_called_once_with(123456789)

    # Сбросим моки перед следующим тестом
    message.answer.reset_mock()

    # Отрицательный тест: абонемент не существует
    rq.get_info = AsyncMock(return_value=None)  # Мокаем get_info для возврата None
    await check(message)

    # Проверяем, что метод answer был вызван с сообщением о том, что абонемент не существует
    message.answer.assert_called_once_with(
        'К сожалению, вашего абонемента не существует('
    )

    # Подсчитываем количество вызовов метода answer
    assert message.answer.call_count == 3  # Должен быть вызван ровно 3 раза