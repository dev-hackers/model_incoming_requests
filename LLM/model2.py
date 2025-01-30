
# Модель классификации запросов по типу "Запрос на обслуживние" или "Инциндент"
# 
# 


"""
pip install ****
"""

import re
import json
import requests
from typing import List, Optional
from tiktoken import get_encoding
from qdrant_client import models
from qdrant_client import QdrantClient
from fastembed.embedding import TextEmbedding

"""
Наш план по атрибутам.

Пишите. мне что за задание вы делаете.

Ускорение

https://github.com/beeware/toga/blob/main/core/src/toga/app.py
207 строка.

Пишите. мне что за задание вы делаете.

Атрибуты - передалать статью.
Класс шаблон
Роль основня экземпляр.
Переделать
Как переделать статью.
https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide

формулировка.
https://docs.python.org/3/faq/programming.html#what-is-a-class

Написать абстракцию
Улицу.

https://refactoring.guru/design-patterns/abstract-factory/python/example#example-0--Output-txt

коллекции

https://docs.python.org/3/library/collections.abc.html







"""


""" ----------- БЛОК QDRANT ----------"""

class Myqdrant():

    def __init__(self, collection_name, vector_name, k_top=10, token_limit=250):
        self.qdrant_client = QdrantClient("http://192.168.125.22:6333", timeout=600)
        self.dense_embedding_model_multilingual_e5_large = TextEmbedding("intfloat/multilingual-e5-large")
        self.encoding = get_encoding("cl100k_base")
        self.collection_name = collection_name
        self.k_top = k_top
        self.vector_name = vector_name
        self.token_limit = token_limit

    def qv_dencse_e5_large (self, query):
        """Преобразование текста в плотный вектор - multilingual_e5_large"""
        result = list(self.dense_embedding_model_multilingual_e5_large.passage_embed(query))[0].tolist()
        return result

    def conditions(self, filter_key=None, filter_value=None, request_id_except=None):
        """Формирование списка условий векторного поиска."""
        conditions = []
        if filter_key and filter_value is not None:
            conditions.append(
                models.FieldCondition(
                    key=filter_key,
                    match=models.MatchValue(value=filter_value),
                )
            )
        if request_id_except  is not None:
            conditions.append(
                models.FieldCondition(
                    key="request_id",
                    match=models.MatchExcept(**{"except": request_id_except}),
                )
        )
        return conditions

    def token_count (self, text):
        """Подсчет количества токенов в тексте."""
        return len(self.encoding.encode(text))

    def list_requests(self, results):
        """Подготовка списка примеров с ограничением по количеству токенов."""
        if not results:
            return []
        requests_point = []
        for point in results.points:
            query = f"{point.payload.get('name')}. {point.payload.get('content_cleaned')}"
            tokens_query = len(self.encoding.encode(query))
            if tokens_query < self.token_limit:
                requests_point.append(point)
        return requests_point

    def retriver_e5(self, query, filter_key=None, filter_value=None, request_id_except=None):
        """Векторный поиск по вектору 'multilingual-e5-large'."""
        conditions = self.conditions(filter_key, filter_value, request_id_except)
        results = self.qdrant_client.query_points(
            self.collection_name,
            query=self.qv_dencse_e5_large(query),
            using=self.vector_name,
            limit=self.k_top,
            with_payload=True,
            query_filter=models.Filter(must=conditions) if conditions else None
        )
        list_requests_point = self.list_requests(results)
        return list_requests_point


""" ----------- БЛОК LLM ----------"""

def extract_classification(text: str, classifications: List[str]) -> Optional[str]:
    for classification in classifications:
        if classification in text:
            return classification
    return None


def clear_dict(text):
    text = re.sub(r'^.*?{', '"{', text, flags=re.DOTALL)
    text = re.sub(r'}.*$', '}"', text)
    text = re.sub(r'\\\\\\\"', ' ', text)
    text = re.sub(r':\\\\.*?\\\\', '', text)
    text = re.sub(r'\\\\.*?\\\\', '', text)
    text = re.sub(r'\\n|\\\\', '', text)
    text = re.sub(r'""$', '"}"', text)
    text = re.sub(r'(?<=\"reasoning\":\s\")(.+?)(?=\"})', lambda m: m.group(0).replace(r'\"', ' '), text)
    return text


def llama3_request(system_message, user_message, assistant_message='', url = 'http://192.168.125.23:8000/llama3'):
    # Создаем строку запроса с параметрами
    params = {
        'system_message': system_message,
        'user_message': user_message,
        'assistant_message': assistant_message
    }
    # Выполняем GET-запрос с параметрами
    try:
        response = requests.get(url, params=params, timeout=120)  # таймаут 120 сек
        response.raise_for_status()  # Проверяем, нет ли ошибок HTTP     
    except requests.exceptions.Timeout:
        error = "Время ожидания запроса к LLM истекло"
        print(error)
        # сообщение бота error
        return None
    except requests.exceptions.ConnectionError:
        error = "Ошибка соединения к серверу LLM"
        print(error)
        # сообщение бота error
        return None
    except requests.exceptions.HTTPError as err:        
        error = f"HTTP ошибка сервера LLM: {err}"
        print(error)
        # сообщение бота error
        return None
    except requests.exceptions.RequestException as err:
        error = f"Произошла ошибка сервера LLM: {err}"
        print(error)
        # сообщение бота error
        return None
    # Проверяем статус ответа
    if response.status_code == 200:
        # Возвращаем ответ в виде строки
        return response.text
    else:
        # Если статус кода не 200, возвращаем сообщение об ошибке
        print(f"Error: Status code {response.status_code}")
        return None


def llama3_classification_type(system_message, user_message, assistant_message=''):
    response_llama3 = llama3_request(system_message, user_message, assistant_message='')
    if response_llama3:
        try:
            response_llama3_clear = clear_dict(response_llama3)
            result = json.loads(json.loads(response_llama3_clear))
            return result["classification"], result.get("scope")
        except:
            return extract_classification(response_llama3_clear, ["Критический", "Средний"]), 0.5
    return None, None

""" ----------- БЛОК PROMPT ----------"""

system_prompt = """Ты эксперт по установлению типа поступающих к тебе заявок от клиентов.
Классифицируй заявку как "Критический" или "Средний" на основе заданных примеров.
"""

def template_prompt_user(query, content):
    return f"""
Кдассифицируй следующий запрос от пользователя:

Запрос: { query }

Список примеров классификации:
{content}
Шаги по классификации запроса:
- Внимательно прочитайте предоставленный запрос клиента и примеры классификации.
- Проанализируйте запрос и на основе примеров определи, является ли запрос "Инцидент" или "Запрос на обслуживание".
- Дайте краткое объяснение своей классификации на русском языке.

Представьте свою классификацию и объяснение в следующем формате dict:
{{"classification": [вставьте либо Критический, либо «Средний»], "scope": [от 0.4 до 1], "reasoning": [ваше объяснение на русском языке]}}

Пример ответа:
{{"classification": "Критический", "scope": 0.95, "reasoning": "Не работает обмен между системами. Это типичный пример Критического запроса." }}

Проверь себя на соответствие заданному формату ответа.
"""


def points_to_content(points):
    content = ''
    for point in points:
        content+= f"{{\n'query' : {point.payload.get('name')}. {point.payload.get('content_cleaned')}\n'classification': {point.payload.get('real_type')}\n}},\n"
    return content


""" ----------- Экземпляр для работы с БД QDRANT ----------"""

myqdrant = Myqdrant(
    collection_name='energon_requests_summary_2', # Коллекция в БД.
    vector_name='multilingual-e5-large_summary', # Вектор поиска похожих примеров.
    k_top=15, # Число примеров.
    token_limit=250, # Ограничение на размер токенов в примере, если болше исключается из примеров.
)


""" ----------- Основная функция  ----------"""

def predict (subject, content=None):
    query = f"{subject}. {content}"
    points_1 = myqdrant.retriver_e5(query, filter_key="real_priority", filter_value="Средний")
    points_2 = myqdrant.retriver_e5(query, filter_key="real_priority", filter_value="Критический")
    user_prompt = template_prompt_user(query, points_to_content(points_1 + points_2))
    answer = llama3_classification_type(system_prompt, user_prompt)
    return {'results': answer[0].lower(), 'probabilities': answer[1]}


""" ----------- Проверка работы основной функции  ----------"""

if __name__ == "__main__":
    query = 'Актуализировать тестовую базу Srvr="s065";Ref="copy_tms_sb_4";'
    answer = predict(query)
    print(answer)  #{'results': 'средний', 'probabilities': 0.7}