import psycopg2
from psycopg2.extras import RealDictCursor
import re
from model import Project, Task, Employee

class Database:
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
        try:
            return psycopg2.connect(**self.connection_params)
        except psycopg2.OperationalError as e:
            raise ConnectionError(f"Не удалось подключиться к БД: {e}")
    
    def init_db(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS projects (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        status VARCHAR(20) DEFAULT 'active'
                            CHECK (status IN ('Active', 'Done', 'Canceled')),
                        created_at INTEGER not NULL,
                        updatetd_at INTEGER
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
                        updatetd_at INTEGER
                    );
                """)
            conn.commit()

    def get_tasks(self):
        """Получить все задачи."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT t.id, t.name, e.first_name || ' ' || e.last_name, p.name AS project_name, t. status
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
        """Добавить задачу в БД."""
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
        
    def get_projects(self):
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
        
    def get_employees(self):
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
        
    def delete_task(self, row_id):
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