from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.project import Project
from flask_app.models.task_group import Task_Group
from flask_app.models.task import Task
from flask_app.models.user import User

from datetime import date,timedelta


@app.route("/task_groups/<int:id>/create_task")
def _create_task(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure task group exists
    task_group_data = {'id':id}
    task_group = Task_Group.read_one_with_version_with_project(task_group_data)
    if not task_group:
        return redirect("/projects")
    #else
    #make sure the user is a project participant
    participant_data = {
        'project_id':task_group.version.project_id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    participants = User.read_all_participants_of_project(participant_data)
    return render_template("create_task.html",task_group=task_group,participants=participants)

@app.route("/task_groups/<int:id>/create_task/submit", methods=['POST'])
def _create_task_submit(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure task group exists
    task_group_data = {'id':id}
    task_group = Task_Group.read_one_with_version_with_project(task_group_data)
    if not task_group:
        return redirect("/projects")
    #else
    #make sure the user is a project participant
    participant_data = {
        'project_id':task_group.version.project_id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    #validate form data
    data = {
        'title':request.form['title'],
        'task_group_id':id,
        'priority':request.form['priority'],
        'assigned_user_id':request.form['assigned_user_id'],
        'status':request.form['status'],
        'progress':request.form['progress'],
        'description':request.form['description'],
        
    }
    if not Task.validate(data):
        return redirect(f"/task_groups/{id}/create_task")
    #else
    Task.create(data)
    return redirect(f"/task_groups/{id}")

@app.route("/tasks/<int:id>")
def _edit_task(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure task exists
    task_data = {'id':id}
    task = Task.read_one_with_assigned_user(task_data)
    if not task:
        return redirect("/projects")
    #else
    #make sure the user is a project participant
    task_group_data = {'id':task.task_group_id}
    task_group = Task_Group.read_one_with_version_with_project(task_group_data)
    participant_data = {
        'project_id':task_group.version.project_id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    participants = User.read_all_participants_of_project(participant_data)
    print(task.progress)
    return render_template("task_view.html",task_group=task_group,participants=participants,task=task)

@app.route("/tasks/<int:id>/submit", methods=['POST'])
def _edit_task_submit(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure task exists
    task_data = {'id':id}
    task = Task.read_one_with_assigned_user(task_data)
    if not task:
        return redirect("/projects")
    #else
    #make sure the user is a project participant
    task_group_data = {'id':task.task_group_id}
    task_group = Task_Group.read_one_with_version_with_project(task_group_data)
    participant_data = {
        'project_id':task_group.version.project_id,
        'user_id':session['user_id']
    }
    if not Project.is_participant(participant_data):
        return redirect("/projects")
    #else
    #validate form data
    data = {
        'title':request.form['title'],
        'priority':request.form['priority'],
        'assigned_user_id':request.form['assigned_user_id'],
        'status':request.form['status'],
        'progress':request.form['progress'],
        'description':request.form['description'],
        'id':id
    }
    if not Task.validate(data):
        return redirect(f"/tasks/{task.id}")
    #else
    Task.update(data)
    return redirect(f"/task_groups/{task.task_group_id}")
