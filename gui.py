"""
Модуль графического интерфейса для приложения "Задачник"

Classes
-----------

TaskTrackerApp
"""

import tkinter as tk
from tkinter import ttk, messagebox
from model import Task, Project, Employee
from storage import Database
from analysis import project_statistics, plot_completion_rate
import time
from utils import is_valid_email, clean_string

class TaskTrackerApp: #TODO разнести функции по вкладкам на разыне файлы, что бы было проще работать с отдальными вкладками
    """
    Настольное приложение "Задачник"
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Задачник")
        self.db = Database()
        self.main_ui()
        self.tasks_list.bind("<<TreeviewSelect>>", self.on_task_row_select)
        self.projects_list.bind("<<TreeviewSelect>>", self.on_project_row_select)
        self.employees_list.bind("<<TreeviewSelect>>", self.on_employee_row_select)

    def main_ui(self):
        """
            Создание основных элементов интерфейса

            Создает основные вкладки, задачет их названия и запускает функции их наполнения

            Examples
            --------
            >>> app.main_ui()
        """
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
        self.create_statistics_tab()

    def create_tasks_tab(self):
        """
            Интерфейс вкладки "Задачи"

            Отрисовывает заголовки, кнопки, фильтр и список задач

            Examples
            --------
            >>> app.create_tasks_tab()
        """
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

        tk.Label(self.tab_tasks, text="Статус:").grid(row=4, column=0, padx=5, pady=5)
        self.task_status_entry = ttk.Combobox(self.tab_tasks, values=['todo', 'in_progress', 'done'], state='readonly')
        self.task_status_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self.tab_tasks, text="Добавить задачу", command=self.add_task).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.tab_tasks, text="Изменить задачу", command=self.edit_task).grid(row=5, column=2, columnspan=2, pady=10)
        
        tk.Label(self.tab_tasks, text="Фильтр по статусу:").grid(row=6, column=0, padx=5, pady=5)
        self.status_filter = ttk.Combobox(self.tab_tasks, values=['все', 'todo', 'in_progress', 'done'], state='readonly')
        self.status_filter.set('все')
        self.status_filter.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.tab_tasks, text="Применить фильтр", command=self.filter_tasks).grid(row=6, column=2, padx=5, pady=5)

        self.tasks_list = ttk.Treeview(self.tab_tasks, columns=('id', 'Название', 'Описание', 'Исполнитель', 'Проект', 'Статус'), show='headings', height=10)
        self.tasks_list.heading('id', text='id')
        self.tasks_list.heading('Название', text='Название')
        self.tasks_list.heading('Описание', text='Описание')
        self.tasks_list.heading('Исполнитель', text='Исполнитель')
        self.tasks_list.heading('Проект', text='Проект')
        self.tasks_list.heading('Статус', text='Статус')
        self.tasks_list.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

        self.filter_tasks()

        tk.Button(self.tab_tasks, text="Удалить задачу", command=self.delete_task).grid(row=8, column=0, padx=5, pady=5)

    def create_projects_tab(self):
        """
            Интерфейс вкладки "Проекты"

            Отрисовывает заголовки, кнопки и список проектов

            Examples
            --------
            >>> app.create_projects_tab()
        """
        tk.Label(self.tab_projects, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.project_name_entry = tk.Entry(self.tab_projects, width=50)
        self.project_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab_projects, text="Статус:").grid(row=1, column=0, padx=5, pady=5)
        self.project_status_entry = ttk.Combobox(self.tab_projects, values=['Active', 'Done', 'Canceled'], state='readonly')
        self.project_status_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.tab_projects, text="Добавить проект", command=self.add_project).grid(row=2, column=0, columnspan=2, pady=10)
        tk.Button(self.tab_projects, text="Изменить проект", command=self.edit_project).grid(row=2, column=1, columnspan=2, pady=10)

        self.projects_list = ttk.Treeview(self.tab_projects, columns=('id', 'Название', 'Статус'), show='headings', height=10)
        self.projects_list.heading('id', text='id')
        self.projects_list.heading('Название', text='Название')
        self.projects_list.heading('Статус', text='Статус')
        self.projects_list.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_projects()

    def create_employee_tab(self):
        """
            Интерфейс вкладки "Сотрудники"

            Отрисовывает заголовки, кнопки и список сотрудников

            Examples
            --------
            >>> app.create_employee_tab()

        """
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
        tk.Button(self.tab_employee, text="Изменить сутрудника", command=self.edit_employee).grid(row=3, column=1, columnspan=2, pady=10)

        self.employees_list = ttk.Treeview(self.tab_employee, columns=('id', 'Имя', 'Фамилия', 'Email'), show='headings', height=10)
        self.employees_list.heading('id', text='id')
        self.employees_list.heading('Имя', text='Имя')
        self.employees_list.heading('Фамилия', text='Фамилия')
        self.employees_list.heading('Email', text='Email')
        self.employees_list.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_employees()

    def create_statistics_tab(self):
        """
            Интерфейс вкладки "Статистика"

            Отрисовывает заголовки, текстовое поле и кнопки для вкладки статистики

            Examples
            --------
            >>> app.create_statistics_tab()
        """
        tk.Label(self.tab_statistics, text="Проект:").grid(row=0, column=0, padx=5, pady=5)
        self.analysis_project_id_entry = ttk.Combobox(self.tab_statistics, values=self.db.get_projects(), state='readonly')
        self.analysis_project_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.tab_statistics, text="Посмотреть статистику", command=self.show_statistics).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.tab_statistics, text="Посмотреть график", command=self.show_plot).grid(row=0, column=3, padx=5, pady=5)

        self.analysis_result = tk.Text(self.tab_statistics, height=15, width=60)
        self.analysis_result.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        tk.Button(self.tab_statistics, text="Сохранить отчёт в файл", command=self.save_report).grid(row=2, column=0, columnspan=3, pady=10)

    def add_task(self):
        """
            Добавление задачи

            Берет значения из полей для ввода, добавляет задачу в базу данных, показывает
            сообщение о добавленной задаче, очищает поля ввода и обновляет таблицу с задачами.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.
            
            Examples
            --------
            >>> app.add_task()
        """
        try:
            name = clean_string(self.task_name_entry.get())
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

    def edit_task(self):
        """
            Редактирование задачи

            Берет значения из полей для ввода, проверяет что выбрана строка, которую необходимо изменить,
            сохраняет изменения базе данных, показывает сообщение об успехе изменения.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.edit_task()
        """
        try:
            task_name = self.task_name_entry.get()
            task_discription = self.task_discription_entry.get()
            task_project = self.task_project_entry.get()[0][0]
            task_employee = self.task_employee_entry.get()[0][0]
            task_status = self.task_status_entry.get()
            updated_at = time.time()
            
            selected = self.tasks_list.focus()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберете задачу для изменения")
                return
            row_id = self.tasks_list.item(selected, "values")[0]
            self.db.edit_task(row_id, task_name, task_discription, task_project, task_employee, task_status, updated_at)
            messagebox.showinfo("Успех", "Задача обновлена!")
            self.filter_tasks()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить задачу: {e}")

    def filter_tasks(self):
        """
            Показывает все задачи или с учетом выбранного фильтра

            Берет значения из поля фильтра, получает все задачи из базы данных и заполняет ими таблицу с задачами.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.filter_tasks()
        """
        try:
            status_filter = self.status_filter.get()
            tasks = self.db.get_tasks()

            # Фильтрация по статусу
            if status_filter != "все":
                tasks = [t for t in tasks if t[4] == status_filter]

            # Обновление списка
            for row in self.tasks_list.get_children():
                self.tasks_list.delete(row)
            for row in tasks:
                self.tasks_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отфильтровать задачи: {e}")

    def add_project(self):
        """
            Добавление проекта

            Берет значения из полей для ввода, добавлет проект в базу данных, показывает сообщение об успехе клиенту и обновляет список проектов.
            При успехе показывает сообщение о добавлении, очищает поля ввода и обновлет список проектов.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.add_project()
        
        """
        try:
            project_name = self.project_name_entry.get()
            project_status = self.project_status_entry.get()
            # TODO добавить проерку на одинаковое название проектов
            project = Project(project_name, project_status)
            self.db.add_project(project)
            messagebox.showinfo("Успех", "Проект добавлен!")
            self.clear_project_fields()
            self.refresh_projects
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить проект: {e}")

    def edit_project(self):
        """
            Редактирование проекта

            Берет значения из полей для ввода, проверяет что выбрана строка, которую необходимо изменить, 
            изменияет запись и обновлет список проектов.В случае ошибки при получении
            данных отображает сообщение об ошибке пользователю.
            
            Examples
            --------
            >>> app.edit_project()
        """
        try:
            project_name = self.project_name_entry.get()
            project_status = self.project_status_entry.get()
            updated_at = time.time()
            
            selected = self.projects_list.focus()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберете проект для изменения")
                return
            row_id = self.projects_list.item(selected, "values")[0]
            self.db.edit_project(row_id, project_name, project_status, updated_at)
            messagebox.showinfo("Успех", "Проект обновлен!")
            self.refresh_projects()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить проект: {e}")

    def refresh_projects(self):
        """
            Обновляет список проектов в интерфейсе приложения.

            Метод очищает таблицу проектов, загружает актуальный список проектов
            из базы данных и отображает их в таблице. В случае ошибки при получении
            данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.refresh_projects()
        """
        try: 
            for row in self.projects_list.get_children():
                self.projects_list.delete(row)
            projects = self.db.get_projects()
            for row in projects:
                self.projects_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить проекты: {e}")

    def add_employee(self):
        """
            Добавление сотрудников.

            Метод берет данные из полей ввода, проверяет их на заполненость,
            создает нового сотрудника в базе данных, показывает сообщение 
            о добавлении сотрудника и обновляет список сотрудников. В случае ошибки при получении
            данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.refresh_projects()
        """
        try:
            employee_first_name = clean_string(self.employee_first_name_entry.get())
            employee_last_name = clean_string(self.employee_last_name_entry.get())
            employee_email = self.employee_email_entry.get()

            if employee_first_name == '' or employee_last_name == '' or employee_email == '':
                raise ValueError('Все поля должны быть заполнены')

            if not is_valid_email(employee_email):
                raise ValueError('Не корректная почта')

            employee = Employee(employee_first_name, employee_last_name, employee_email)
            self.db.add_employee(employee)
            messagebox.showinfo("Успех", "Сотрудник добавлен!")
            self.clear_employee_fields()
            self.refresh_employees()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить сотрудника: {e}")

    def edit_employee(self):
        """
            Изменение сотрудника.

            Метод очищает таблицу проектов, загружает актуальный список проектов
            из базы данных и отображает их в таблице. В случае ошибки при получении
            данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.edit_employee()
        """
        try:
            employee_first_name = self.employee_first_name_entry.get()
            employee_last_name = self.employee_last_name_entry.get()
            employee_email = self.employee_email_entry.get()

            selected = self.employees_list.focus()
            if not selected:
                messagebox.showwarning("Ошибка", "Выберете сотрудника для изменения")
                return
            row_id = self.employees_list.item(selected, "values")[0]
            self.db.edit_employee(row_id, employee_first_name, employee_last_name, employee_email)
            messagebox.showinfo("Успех", "Сотрудник обновлен!")
            self.refresh_employees()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить сотрудника: {e}")

    def refresh_employees(self):
        """
            Обновляет список сотрудников в интерфейсе приложения.

            Метод очищает таблицу сотрудников, загружает актуальный список сорудников
            из базы данных и отображает их в таблице. В случае ошибки при получении
            данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.refresh_employees()
        """
        try: 
            for row in self.employees_list.get_children():
                self.employees_list.delete(row)
            employees = self.db.get_employees()
            for row in employees:
                self.employees_list.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить сотрудников: {e}")

    def delete_task(self):
        """
            Удаление задачи.

            Метод берет берет выбранную строку и удаляет задачу из базы данных, показывает сообщение об удалении и обновляет список задач.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.delete_task()
        """
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
        """
            Очистка поле ввода задач.

            Метод очищает поля вввода на вкладке "Задачи".

            Examples
            --------
            >>> app.clear_task_fields()
        """
        self.task_name_entry.delete(0, tk.END)
        self.task_discription_entry.delete(0, tk.END)
        self.task_project_entry.set('')
        self.task_employee_entry.set('')

    def clear_project_fields(self):
        """
            Очистка поле ввода проектов.

            Метод очищает поля вввода на вкладке "Проекты".

            Examples
            --------
            >>> app.clear_project_fields()
        """
        self.project_name_entry.delete(0, tk.END)
        self.project_status_entry.delete(0, tk.END)
        
    def clear_employee_fields(self):
        """
            Очистка поле ввода сотрудников.

            Метод очищает поля вввода на вкладке "Сотрудники".

            Examples
            --------
            >>> app.clear_employee_fields()
        """
        self.employee_first_name_entry.delete(0, tk.END)
        self.employee_last_name_entry.delete(0, tk.END)
        self.employee_email_entry.delete(0, tk.END)

    def on_task_row_select(self, event):
        """
            Заполнение поле ввода при выбранной задаче.

            Метод берет данные из выбранной строки и заполняет поля ввода.

            Examples
            --------
            >>> app.on_task_row_select()
        """
        selected_items = self.tasks_list.selection()
        if not selected_items:
            return
        item = selected_items[0]
        values = self.tasks_list.item(item, "values")
        
        self.task_name_entry.delete(0, tk.END)
        self.task_name_entry.insert(0, values[1])

        self.task_discription_entry.delete(0, tk.END)
        self.task_discription_entry.insert(0, values[2])

        self.task_project_entry.set(values[4]) # TODO надо подставлять всю строку проекта, что бы не приходилось дополнительно выбирать при изменении. Или придумать еще какой-то способ
        self.task_employee_entry.set(values[3]) # TODO надо подставлять всю строку проекта, что бы не приходилось дополнительно выбирать при изменении. Или придумать еще какой-то способ
        self.task_status_entry.set(values[5])


    def on_project_row_select(self, event):
        """
            Заполнение поле ввода при выбранному проекту.

            Метод берет данные из выбранной строки и заполняет поля ввода.

            Examples
            --------
            >>> app.on_project_row_select()
        """
        selected_items = self.projects_list.selection()
        if not selected_items:
            return
        item = selected_items[0]
        values = self.projects_list.item(item, "values")
                
        self.project_name_entry.delete(0, tk.END)
        self.project_name_entry.insert(0, values[1])

        self.project_status_entry.set(values[2])

    def on_employee_row_select(self, event):
        """
            Заполнение поле ввода при выбранному сотруднику.

            Метод берет данные из выбранной строки и заполняет поля ввода.

            Examples
            --------
            >>> app.on_employee_row_select()
        """
        selected_items = self.employees_list.selection()
        if not selected_items:
            return
        item = selected_items[0]
        values = self.employees_list.item(item, "values")
                
        self.employee_first_name_entry.delete(0, tk.END)
        self.employee_first_name_entry.insert(0, values[1])

        self.employee_last_name_entry.delete(0, tk.END)
        self.employee_last_name_entry.insert(0, values[2])

        self.employee_email_entry.delete(0, tk.END)
        self.employee_email_entry.insert(0, values[3])

    def show_statistics(self):
        """
            Отображение статистики.

            Метод берет значение проекта и формирует статисткику по нему.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.show_statistics()
        """
        try:
            project_id = int(self.analysis_project_id_entry.get()[0][0])
            result = project_statistics(self.db, project_id)

            report = (
                f"Статистика проекта {project_id}:\n\n"
                f"Всего задач: {result['total_tasks']}\n"
                f"Процент выполнения: {result['completion_rate']:.1f}%\n"
                f"Количество исполнителей: {result['employees_count']}\n"
                f"Ср. задач на исполнителя: {result['avg_tasks_per_employee']:.1f}\n"
                f"Задач в работе: {result['in_progress_ratio']:.1f}\n"
            )

            self.analysis_result.delete(1.0, tk.END)
            self.analysis_result.insert(tk.END, report)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Собрать статистику не получилось: {e}")

    def show_plot(self): # TODO подготовить тествоые данные, их подгрузку и сделать график со статусом по проектам - процент выполнения каждого проекта
        """
            Отображение графика.

            Метод берет значение проекта и формирует график процента выполнения проекта.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.show_plot()
        """
        try:
            project_id = int(self.analysis_project_id_entry.get()[0][0])
            result = project_statistics(self.db, project_id)
            plot_completion_rate(result['completion_rate'], f"Проект {project_id}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Собрать статистику не получилось: {e}")

    def save_report(self):
        """
            Сохранение отчета.

            Метод берет данные из текстового поля со статистикой и сохраняет их в текстовый файл.
            В случае ошибки при получении данных отображает сообщение об ошибке пользователю.

            Examples
            --------
            >>> app.save_report()
        """
        try:
            report = self.analysis_result.get(1.0, tk.END).strip()
            if not report:
                messagebox.showwarning("Предупреждение", "Нет данных для сохранения!")
                return

            with open("statistics.txt", "w", encoding="utf-8") as f:
                f.write(report)
            messagebox.showinfo("Успех", "Отчёт сохранён в statistics.txt!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить отчёт: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskTrackerApp(root)
    root.mainloop()