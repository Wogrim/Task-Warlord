from ast import AsyncFunctionDef
from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.project import Project
from flask_app.models.task_group import Task_Group
from flask_app.models.task import Task

from datetime import date,timedelta

@app.route("/task_groups/<int:id>")
def _task_group_view(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #get the task group
    data = {'id':id}
    task_group = Task_Group.read_one_with_version_with_project(data)
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
    #get all the tasks for this task_group with assigned user
    task_data = {'task_group_id':id}
    tasks = Task.read_all_in_task_group_with_assigned_user(task_data)
    return render_template("task_group_view.html",task_group=task_group,tasks=tasks)

@app.route("/task_groups/<int:id>/edit",methods=['POST'])
def _task_group_edit(id):
    #make sure a user is logged in
    if 'user_id' not in session:
        return redirect("/")
    #else
    #make sure task group exists
    data = {
        'id':id,
        'name': request.form['name'],
        'start_date': request.form['start_date'],
        'end_date': request.form['end_date'],
        'progress': request.form['progress'],
        'color':request.form['color']
    }
    task_group = Task_Group.read_one_with_version_with_project(data)
    if not task_group:
        return redirect("/projects")
    #else
    #make sure this user is the owner of the project
    if session['user_id'] != task_group.version.project.owner_user_id:
        flash("only the project owner can edit this")
        return redirect(f"/versions/{task_group.version_id}")
    #else
    if not Task_Group.validate(data):
        return redirect(f"/versions/{task_group.version_id}")
    #else
    Task_Group.update(data)
    return redirect(f"/versions/{task_group.version_id}")
