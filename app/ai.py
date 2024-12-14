'''
Файл, содержащий в себе запрос в нейросеть для составления программы тренировок.
'''
from mistralai import Mistral
from config import AI_TOKEN

async def generate(age, experience, level, goal, type_tr, quantity, zones):
    '''
    Асинхронная функция для генерации программы тренировок с учетом заданных параметров
    при помощи нейросети Mistral AI.

    Аргументы:
        age (int): Возраст пользователя.
        experience (str): Опыт пользователя в тренировках
        level (str): Уровень физической подготовки пользователя
        goal (str): Основная цель тренировок пользователя
        type_tr (str): Тип тренировок, который предпочитает пользователь
        quantity (int): Количество тренировок в неделю.
        zones (str): Зоны тела, которые следует развивать

    Действия:
        - открывает файл с шаблоном - prompt.txt
        - подставляет содержимое этого файла в запрос нейросети
        - подставляет аргументы в запрос
        - если результат есть - возвращает ответ нейросети

    Возвращает:
        str: Программа тренировок в виде строки на русском языке.
    '''
    s = Mistral(
        api_key=AI_TOKEN,
    )
    file = open('prompt.txt', 'r')
    content = file.read()


    res = await s.chat.complete_async(model="mistral-large-latest", messages=[
        {
            "content": content.format(age, experience, level, goal, type_tr, quantity, zones),
            "role": "user",
        },
    ])
    file.close()
    if res is not None:
        return res.choices[0].message.content
