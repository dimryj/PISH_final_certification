import tkinter as tk
from tkinter import ttk, messagebox
from model import Task, Project, Employee
from storage import Database

class TaskTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Задачник")
        self.db = Database()

        self.main_ui()

    def main_ui(self):
        tab_control = ttk.Notebook(self.root)
        
        self.tab_tasks = ttk.Frame(tab_control)
        self.tab_projects = ttk.Frame(tab_control)
        self.tab_employee = ttk.Frame(tab_control)
        self.tab_statistics = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_tasks, text='Задачи')
        tab_control.add(self.tab_projects, text='Проекты')
        tab_control.add(self.tab_employee, text='Сотрудники')
        tab_control.add(self.tab_statistics, text='Статистика')
        tab_control.pack(expand=1, fill='both')
        
        self.create_tasks_tab()
        self.create_projects_tab()
        self.create_employee_tab()
        #self.create_statistics_tab()
    
    def create_tasks_tab(self):
        tk.Label(self.tab_tasks, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = tk.Entry(self.tab_tasks, width=50)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_tasks, text="Описание:").grid(row=1, column=0, padx=5, pady=5)
        self.task_discription_entry = tk.Entry(self.tab_tasks, width=50)
        self.task_discription_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tab_tasks, text="Проект:").grid(row=2, column=0, padx=5, pady=5)
        self.task_project_entry = ttk.Combobox(self.tab_tasks, values=self.db.get_projects(), state='readonly')
        self.task_project_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.tab_tasks, text="Сотрудник:").grid(row=3, column=0, padx=5, pady=5)
        self.task_employee_entry = ttk.Combobox(self.tab_tasks, values=self.db.get_employees(), state='readonly')
        self.task_employee_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.tab_tasks, text="Добавить задачу", command=self.add_task).grid(row=4, column=0, columnspan=2, pady=10)
        
        tk.Label(self.tab_tasks, text="Фильтр по статусу:").grid(row=5, column=0, padx=5, pady=5)
        self.status_filter = ttk.Combobox(self.tab_tasks, values=['все', 'todo', 'in_progress', 'done'], state='readonly')
        self.status_filter.set('все')
        self.status_filter.grid(row=5, column=1, padx=5, pady=5)

        tk.Button(self.tab_tasks, text="Применить фильтр", command=self.filter_tasks).grid(row=5, column=2, padx=5, pady=5)

        self.tasks_list = ttk.Treeview(self.tab_tasks, columns=('id', 'Название', 'Исполнитель', 'Проект', 'Статус'), show='headings', height=10)
        self.tasks_list.heading('id', text='id')
        self.tasks_list.heading('Название', text='Название')
        self.tasks_list.heading('Исполнитель', text='Исполнитель')
        self.tasks_list.heading('Проект', text='Проект')
        self.tasks_list.heading('Статус', text='Статус')
        self.tasks_list.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.filter_tasks()

        tk.Button(self.tab_tasks, text="Удалить задачу", command=self.delete_task).grid(row=7, column=0, padx=5, pady=5)

    def create_projects_tab(self):
        tk.Label(self.tab_projects, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(self.tab_projects, width=50)
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_projects, text="Статус:").grid(row=1, column=0, padx=5, pady=5)
        self.project_status_entry = ttk.Combobox(self.tab_projects, values=['Active', 'Done', 'Canceled'], state='readonly')
        self.project_status_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.tab_projects, text="Добавить проект", command=self.add_project).grid(row=2, column=0, columnspan=2, pady=10)

        self.projects_list = ttk.Treeview(self.tab_projects, columns=('id', 'Название', 'Статус'), show='headings', height=10)
        self.projects_list.heading('id', text='id')
        self.projects_list.heading('Название', text='Название')
        self.projects_list.heading('Статус', text='Статус')
        self.projects_list.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_projects()

    def create_employee_tab(self):
        tk.Label(self.tab_employee, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.employee_first_name_entry = tk.Entry(self.tab_employee, width=50)
        self.employee_first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_employee, text="Фамилия:").grid(row=1, column=0, padx=5, pady=5)
        self.employee_last_name_entry = tk.Entry(self.tab_employee, width=50)
        self.employee_last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tab_employee, text="Email:").grid(row=2, column=0, padx=5, pady=5)
        self.employee_email_entry = tk.Entry(self.tab_employee, width=50)
        self.employee_email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Button(self.tab_employee, text="Добавить сутрудника", command=self.add_employee).grid(row=3, column=0, columnspan=2, pady=10)

        self.employees_list = ttk.Treeview(self.tab_employee, columns=('id', 'Имя', 'Фамилия', 'Email'), show='headings', height=10)
        self.employees_list.heading('id', text='id')
        self.employees_list.heading('Имя', text='Имя')
        self.employees_list.heading('Фамилия', text='Фамилия')
        self.employees_list.heading('Email', text='Email')
        self.employees_list.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_employees()

    def create_statistics_tab():
        pass

    def add_task(self):
        try:
            name = self.task_name_entry.get()
            if not name:
                messagebox.showerror("Ошибка", "Заголовок задачи не может быть пустым!")
                return

            discription = self.task_discription_entry.get()
            project = int(self.task_project_entry.get()[0][0])
            employee = self.task_employee_entry.get()[0][0]
            employee = int(employee) if employee.strip() else None

            task = Task(name, discription, project, employee)
            self.db.add_task(task)
            messagebox.showinfo("Успех", "Задача добавлена!")
            self.clear_task_fields()
            self.filter_tasks()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить задачу: {e}")

    def filter_tasks(self):
        try:
            status_filter = self.status_filter.get()
            tasks = self.db.get_tasks()

            # Фильтрация по статусу
            if status_filter != "все":
                tasks = [t for t in tasks if t.status == status_filter]

            # Обновление списка
            for row in self.tasks_list.get_children():
                self.tasks_list.delete(row)
            for row in tasks:
                self.tasks_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отфильтровать задачи: {e}")

    def add_project(self):
        try:
            project_name = self.project_name_entry.get()
            project_status = self.project_status_entry.get()

            project = Project(project_name, project_status)
            self.db.add_project(project)
            messagebox.showinfo("Успех", "Проект добавлен!")
            self.clear_project_fields()
            self.refresh_projects
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить проект: {e}")

    def refresh_projects(self):
        try: 
            for row in self.projects_list.get_children():
                self.projects_list.delete(row)
            projects = self.db.get_projects()
            for row in projects:
                self.projects_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить проекты: {e}")

    def add_employee(self):
        try:
            employee_first_name = self.employee_first_name_entry.get()
            employee_last_name = self.employee_last_name_entry.get()
            employee_email = self.employee_email_entry.get()

            employee = Employee(employee_first_name, employee_last_name, employee_email)
            self.db.add_employee(employee)
            messagebox.showinfo("Успех", "Сотрудник добавлен!")
            self.clear_employee_fields()
            self.refresh_employees()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить проект: {e}")

    def refresh_employees(self):
        try: 
            for row in self.employees_list.get_children():
                self.employees_list.delete(row)
            employees = self.db.get_employees()
            for row in employees:
                self.employees_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить сотрудников: {e}")

    def delete_task(self):
        try:
            selected = self.tasks_list.focus()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберите задачу для удаления")
                return
            row_id = self.tasks_list.item(selected, "values")[0]
            self.db.delete_task(row_id)
            messagebox.showinfo("Успех", "Задача удалена!")
            self.filter_tasks()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить задачу: {e}")

    def clear_task_fields(self):
        self.task_name_entry.delete(0, tk.END)
        self.task_discription_entry.delete(0, tk.END)
        self.task_project_entry.set('')
        self.task_employee_entry.set('')

    def clear_project_fields(self):
        self.project_name_entry.delete(0, tk.END)
        self.project_status_entry.delete(0, tk.END)
        
    def clear_employee_fields(self):
        self.employee_first_name_entry.delete(0, tk.END)
        self.employee_last_name_entry.delete(0, tk.END)
        self.employee_email_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()