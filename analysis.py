import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from storage import Database

def get_tasks_df(db: Database):
    """Получить DataFrame с задачами."""
    tasks = db.get_tasks_for_statistics()
    return pd.DataFrame(tasks, columns=('task_id', 'task_name', 'discription', 'employee_id', 'employee_name', 'employee_last_name', 'project_name', 'project_id', 'status'))

def project_statistics(db: Database, project_id):
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
    plt.figure(figsize=(6, 4))
    sns.barplot(x=[project_name], y=[completion_rate], palette="Blues")
    plt.title("Процент выполнения задач")
    plt.ylabel("Выполнение (%)")
    plt.ylim(0, 100)
    plt.show()