import time

class Task:
    def __init__(self, name, discription, project=None, employee=None, status='todo', created_at=time.time(), updated_at=None):
        self.name = name
        self.discription = discription
        self.project = project
        self.status = "todo" # todo, in progress, done 
        self.employee = employee
        self.created_at = time.time()
    
    def __repr__(self):
        return f"<Задача {self.name}: {self.discription} [{self.status}] {self.project} {self.employee} {self.created_at}>"

class Employee:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):
        return f"<Сотрудник {self.first_name}: {self.last_name} <{self.email}>"
    
class Project:
    def __init__(self, name, status='New', created_at=time.time(), updatetd_at=None):
        self.name = name
        self.status = status
        self.created_at = time.time()

    def __repr__(self):
        return f"<Проект {self.name}: {self.status}"
    
