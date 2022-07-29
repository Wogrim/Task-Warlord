from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.user import User

class Task:
    schema = "task_warlord_schema"

    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.task_group_id = data['task_group_id']
        self.priority = data['priority']
        self.assigned_user_id = data['assigned_user_id']
        self.status = data['status']
        self.progress = data['progress']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.assigned_user = 0
    
    @classmethod
    def read_all_in_task_group_with_assigned_user(cls,data):
        query = "SELECT * FROM tasks LEFT JOIN users ON tasks.assigned_user_id=users.id WHERE task_group_id=%(task_group_id)s ORDER BY priority DESC;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        tasks = []
        for result in results:
            task = cls(result)
            user_data = {
                'id':result['users.id'],
                'first_name':result['first_name'],
                'last_name':result['last_name'],
                'email':result['email'],
                'password':result['password'],
                'created_at':result['users.created_at'],
                'updated_at':result['users.updated_at'],
            }
            task.assigned_user = User(user_data)
            tasks.append(task)
        return tasks

    @classmethod
    def read_one_with_assigned_user(cls,data):
        query = "SELECT * FROM tasks LEFT JOIN users ON tasks.assigned_user_id=users.id WHERE tasks.id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        task = cls(results[0])
        user_data = {
            'id':results[0]['users.id'],
            'first_name':results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        task.assigned_user = User(user_data)
        return task
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM tasks WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def create(cls,data):
        if data['assigned_user_id'] != "0":
            query = "INSERT INTO tasks (title,task_group_id,priority,assigned_user_id,status,progress,description,created_at,updated_at) VALUES (%(title)s,%(task_group_id)s,%(priority)s,%(assigned_user_id)s,%(status)s,%(progress)s,%(description)s,NOW(),NOW());"
        else:
            query = "INSERT INTO tasks (title,task_group_id,priority,assigned_user_id,status,progress,description,created_at,updated_at) VALUES (%(title)s,%(task_group_id)s,%(priority)s,NULL,%(status)s,%(progress)s,%(description)s,NOW(),NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        if data['assigned_user_id'] != "0":
            query = "UPDATE tasks SET title=%(title)s,priority=%(priority)s,assigned_user_id=%(assigned_user_id)s,status=%(status)s,progress=%(progress)s,description=%(description)s,updated_at=NOW() WHERE id=%(id)s;"
        else:
            query = "UPDATE tasks SET title=%(title)s,priority=%(priority)s,assigned_user_id=NULL,status=%(status)s,progress=%(progress)s,description=%(description)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['title']) < 3 or len(data['title'])>255:
            is_valid = False
            flash("title must be 3-255 characters")
        priority = int(data['priority'])
        if priority < 1 or priority > 4:
            is_valid = False
            flash("invalid priority")
        status = int(data['status'])
        if status < 1 or status > 5:
            is_valid = False
            flash("invalid status")
        if len(data['description'])>2500:
            is_valid = False
            flash("description max length is 2500 characters")
        progress = int(data['progress'])
        if progress < 0 or progress > 100:
            is_valid = False
            flash("progress must be from 0 to 100")
        #TODO: make sure the assigned user is a participant in the project
        return is_valid