"""
Задача:
1.Разработать абстрактный класс Street в котором будет возможность регистрировать произвольное число объектов относящихся к этому классу.

2. Разработать абстрактный класс AbstractStreet в котором будут реализованы методы:
- Добавление экземпляра объекта в список принадлежащих объектов для текущего экземпляра Street.
- Удаление экземпляра объекта из списка принадлежащих объектов для текущего экземпляра Street.
- Вывод экземпляров объектов содержащихся в экземпляре Street.
- Вывод количества объектов содержащихся в экземпляре Street по каждому типу объектов.

3. Реализовать абстрактный класс AbstractObject на основе которого будут создаваться конкретные классы объектов, которые будут принадлежать классу Street. 

4. Реализовать абстрактный класс AbstractHouse в котором будут реализованы методы:
- Инициализация с заданием типа экземпляра и описания.
- Вывод описания экземпляра.

5. Реализовать три конкретных класса House, Shopping, Station на основе абстрактного класса AbstractHouse.
"""

from abc import ABC, abstractmethod

class AbstractObject(ABC):
    @abstractmethod
    def __init__(self, description: str):
        self.description = description
        self.type = None
    def get_description(self):
        return self.type, self.description	

class House(AbstractObject):
    def __init__(self, description):  
        super().__init__(description)
        self.type = "House"

class Shopping(AbstractObject):
    def __init__(self, description):
        super().__init__(description)
        self.type = "Shopping"

class Station(AbstractObject):
    def __init__(self, description):
        super().__init__(description)
        self.type = "Station"


class AbstractStreet(ABC):

    @abstractmethod
    def add_object(self, object: AbstractObject):
        pass

    @abstractmethod
    def del_object(self, description: str):
        pass

    @abstractmethod
    def get_inventory(self):
        pass

    @abstractmethod
    def get_count(self):
        pass


class Street(AbstractStreet):
    def __init__(self):
        """
        Инициализация экземпляра Street.
        Список экземпляров объектов принадлежащих текщему экземпляру Street создается пустым.
        """
        self._street_inventory = []	

    def add_object(self, object: AbstractObject):
        """ Добавление экземпляра объекта в список принадлежащих объектов для текущего экземпляра Street.
        Args:
            object (AbstractObject): экземпляр объекта.
        Raises:
            ValueError: Ошибка если экземпляр с такимже описанием уже есть в текущем экземпляре Street.
        """
        exists = [obj for obj in self._street_inventory if obj.description == object.description]
        if not exists:
            self._street_inventory.append(object)
        else:
            raise ValueError(f"Addition is not possible. Object {object.description} already exists")

    def del_object(self, description: str):
        """ Удаление экземпляра объектоа из списока принадлежащих объектов текущего экземпляра Street.
        Args:
            description (str): Описание экземпляра объекта
        Raises:
            ValueError: Ошибка если объекта с таким описанием нет.
        """
        # self._street_inventory - список ссылок на экземпляры объектов
        # Цель удалить из списка self._street_inventory ссылку на экземпляр объекта с атрибутом description равным description-входной параметр.
        
        # Чтобы удалить объект из списка нужно найти ссылку на этот объект 
        # по значению атрибута description.
        # Это можно сделать несколькими способами. 
        # Первый вариант использует - https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions
        # В результате мы получим список exists, который будет пустой или только с одним элементом, так как описание уникально(проверка при вставке на уникальность)
        # После получения списка exists проверяем его на пустоту и если он не пустой, то удаляем этот элемент из списка.

        # 1. Вариант (самый компактный)
        exists = [obj for obj in self._street_inventory if obj.description == description]

        # 2. Вариант
        exits=[]
        for obj in self._street_inventory:
            if obj.description == description:
                exits.append(obj)
        # 1 и 2 варианты эквивалентны.

        if exists:
            self._street_inventory.remove(exists[0])
        else:
            raise ValueError(f"Deletion is not possible. Object {description} not found.")

        # 3. Вариант (самый намой взгляд читаемый)
        for obj in self._street_inventory:
            if obj.description == description:
                self._street_inventory.remove(obj)
                break
        else:
            raise ValueError(f"Deletion is not possible. Object {description} not found.")



    def get_inventory(self)-> list[tuple[str, str]]:
        """ Возвращает список объектов содержащихся в текущем экземпляре Street.
        Returns:
            list[tuple[str, str]]: Список объектов
        """
        list_inventory = []
        for object in self._street_inventory:
            list_inventory.append(object.get_description())
        return list_inventory

    def get_count(self)-> list[dict[str, int]]:
        """ Возвращает список где указывается количество объектов для каждого типа объектов.
        Returns:
            list[dict[str, int]]: Список где указывается количество объектов каждого типа.
        """
        count = []
        for type in set(obj.type for obj in self._street_inventory):
            count.append(
                {
                    "type": type,
                    "count": len([obj for obj in self._street_inventory if obj.type == type])
                }
            )
        return count


def main():
    try:
        # Создание экземпляра Street.
        my_street = Street()
        # Заполнение экземпляра Street экземплярами объектов
        my_street.add_object(House('Hs1'))
        my_street.add_object(Shopping('Sh1'))
        my_street.add_object(Station('St1'))
        my_street.add_object(Station('St2'))
        # Вывод экземпляров объектов содержащихся в экземпляре my_street типа Street.
        print(my_street.get_inventory()) # [('House', 'Hs1'), ('Shopping', 'Sh1'), ('Station', 'St1'), ('Station', 'St2')]
        # Вывод количества экземпляров объектов содержащихся в экземпляре my_street по типам.
        print(my_street.get_count()) # [{'type': 'Station', 'count': 2}, {'type': 'Shopping', 'count': 1}, {'type': 'House', 'count': 1}]
        # Удаление экземпляра объекта из экземпляра Street
        my_street.del_object('St2')
        # Вывод экземпляров объектов содержащихся в экземпляре my_street типа Street.
        print(my_street.get_inventory()) # [('House', 'Hs1'), ('Shopping', 'Sh1'), ('Station', 'St1')]
        # Вывод количества экземпляров объектов содержащихся в экземпляре my_street по типам.
        print(my_street.get_count()) # [{'type': 'Station', 'count': 1}, {'type': 'Shopping', 'count': 1}, {'type': 'House', 'count': 1}]

    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()