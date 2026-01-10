"""
Модуль для создания основных 
==============================================

Classes
-------

Task
Employee
Project
"""
import time

class Task:
    """
    Класс описывающий задачи в системе.

    Parameters
    ----------
    name : str
        Название задачи
    discription : str
        Описание задачи
    project : Project, optional
        Проект, к которому относится задача (по умолчанию None)
    employee : Employee, optional
        Исполнитель задачи (по умолчанию None)
    status : str, optional
        Статус задачи ('todo', 'in progress', 'done') (по умолчанию 'todo')
    created_at : float, optional
        Время создания задачи (по умолчанию текущее время)
    updated_at : float, optional
        Время последнего обновления задачи (по умолчанию None)
    """
    def __init__(self, name, discription, project=None, employee=None, status='todo', created_at=time.time(), updated_at=None):
        self.name = name
        self.discription = discription
        self.project = project
        self.status = "todo" # todo, in progress, done 
        self.employee = employee
        self.created_at = time.time()
    
    def __repr__(self):
        """
        Возвращает информацию по задаче в виде строки.

        Returns
        -------
        str
            Форматированная строка с информацией о задаче
        """
        return f"<Задача {self.name}: {self.discription} [{self.status}] {self.project} {self.employee} {self.created_at}>"

class Employee:
    """
    Класс описывающий сотрудника.

    Parameters
    ----------
    first_name : str
        Имя сотрудника
    last_name : str
        Фамилия сотрудника
    email : str
        Email сотрудника
    """
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        """
        Возвращает информацию по сотруднику в виде строки.

        Returns
        -------
        str
            Форматированная строка с информацией о сотруднике
        """
        return f"<Сотрудник {self.first_name}: {self.last_name} <{self.email}>"
    
class Project:
    """
    Класс описывающий проект.

    Parameters
    ----------
    name : str
        Название проекта
    status : str, optional
        Статус проекта (по умолчанию 'New')
    created_at : float, optional
        Время создания проекта (по умолчанию текущее время)
    updated_at : float, optional
        Время последнего обновления (по умолчанию None)
    """
    def __init__(self, name, status='New', created_at=time.time(), updatetd_at=None):
        self.name = name
        self.status = status
        self.created_at = time.time()

    def __repr__(self):
        """
        Возвращает информацию по проекту в виде строки.

        Returns
        -------
        str
            Форматированная строка с информацией о проекте
        """
        return f"<Проект {self.name}: {self.status}"
    
