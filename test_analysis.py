import unittest
import pandas as pd
from analysis import get_tasks_df, project_statistics, plot_completion_rate

# Определяем MockDatabase вне setUp, чтобы он был доступен всем тестам
class MockDatabase:
    def __init__(self, tasks):
        self.tasks = tasks
        
    def get_tasks_for_statistics(self):
        return self.tasks

class TestAnalysisModule(unittest.TestCase):
    
    def setUp(self):
        # Создаем тестовые данные
        self.test_tasks = [
            (1, 'Задача 1', 'Описание 1', 1, 'Иван', 'Иванов', 'Проект 1', 100, 'done'),
            (2, 'Задача 2', 'Описание 2', 2, 'Петр', 'Петров', 'Проект 1', 100, 'in_progress'),
            (3, 'Задача 3', 'Описание 3', 1, 'Иван', 'Иванов', 'Проект 1', 100, 'todo'),
            (4, 'Задача 4', 'Описание 4', 3, 'Анна', 'Сидорова', 'Проект 2', 200, 'done')
        ]
        
        self.db = MockDatabase(self.test_tasks)

    def test_get_tasks_df(self):
        df = get_tasks_df(self.db)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 4)
        self.assertEqual(set(df.columns), 
                        {'task_id', 'task_name', 'discription', 
                         'employee_id', 'employee_name', 'employee_last_name',
                         'project_name', 'project_id', 'status'})
        
    def test_project_statistics(self):
        project_id = 100
        expected = {
            'total_tasks': 3,
            'completion_rate': 33.33333333333333,
            'employees_count': 2,
            'avg_tasks_per_employee': 1.5,
            'in_progress_ratio': 1/3
        }
        
        stats = project_statistics(self.db, project_id)
        self.assertEqual(stats['total_tasks'], expected['total_tasks'])
        self.assertAlmostEqual(stats['completion_rate'], expected['completion_rate'], places=2)
        self.assertEqual(stats['employees_count'], expected['employees_count'])
        self.assertAlmostEqual(stats['avg_tasks_per_employee'], expected['avg_tasks_per_employee'])
        self.assertAlmostEqual(stats['in_progress_ratio'], expected['in_progress_ratio'])

    def test_plot_completion_rate(self):
        plot_completion_rate(50.0, 'Проект X')

    def test_project_statistics_empty_project(self):
        # Создаем пустую базу данных
        empty_tasks = []
        empty_db = MockDatabase(empty_tasks)
        
        stats = project_statistics(empty_db, 999)
        self.assertEqual(stats['total_tasks'], 0)
        self.assertEqual(stats['completion_rate'], 0)
        self.assertEqual(stats['employees_count'], 0)
        self.assertEqual(stats['avg_tasks_per_employee'], 0)
        self.assertEqual(stats['in_progress_ratio'], 0)

    def test_invalid_project_id(self):
        stats = project_statistics(self.db, 999)
        self.assertEqual(stats['total_tasks'], 0)
        self.assertEqual(stats['completion_rate'], 0)
        self.assertEqual(stats['employees_count'], 0)
        self.assertEqual(stats['avg_tasks_per_employee'], 0)
        self.assertEqual(stats['in_progress_ratio'], 0)

if __name__ == '__main__':
    unittest.main()