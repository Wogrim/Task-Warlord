from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.project import Project
from flask_app.models.user import User
from flask_app.models.version import Version
from flask_app.models.task_group import Task_Group

from datetime import date,timedelta

@app.route("/projects/<int:id>/create_version")
def _create_version(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure project exists
    project_data = {'id':id}
    project = Project.read_one_by_id(project_data)
    if not project:
        return redirect("/projects")
    #else
    #make sure this user is the owner of this project
    if session['user_id'] != project.owner_user_id:
        flash("you must be the owner of this project to create a new version")
        return redirect(f"/projects/{id}")
    #else
    data = {
        'name':"New Version", #new version name will always be the same
        'project_id':id,
        'end_date': (date.today() + timedelta(weeks=2)).isoformat() #initially the deadline is 2 weeks from today
    }
    version_id = Version.create(data)
    return redirect(f"/versions/{version_id}")

@app.route("/versions/<int:id>")
def _version_view(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #get the version
    data = {'id':id}
    version = Version.read_one_with_project(data)
    if not version:
        return redirect("/projects")
    #make sure the user is a project participant
    participant_data = {
        'project_id':version.project_id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    #get all the task groups for this version
    data = {'version_id':id}
    task_groups = Task_Group.read_all_in_version(data)
    return render_template("version_view_EZ.html",version=version,task_groups=task_groups)

@app.route("/versions/<int:id>/create_task_group")
def _create_task_group(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure version exists
    version_data = {'id':id}
    version = Version.read_one_with_project(version_data)
    if not version:
        return redirect("/projects")
    #else
    #make sure this user is the owner of this version's project
    if session['user_id'] != version.project.owner_user_id:
        flash("you must be the owner of this version's project to create a new task group")
        return redirect(f"/versions/{id}")
    #else
    data = {
        'name':"New Task Group", #new task group always made with preset values
        'version_id':id,
        'start_date': date.today().isoformat(),
        'end_date': version.end_date.isoformat() if date.today() < version.end_date else (date.today()+timedelta(weeks=1)).isoformat(),
        'progress': 0,
        'color':"#d5e8d4"
    }
    task_group_id = Task_Group.create(data)
    return redirect(f"/versions/{id}")