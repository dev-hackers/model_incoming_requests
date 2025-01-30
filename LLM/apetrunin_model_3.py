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


from abc import ABC, abstractmethod
from typing import Any


class AbstractClassification(ABC):
    
    def __init__(self, type_llm: str, type_db: str, type_vector: str, system: str, user: str):
        self.system = system
        self.user = user

    @abstractmethod
    def predict(self, subject: str, content: str)->dict[str, str]:
        pass
    
    @abstractmethod
    def _retriver(self, query, *args, **kwargs)->list[Any]:
        pass

    @abstractmethod
    def _llm_request(self, system: str, user: str, assistent:str =''):
        pass

    @abstractmethod
    def _handler_answer_llm(self, answer_llm: str)->dict[str, str]:
        pass


class FaissClassification(AbstractClassification):
    def _retriver(self, query, *args, **kwargs)->list[Any]:
        pass

class QdrantClassification(AbstractClassification):
    def _retriver(self, query, *args, **kwargs)->list[Any]:
        pass

class LlamaMixin():
    def _llm_request(self, system: str, user: str, assistent:str =''):
        pass

    def _handler_answer_llm(self, answer_llm: str)->dict[str, str]:
        pass

class OpenaiMixin():
    def _llm_request(self, system: str, user: str, assistent:str =''):
        pass

    def _handler_answer_llm(self, answer_llm: str)->dict[str, str]:
        pass

class LlamaFaissClassification(LlamaMixin, FaissClassification):
    def predict(self, subject: str, content: str)->dict[str, str]:
        pass

class OpenaiFaissClassification(LlamaMixin, FaissClassification):
    def predict(self, subject: str, content: str)->dict[str, str]:
        pass

class LlamaQdrantClassification(LlamaMixin, FaissClassification):
     def predict(self, subject: str, content: str)->dict[str, str]:
        pass

class OpenaiQdrantClassification(LlamaMixin, FaissClassification):
    def predict(self, subject: str, content: str)->dict[str, str]:
        pass