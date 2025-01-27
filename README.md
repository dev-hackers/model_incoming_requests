# model_incoming_requests
Разработать модель классификации входящих запросов в службу поддержки.

"""
Разработать модель классификации входящих запросов в службу поддержки.
Тип классификации будет зависить от настройки модели.
Настраиваються следующие параметры:
1. Выбор LLM модели.
2. Выбор промта system и user.
3. Выбор векторной базы данных и типа вектора по которому будет происходить поиск.


Модель обладает обязательным методом predict(subject, content),
где subject - тема запроса, content - тело запроса.
Метод выводит результат в виде словаря: 
{'results': [result_class], 'probabilities': [probability]}
"""


""" Рассматриваю пока возможность работы с двумя векторными базами FAISS и QDRANT, а также с двумя LLM Llama и OpenAI"""


