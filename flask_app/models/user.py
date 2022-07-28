from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    schema = "task_warlord_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def read_one_by_email(cls,data):
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def read_all_participants_of_project(cls,data):
        query = "SELECT * FROM users JOIN users_participate_projects ON users.id=users_participate_projects.user_id WHERE project_id=%(project_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        users = []
        for result in results:
            users.append(cls(result))
        return users

    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    # validate to be used before creating and editing a user account
    @classmethod
    def validate(cls,data):
        is_valid = True
        if len(data['first_name']) < 2 or len(data['first_name']) > 45:
            is_valid = False
            flash("first name must be 2 to 45 characters long","registration")
        if len(data['last_name']) < 2 or len(data['last_name']) > 45:
            is_valid = False
            flash("last name must be 2 to 45 characters long","registration")
        if cls.read_one_by_email(data):
            is_valid = False
            flash("there is already an account for this email","registration")
        if not EMAIL_REGEX.match(data['email']):
            is_valid = False
            flash("incorrect email format","registration")
        if len(data['email']) > 255:
            is_valid = False
            flash("email too long (255 characters max)","registration")
        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash("passwords do not match","registration")
        if len(data['password']) < 8:
            is_valid = False
            flash("password must be at least 8 characters long","registration")
        return is_valid