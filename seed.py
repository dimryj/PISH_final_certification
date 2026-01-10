from storage import Database
from model import Task, Project, Employee

def create_sample_data():
    """
        Метод создает и загружает тестовые данные в БД.

        Example
        --------
        >>> app.create_sample_data()
    """
    db = Database()

    print("Начинаем заполнение базы данных...")
    projects = [
        Project("Проект 1", "Active"),
        Project("Проект 2", "Active"),
        Project("Проект 3", "Active"),
        Project("Проект 4", "Active"),
        Project("Проект 5", "Active")
    ]

    for project in projects:
        try:
            db.add_project(project)
            print(f"Проект '{project.name}' добавлен")
        except Exception as e:
            print(f"Ошибка при добавлении проекта '{project.name}': {e}")

    employees = [
        Employee("Иван", "Иванов", "ivan@example.com"),
        Employee("Петр", "Петров", "petr@example.com"),
        Employee("Анна", "Сидорова", "anna@example.com"),
        Employee("Мария", "Иванова", "maria@example.com"),
        Employee("Алексей", "Смирнов", "alexey@example.com")
    ]

    for employee in employees:
        try:
            db.add_employee(employee)
            print(f"Сотрудник '{employee.email}' добавлен")
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника '{employee.email}': {e}")

    tasks = [
        Task("Задача 1", "Описание задачи 1", 1, 1, "todo"),
        Task("Задача 2", "Описание задачи 2", 1, 2, "todo"),
        Task("Задача 3", "Описание задачи 3", 1, 1, "todo"),
        
        Task("Задача 4", "Описание задачи 4", 2, 3, "todo"),
        Task("Задача 5", "Описание задачи 5", 2, 4, "todo"),
        Task("Задача 6", "Описание задачи 6", 2, 2, "todo"),
        
        Task("Задача 7", "Описание задачи 7", 3, 5, "todo"),
        Task("Задача 8", "Описание задачи 8", 3, 1, "todo"),
        Task("Задача 9", "Описание задачи 9", 3, 5, "todo"),
        
        Task("Задача 10", "Описание задачи 10", 4, 2, "todo"),
        Task("Задача 11", "Описание задачи 11", 4, 4, "todo"),
        Task("Задача 12", "Описание задачи 12", 4, 2, "todo"),
        
        Task("Задача 13", "Описание задачи 13", 5, 3, "todo"),
        Task("Задача 14", "Описание задачи 14", 5, 5, "todo"),
        Task("Задача 15", "Описание задачи 15", 5, 2, "todo")
    ]

    for task in tasks:
        try:
            db.add_task(task)
            print(f"Задача '{task.name}' добавлена (проект {task.project}, статус {task.status})")
        except Exception as e:
            print(f"Ошибка при добавлении задачи '{task.name}': {e}")

    print("\nЗаполнение базы данных завершено!")