from mistralai import Mistral
from config import AI_TOKEN
async def generate(age, experience, level, goal, type_tr, quantity, zones):
    s = Mistral(
        api_key=AI_TOKEN,
    )
    res = await s.chat.complete_async(model="mistral-small-latest", messages=[
        {
            #"content": f'Составь программу тренировок по следующим входным данным: Ты должен составить эту программу для человека возраста {age}, опыт занятия в зале составляет {experience}, его уровень физичиеской подготовки - {level}, основная цель его занятий - {goal}, предпочтительный тип тренировок - {type_tr} он готов ходить в зал {quantity} раз в неделю, поэтому очень важно, чтобы количество тренировочных дней обязательно совпадало с {quantity}, увеличь количество упражнений в день на следующую зону: {zones}. Ответ напищи на русском языке. Вступительной фразой должна быть: "Вот ваша программа тренировок". Больше ничего вступительного писать не нужно. Не предлагай пользователю упражнения с собственным весом. Если человек взрослый напиши о большем времени отдыха между подходами. Порекомендуй пользователю подбирать такой вес на тренажере, чтобы он смог выполнить 8-12 повторений в каждом подходе. Скажи, какие упражнения пользователю делать не стоит, если у него были или есть травмы на определнной части тела. Для неопытного спортсмена вкратце распиши, что из себя представляет каждое предложенное тобой упражнение. Не предлагай жим ножницами ',
            "content": f'Act like a professional trainer and write plan of training for amateur sportsman according to such demandings: this must be a course for a person whose age is {age}, his experience of attending gym is {experience}, he {level}, the main purpose of his training is {goal}, he would like to mostly do {type_tr}, it is very important that the number of trainings a week is equal to {quantity} and you also have to suggest more exercises that develop {zones}. In your answer you should explain how did you use all the information I have given to you. Add this information to brief descriptions of exercises. The introductory sentence must be "Here is your plan of trainings". Do not write any more introductory sentences. You should also not suggest any exercises that do not require gym equipment. On each exercise write a warning that person should not do it if he had injured part of body this exercise develops most. And please translate your answer to Russian and send me only Russian instructions, I do not need English version. I need translation of high quality. I would also like you to add brief descriptions to the exercises. It is really essential that number jf symbols of your answer is not more than 4096',
            "role": "user",
        },
    ])
    if res is not None:
        return res.choices[0].message.content
