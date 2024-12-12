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
    print(content)

    res = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            #"content": f'Составь программу тренировок по следующим входным данным: Ты должен составить эту программу для человека возраста {age}, опыт занятия в зале составляет {experience}, его уровень физичиеской подготовки - {level}, основная цель его занятий - {goal}, предпочтительный тип тренировок - {type_tr} он готов ходить в зал {quantity} раз в неделю, поэтому очень важно, чтобы количество тренировочных дней обязательно совпадало с {quantity}, увеличь количество упражнений в день на следующую зону: {zones}. Ответ напищи на русском языке. Вступительной фразой должна быть: "Вот ваша программа тренировок". Больше ничего вступительного писать не нужно. Не предлагай пользователю упражнения с собственным весом. Если человек взрослый напиши о большем времени отдыха между подходами. Порекомендуй пользователю подбирать такой вес на тренажере, чтобы он смог выполнить 8-12 повторений в каждом подходе. Скажи, какие упражнения пользователю делать не стоит, если у него были или есть травмы на определнной части тела. Для неопытного спортсмена вкратце распиши, что из себя представляет каждое предложенное тобой упражнение. Не предлагай жим ножницами ',
            #"content": f'Act like a professional trainer and write plan of trainings for amateur sportsman according to such demands: this must be a course for a person whose age is {age}, his experience of attending gym is {experience}, he {level}, the main purpose of his training is {goal}, he would like to mostly do {type_tr}, it is very important that the number of trainings a week is equal to {quantity} and you also have to suggest more exercises that develop {zones}. In your answer you should explain how did you use all the information I have given to you. Add this information to brief descriptions of exercises. The introductory sentence must be "Here is your plan of trainings". Do not write any more introductory sentences. You should also not suggest any exercises that do not require gym equipment. Offer the user one of the following exercises: pecs: dumbbell bench press, horizontal bench press, dumbbell bench press, crossover chest press. For triceps: French press standing in a crossover with a rope, arm curls in a crossover with a rope, arm curls in a crossover with a curved or straight bar, French bench press. For the back muscles: vertical pull with a straight bar, horizontal pull, vertical pull with a narrow grip, barbell/dumbbell pull on the broadest muscles of the back. Biceps: straight barbell biceps curl, dumbbell biceps curl, dumbbell biceps curl, hammer press, crossover biceps curl, EZ barbell biceps curl, EZ barbell curl on Scott bench. Shoulders: barbell pull-downs, dumbbell swings, crossover swings. Legs: leg curls, leg curls, leg press, toe raises sitting in a machine or standing with dumbbells, squat with a barbell, lunges with additional weight, single leg squat with additional weight (if it works). Cardio: burpees, treadmill running. You can also suggest some exercises not on this list. On each exercise write a warning that person should not do it if he had injured part of body this exercise develops most. I would also like you to add brief descriptions to the exercises. Translate your message to russian and send me only the translation. I do not need english version. It is really essential that number of symbols of your answer is not more than 4096.',
            "content": content.format(age, experience, level, goal, type_tr, quantity, zones),
            #"content": f'Act like a professional trainer and write plan of training for amateur sportsman according to such demands: this must be a course for a person whose age is {age}, his experience of attending gym is {experience}, he {level}, the main purpose of his training is {goal}, he would like to mostly do {type_tr}, it is very important that the number of trainings a week is equal to {quantity} and you also have to suggest more exercises that develop {zones}. In your answer you should explain how did you use all the information I have given to you. Add this information to brief descriptions of exercises. The introductory sentence must be "Here is your plan of trainings". Do not write any more introductory sentences. You should also not suggest any exercises that do not require gym equipment. On each exercise write a warning that person should not do it if he had injured part of body this exercise develops most. I would also like you to add brief descriptions to the exercises. Translate your message to russian and send me only the translation. I do not need english version. It is really essential that number of symbols of your answer is not more than 4096',
            "role": "user",
        },
    ])
    file.close()
    if res is not None:
        return res.choices[0].message.content
