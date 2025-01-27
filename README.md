Основная задача решается для людей. которые занимаются индивидуально.

**Если, Вы новичок - этот код не для Вас. Рекомендуется купить план индивидуамльного обучения и начать заниматься.**

[https://spb-tut.ru/programming_school/individual-programming-training/](https://spb-tut.ru/programming_school/individual-programming-training/)


Основные цели, изучение ООП на глубочайшем уровне, конкретно работа с атрибутами(это и есть вход в классы по полной)

Имеется файл LLM модели: `models2.py`, в котором написана костомная программа на обработка запросов двух разных ситуаций.
Задача используя библиотеки из этого файла, написать абстрактный код, который может быть использован в разных ситуациях.
Реализация при помощи:
Абстрактной фабрики.
Миксинов.
ОБработчика.

Предусмотреть возможность смены вопросов.
Смены AI

Пока все равно основная цель - это полное раскрытие ООП.




## Любая помощь, идея привествуется. Но в данный момент не нужно делать пул реквесты, а просто берёте репо себе в новом файле делаете свой вариант, очень подробно описывая и присылаете ссылку, Ваш файл будет добавлен и ссылка на ваш репо.




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

### Файлы.

- стартовый от куда отталкиваться: `model2.py`
- понимание абстрактной фабрики: `model_incoming_requests.git`
- основное приложение разработки: `model_incoming_requests.git`




