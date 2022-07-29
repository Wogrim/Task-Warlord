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
