from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date
from flask import flash
from flask_app.models.version import Version
from flask_app.models.project import Project

class Task_Group:
    schema = "task_warlord_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.version_id = data['version_id']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
        self.progress = data['progress']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.version = 0
    
    @classmethod
    def read_all_in_version(cls,data):
        query = "SELECT * FROM task_groups WHERE version_id=%(version_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        task_groups = []
        for result in results:
            task_groups.append(cls(result))
        return task_groups
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM task_groups WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def read_one_with_version_with_project(cls,data):
        query = "SELECT * FROM task_groups JOIN versions ON task_groups.version_id=versions.id JOIN projects ON versions.project_id=projects.id WHERE task_groups.id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        if len(results) > 0:
            task_group = cls(results[0])
            version_data = {
                'id':results[0]['versions.id'],
                'name':results[0]['versions.name'],
                'project_id':results[0]['project_id'],
                'end_date':results[0]['versions.end_date'],
                'created_at':results[0]['versions.created_at'],
                'updated_at':results[0]['versions.updated_at'],
            }
            task_group.version = Version(version_data)
            project_data = {
                'id':results[0]['projects.id'],
                'name':results[0]['projects.name'],
                'owner_user_id':results[0]['owner_user_id'],
                'created_at':results[0]['projects.created_at'],
                'updated_at':results[0]['projects.updated_at']
            }
            task_group.version.project = Project(project_data)
            return task_group
        #else
        return False
    
    @classmethod
    def create(cls,data):
        query = "INSERT INTO task_groups (name,version_id,start_date,end_date,progress,color,created_at,updated_at) VALUES (%(name)s,%(version_id)s,%(start_date)s,%(end_date)s,%(progress)s,%(color)s,NOW(),NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE task_groups SET name=%(name)s,start_date=%(start_date)s,end_date=%(end_date)s,progress=%(progress)s,color=%(color)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    @classmethod
    def validate(cls,data):
        is_valid = True
        date_start = date.fromisoformat(data['start_date'])
        date_end = date.fromisoformat(data['end_date'])
        if date_end < date_start:
            is_valid = False
            flash("end date can't be before start date")
        if len(data['name']) < 3 or len(data['name'])>45:
            is_valid = False
            flash("task group name must be 3-45 characters")
        progress = int(data['progress'])
        if progress < 0 or progress > 100:
            is_valid = False
            flash("progress must be from 0 to 100")
        return is_valid