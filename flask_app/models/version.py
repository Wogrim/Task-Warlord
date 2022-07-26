from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date
from flask_app.models.project import Project

class Version:
    schema = "task_warlord_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.project_id = data['project_id']
        self.end_date = data['end_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.project = 0
    
    @classmethod
    def read_all_in_project(cls,data):
        query = "SELECT * FROM versions WHERE project_id=%(project_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        versions = []
        for result in results:
            versions.append(cls(result))
        return versions
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM versions WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def read_one_with_project(cls,data):
        query = "SELECT * FROM versions JOIN projects ON versions.project_id=projects.id WHERE versions.id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            version = cls(results[0])
            project_data = {
                'id':results[0]['projects.id'],
                'name':results[0]['projects.name'],
                'owner_user_id':results[0]['owner_user_id'],
                'created_at':results[0]['projects.created_at'],
                'updated_at':results[0]['projects.updated_at']
            }
            version.project = Project(project_data)
            return version
        #else
        return False
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO versions (name,project_id,end_date,created_at,updated_at) VALUES (%(name)s,%(project_id)s,%(end_date)s,NOW(),NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE versions SET name=%(name)s,end_date=%(end_date)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name']) < 2 or len(data['name']) > 20:
            is_valid = False
            flash("version name must be 2-20 characters")
        #TODO: make sure the person editing is the project owner in the route
        return is_valid