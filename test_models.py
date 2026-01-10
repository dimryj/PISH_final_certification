import unittest
from model import Task, Employee, Project
import time

class TestTaskModel(unittest.TestCase):
    
    def test_task_creation(self):
        # Проверка создания задачи с базовыми параметрами
        task = Task("Тестовая задача", "Описание задачи")
        self.assertEqual(task.name, "Тестовая задача")
        self.assertEqual(task.discription, "Описание задачи")
        self.assertEqual(task.status, "todo")
        self.assertIsNotNone(task.created_at)

    def test_task_employee_assignment(self):
        # Проверка назначения сотрудника на задачу
        employee = Employee("Иван", "Иванов", "ivan@example.com")
        task = Task("Задача", "Описание", employee=employee)
        self.assertEqual(task.employee, employee)
        self.assertEqual(task.employee.first_name, "Иван")

    def test_task_project_assignment(self):
        # Проверка назначения проекта на задачу
        project = Project("Проект X")
        task = Task("Задача", "Описание", project=project)
        self.assertEqual(task.project, project)
        self.assertEqual(task.project.name, "Проект X")

    def test_task_status_validation(self):
        # Проверка корректности установки статуса
        task = Task("Задача", "Описание")
        task.status = "in_progress"
        self.assertEqual(task.status, "in_progress")

    def test_task_timestamps(self):
        # Проверка временных меток
        start_time = time.time()
        task = Task("Задача", "Описание")
        end_time = time.time()
        
        self.assertGreaterEqual(task.created_at, start_time)
        self.assertLessEqual(task.created_at, end_time)


class TestEmployeeModel(unittest.TestCase):
    
    def test_employee_creation(self):
        # Проверка создания сотрудника
        employee = Employee("Петр", "Петров", "petr@example.com")
        self.assertEqual(employee.first_name, "Петр")
        self.assertEqual(employee.last_name, "Петров")
        self.assertEqual(employee.email, "petr@example.com")

    def test_employee_repr(self):
        # Проверка строкового представления
        employee = Employee("Анна", "Сидорова", "anna@example.com")
        expected = f"<Сотрудник Анна: Сидорова <anna@example.com>"
        self.assertEqual(repr(employee), expected)


class TestProjectModel(unittest.TestCase):
    
    def test_project_creation(self):
        # Проверка создания проекта
        project = Project("Новый проект")
        self.assertEqual(project.name, "Новый проект")
        self.assertEqual(project.status, "New")
        self.assertIsNotNone(project.created_at)

    def test_project_status_change(self):
        # Проверка изменения статуса проекта
        project = Project("Проект Y")
        project.status = "In Progress"
        self.assertEqual(project.status, "In Progress")

    def test_project_timestamps(self):
        # Проверка временных меток проекта
        start_time = time.time()
        project = Project("Проект Z")
        end_time = time.time()
        
        self.assertGreaterEqual(project.created_at, start_time)
        self.assertLessEqual(project.created_at, end_time)

if __name__ == '__main__':
    unittest.main()