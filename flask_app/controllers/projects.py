from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.project import Project
from flask_app.models.user import User
from flask_app.models.version import Version

@app.route("/projects")
def _projects():
    if 'user_id' not in session:
        return redirect("/")
    #else
    owned_project_data = {'owner_user_id':session['user_id']}
    owned_projects = Project.read_all_owned_by_user(owned_project_data)
    participated_project_data = {'user_id':session['user_id']}
    participated_projects = Project.read_all_participated_by_user(participated_project_data)
    #TODO: invited projects
    return render_template("your_projects.html",owned_projects=owned_projects,participated_projects=participated_projects)

@app.route("/projects/create")
def _create_project():
    if 'user_id' not in session:
        return redirect("/")
    #else
    data = {
        'name':"My New Project", #new project name will always be the same
        'owner_user_id':session['user_id']
    }
    project_id = Project.create(data)
    return redirect(f"/projects/{project_id}")

@app.route("/projects/<int:id>")
def _project_view(id):
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure the user is a project participant
    participant_data = {
        'project_id':id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    data = {'id':id}
    project = Project.read_one_by_id(data)
    participants_data = {'project_id':id}
    participants = User.read_all_participants_of_project(participants_data)
    versions = Version.read_all_in_project(participants_data)
    return render_template("project_view.html",project=project,participants=participants,versions=versions)
