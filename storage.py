import psycopg2

class Database:
    """
        Класс для работы с базой данных PostgreSQL.

        Parameters
        ----------------------
        host : str
            Хост базы данных (по умолчанию "localhost")
        port : int
            Порт подключения (по умолчанию 5432)
        dbname : str
            Имя базы данных (по умолчанию "final_certification")
        user : str
            Пользователь БД (по умолчанию "postgres")
        password : str
            Пароль пользователя (по умолчанию "postgres")
    """
    def __init__(self, host="localhost", port=5432, dbname="final_certification", 
                 user="postgres", password="postgres"):
        self.connection_params = {
            'host': host,
            'port': port,
            'dbname': dbname,
            'user': user,
            'password': password
        }
        self.init_db()

    def get_connection(self):
        """
            Получение подключения к базе данных.

            Returns
            ----------
            psycopg2.connection
                Объект подключения к БД

            Raises
            --------
            ConnectionError
                Если не удалось установить соединение

            Examples
            --------
            >>> db = Database()
            >>> conn = db.get_connection()
        """
        try:
            return psycopg2.connect(**self.connection_params)
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Не удалось подключиться к БД: {e}")
    
    def init_db(self):
        """
            Создание таблиц базы данных, если они не были созданы ранее

            Examples
            --------
            >>> app.init_db()
        """
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        status VARCHAR(20) DEFAULT 'Active'
                            CHECK (status IN ('Active', 'Done', 'Canceled')),
                        created_at INTEGER not NULL,
                        updated_at INTEGER
                    );
                """)
                
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS employees (
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(100) NOT NULL,
                        last_name VARCHAR(100) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL
                            CHECK (email ~* '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                    );
                """)
                
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        discription VARCHAR(255),
                        project_id INTEGER NOT NULL,
                        employee_id INTEGER,
                        status VARCHAR(20) DEFAULT 'todo'
                            CHECK (status IN ('todo', 'in_progress', 'done')),
                        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                        FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE SET NULL,
                        created_at INTEGER NOT NULL,
                        updated_at INTEGER
                    );
                """)
            conn.commit()

    def get_tasks(self):
        """
        Получение всех задач из базы данных.

        Returns
        ----------
        list of tuples
            Список кортежей с данными задач:
            (id, name, description, employee_name, project_name, status)

        Raises
        --------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> tasks = db.get_tasks()
        >>> tasks[0]
        (1, 'Задача 1', 'Описание задачи', 'Иван Петров', 'Проект X', 'todo')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT t.id, t.name, t.discription, e.first_name || ' ' || e.last_name, p.name AS project_name, t. status
                        FROM tasks t
                        JOIN projects p ON t.project_id = p.id
                        JOIN employees e ON t.employee_id = e.id
                        ORDER BY t.id
                    """)
                    rows = cur.fetchall()
                    return rows
        except Exception as e:
            raise Exception(f"Ошибка при получении задач: {e}")
        
    def add_task(self, task):
        """
        Добавление новой задачи в базу данных.

        Parameters
        ----------
        task : dict
            Словарь с данными задачи:
            - name (str): название задачи
            - discription (str): описание
            - project_id (int): ID проекта
            - employee_id (int): ID исполнителя
            - status (str): статус задачи
            - created_at (int): дата создания

        Raises
        --------
        ValueError
            При нарушении целостности данных
        Exception
            При других ошибках

        Examples
        --------
        >>> db = Database()
        >>> task = {
                'name': 'Новая задача',
                'discription': 'Описание новой задачи',
                'project_id': 1,
                'employee_id': 1,
                'status': 'todo',
                'created_at': int(time.time())
        }
        >>> db.add_task(task)
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO tasks 
                        (name, discription, project_id, employee_id, status, created_at)
                        VALUES (%s, %s, %s, %s, %s, %s)""",
                        (task.name, task.discription, task.project,
                         task.employee, task.status, task.created_at)
                    )
                conn.commit()
        except psycopg2.IntegrityError as e:
            if 'ограничение внешнего ключа' in str(e).lower():
                raise ValueError("Указанный проект или исполнитель не существует")
            else:
                raise ValueError(f"Ошибка при добавлении задачи: {e}")
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def edit_task(self, row_id, task_name, task_discription, task_project, task_employee, task_status, updated_at):
        """
        Добавление новой задачи в базу данных.

        Parameters
        ----------
        row_id : int
            ID задачи для редактирования
        task_name : str
            Новое название задачи
        task_discription : str
            Новое описание задачи
        task_project : int
            ID проекта, к которому относится задача
        task_employee : int
            ID исполнителя задачи
        task_status : str
            Новый статус задачи (должен быть одним из: 'todo', 'in_progress', 'done')
        updated_at : int
            Временная метка обновления

        Raises
        --------
        ValueError
            Если указан несуществующий проект или исполнитель
        Exception
            При других ошибках выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> db.edit_task(1, Обновленное название', 'Новое описание', 2, 3, 'in_progress', int(time.time()))
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """UPDATE tasks 
                        set name = %s, discription = %s, project_id = %s, employee_id = %s, status = %s, updated_at = %s
                        WHERE id = %s""",
                        (task_name, task_discription, task_project, task_employee, task_status, updated_at, row_id)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def get_projects(self):
        """
        Получить список всех проектов из базы данных.

        Returns
        -------
        list of tuples
            Список кортежей с данными проектов:
                (id, name, status)

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> projects = db.get_projects()
        >>> projects[0]
        (1, 'Проект 1', 'Active')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT p.id, p.name, p.status
                        FROM projects p
                        ORDER BY p.id
                    """)
                    rows = cur.fetchall()
                    return rows
        except Exception as e:
            raise Exception(f"Ошибка при получении задач: {e}")
        
    def add_project(self, project):
        """
        Добавить новый проект в базу данных.

        Parameters
        ----------
        project : dict
            Словарь с данными проекта:
                - name (str): название проекта
                - status (str): статус проекта ('Active', 'Done', 'Canceled')
                - created_at (int): временная метка создания

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> project = {
                'name': 'Новый проект',
                'status': 'Active',
                'created_at': int(time.time())
        }
        >>> db.add_project(project)
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO projects 
                        (name, status, created_at)
                        VALUES (%s, %s, %s)""",
                        (project.name, project.status, project.created_at)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def edit_project(self, row_id, project_name, project_status, updated_at):
        """
        Редактировать существующий проект.

        Parameters
        ----------
        row_id : int
            ID сотрудника для редактирования
        project_name : str
            Новое название проекта
        project_status : str
            Навый статус проекта
        updated_at : str
            Дата обновления

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> db.edit_employee(1, 'Проект 11', 'Active', '1767788811')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """UPDATE projects 
                        set name = %s, status = %s, updated_at = %s
                        WHERE id = %s""",
                        (project_name, project_status, updated_at, row_id)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def get_employees(self):
        """
        Получить список всех сотрудников из базы данных.

        Parameters
        ----------
        list of tuples
            Список кортежей с данными сотрудников:
                (id, first_name, last_name, email)

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> employees = db.get_employees()
        >>> employees[0]
        (1, 'Иван', 'Иванов', 'ivan@example.com')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT e.id, e.first_name, e.last_name, e.email
                        FROM employees e
                        ORDER BY e.id
                    """)
                    rows = cur.fetchall()
                    return rows
        except Exception as e:
            raise Exception(f"Ошибка при получении задач: {e}")
        
    def add_employee(self, employee):
        """
        Добавить нового сотрудника в базу данных.

        Parameters
        ----------
        employee : dict
            Словарь с данными сотрудника:
                - first_name (str): имя сотрудника
                - last_name (str): фамилия сотрудника
                - email (str): email сотрудника (должен быть уникальным)

        Raises
        ------
        ValueError
            Если email уже существует в базе данных
        Exception
            При других ошибках выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> employee = {
                'first_name': 'Петр',
                'last_name': 'Петров',
                'email': 'petr@example.com'
            }
        >>> db.add_employee(employee)
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """INSERT INTO employees 
                        (first_name, last_name, email)
                        VALUES (%s, %s, %s)""",
                        (employee.first_name, employee.last_name, employee.email)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def edit_employee(self, row_id, employee_first_name, employee_last_name, employee_email):
        """
        Редактировать существующего сотрудника.

        Parameters
        ----------
        row_id : int
            ID сотрудника для редактирования
        first_name : str
            Новое имя сотрудника
        last_name : str
            Новая фамилия сотрудника
        email : str
            Новый email сотрудника (должен быть уникальным)

        Raises
        ------
        ValueError
            Если email уже существует в базе данных
        Exception
            При других ошибках выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> db.edit_employee(1, 'Обновленное имя', 'Обновленная фамилия', 'new_email@example.com')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """UPDATE employees 
                        set first_name = %s, last_name = %s, email = %s
                        WHERE id = %s""",
                        (employee_first_name, employee_last_name, employee_email, row_id)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def delete_task(self, row_id):
        """
        Удалить задачу из базы данных.

        Parameters
        ----------
        row_id : int
            ID задачи для удаления

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> db.delete_task(1)  # Удаление задачи с ID 1
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """DELETE from tasks 
                        WHERE id=%s""", (row_id,)
                    )
                conn.commit()
        except Exception as e:
            raise Exception(f"Неизвестная ошибка: {e}")
        
    def get_tasks_for_statistics(self):
        """
        Получить данные задач для статистического анализа.

        Returns
        -------
        list of tuples
            Список кортежей с данными:
                (task_id, task_name, discription, employee_id, 
                employee_first_name, employee_last_name, 
                project_name, project_id, status)

        Raises
        ------
        Exception
            При ошибке выполнения запроса

        Examples
        --------
        >>> db = Database()
        >>> stats_data = db.get_tasks_for_statistics()
        >>> stats_data[0]
        (1, 'Задача 1', 'Описание', 1, 'Иван', 'Иванов', 'Проект 1', 1, 'todo')
        """
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT t.id, t.name, t.discription, e.id, e.first_name, e.last_name, p.name, p.id, t.status
                        FROM tasks t
                        JOIN projects p ON t.project_id = p.id
                        JOIN employees e ON t.employee_id = e.id
                        ORDER BY t.id
                    """)
                    rows = cur.fetchall()
                    return rows
        except Exception as e:
            raise Exception(f"Ошибка при получении задач: {e}")