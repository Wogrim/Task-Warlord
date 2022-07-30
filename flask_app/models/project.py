from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

import re
#not used
NAME_REGEX = re.compile(r"^[a-zA-Z0-9_. -]+$")

class Project:
    schema = "task_warlord_schema"

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.owner_user_id = data['owner_user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def read_one_by_id(cls,data):
        query = "SELECT * FROM projects WHERE id=%(id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data);
        if len(results) > 0:
            return cls(results[0])
        #else
        return False
    
    @classmethod
    def add_participant(cls,data):
        query = "INSERT INTO users_participate_projects (project_id,user_id,created_at) VALUES (%(project_id)s,%(user_id)s,NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def add_invite(cls,data):
        query = "INSERT INTO projects_invite_users (project_id,user_id,created_at) VALUES (%(project_id)s,%(user_id)s,NOW());"
        return connectToMySQL(cls.schema).query_db(query,data)

    @classmethod
    def create(cls,data):
        query = "INSERT INTO projects (name,owner_user_id,created_at,updated_at) VALUES (%(name)s,%(owner_user_id)s,NOW(),NOW());"
        project_id = connectToMySQL(cls.schema).query_db(query,data)
        participant_data = {'project_id':project_id, 'user_id':data['owner_user_id']}
        cls.add_participant(participant_data)
        return project_id
    
    @classmethod
    def read_all_owned_by_user(cls,data):
        query = "SELECT * FROM projects WHERE owner_user_id=%(owner_user_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        projects = []
        for result in results:
            projects.append(cls(result))
        return projects
    
    @classmethod
    def read_all_participated_by_user(cls,data):
        query = "SELECT * FROM projects JOIN users_participate_projects ON projects.id=users_participate_projects.project_id WHERE users_participate_projects.user_id=%(user_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        projects = []
        for result in results:
            projects.append(cls(result))
        return projects
    
    @classmethod
    def read_all_invited_to_user(cls,data):
        query = "SELECT * FROM projects JOIN projects_invite_users ON projects.id=projects_invite_users.project_id WHERE projects_invite_users.user_id=%(user_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        projects = []
        for result in results:
            projects.append(cls(result))
        return projects
    
    # update primarily to change the name of the project, but perhaps transfer ownership later
    @classmethod
    def update(cls,data):
        query = "UPDATE projects SET name=%(name)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.schema).query_db(query,data)
    
    # validate to be used before creating and updating a project
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['name']) < 5 or len(data['name']) > 45:
            is_valid = False
            flash("project name must be 5 to 45 characters long")
        return is_valid
    
    # invite_user will invite a specified user to the specified project
    @classmethod
    def invite_user(cls,data):
        query = "INSERT INTO projects_invite_users (project_id,user_id,created_at) VALUES (%(project_id)s,%(user_id)s,NOW());"
        connectToMySQL(cls.schema).query_db(query,data)
        return
    
    @classmethod
    def is_participant(cls,data):
        query = "SELECT * FROM users_participate_projects WHERE project_id=%(project_id)s AND user_id=%(user_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        return len(results)>0
    
    @classmethod
    def is_invited(cls,data):
        query = "SELECT * FROM projects_invite_users WHERE project_id=%(project_id)s AND user_id=%(user_id)s;"
        results = connectToMySQL(cls.schema).query_db(query,data)
        return len(results)>0

    @classmethod
    def delete_invite(cls,data):
        query = "DELETE FROM projects_invite_users WHERE project_id=%(project_id)s AND user_id=%(user_id)s;"
        connectToMySQL(cls.schema).query_db(query,data)
        return
    
    @classmethod
    def accept_invite(cls,data):
        if not cls.is_invited(data):
            flash("this invite does not exist")
            return False
        #else
        cls.delete_invite(data)
        cls.add_participant(data)
        return True

    # validate invite before it is sent
    # expects project_id, invitee's email, sender's user_id
    @classmethod
    def validate_invite(cls,data):
        is_valid = True
        #make sure the project exists
        project_data = {'id':data['project_id']}
        project = cls.read_one_by_id(project_data)
        if not project:
            is_valid = False
            flash("project does not exist","invite")
        #make sure the invited person exists
        user_data = {'id':data['user_id']}
        user_x = user.User.read_one_by_id(user_data)
        if user_x:
            #make sure the invited person isn't already a project participant or already pending invite
            participant_data = {'project_id':data['project_id'],'user_id':user_x.id}
            if cls.is_participant(participant_data):
                is_valid = False
                flash("that user is already a participant in this project","invite")
            elif cls.is_invited(participant_data):
                is_valid = False
                flash("that user already has a pending invite to this project","invite")
        else:
            is_valid = False
            flash("could not find specified user","invite")
        return is_valid