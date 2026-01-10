import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from storage import Database

def get_tasks_df(db: Database):
    """
        Получить DataFrame с задачами.

        Метод берет из база данных задачи с их атрибутами и возвращает его в виде DataFrame

        Parameters
        --------
        db : Database
            Объект базы данных для получения данных

        Returns
        -----------
        pandas.DataFrame
            DataFrame с колонками:
                - task_id: идентификатор задачи
                - task_name: название задачи
                - discription: описание задачи
                - employee_id: идентификатор сотрудника
                - employee_name: имя сотрудника
                - employee_last_name: фамилия сотрудника
                - project_name: название проекта
                - project_id: идентификатор проекта
                - status: статус задачи

        Examples
        --------
        >>> df = get_tasks_df(db)
    """
    tasks = db.get_tasks_for_statistics()
    return pd.DataFrame(tasks, columns=('task_id', 'task_name', 'discription', 'employee_id', 'employee_name', 'employee_last_name', 'project_name', 'project_id', 'status'))

def project_statistics(db: Database, project_id):
    """
        Получить статистику по проекту.

        Parameters
        --------
        db : Database
            Объект базы данных
        project_id : int
            Идентификатор проекта для статистики

        Returns
        -----------
        dict
            Словарь с метриками проекта:
                - total_tasks: общее количество задач
                - completion_rate: процент выполненных задач (%)
                - employees_count: количество сотрудников
                - avg_tasks_per_employee: среднее количество задач на сотрудника
                - in_progress_ratio: доля задач в статусе 'in_progress'

        Examples
        --------
        >>> stats = project_statistics(db, 1)
        >>> stats['completion_rate']
        1.0
    """
    df = get_tasks_df(db)
    project_tasks = df[df['project_id'] == project_id]

    total_tasks = len(project_tasks)
    completed_tasks = len(project_tasks[project_tasks["status"] == "done"])
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    employees = project_tasks["employee_id"].nunique()

    avg_tasks_per_assignee = total_tasks / employees if employees > 0 else 0
    in_progress_ratio = len(project_tasks[project_tasks["status"] == "in_progress"]) / total_tasks

    return {
        "total_tasks": total_tasks,
        "completion_rate": completion_rate,
        "employees_count": employees,
        "avg_tasks_per_employee": avg_tasks_per_assignee,
        "in_progress_ratio": in_progress_ratio
    }

def plot_completion_rate(completion_rate, project_name):
    """
        Построить график процента выполнения задач в проекте.

        Parameters
        --------
        completion_rate : float
            Процент выполнения задач (от 0 до 100)
        project_name : int
            Идентификатор проекта для отображения на графике

        Examples
        --------
        >>> plot_completion_rate(20.0, 1)
        Отображает график
    """
    plt.figure(figsize=(6, 4))
    sns.barplot(x=[project_name], y=[completion_rate], palette="Blues")
    plt.title("Процент выполнения задач")
    plt.ylabel("Выполнение (%)")
    plt.ylim(0, 100)
    plt.show()