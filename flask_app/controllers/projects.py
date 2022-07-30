from wsgiref import validate
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
    invited_projects = Project.read_all_invited_to_user(participated_project_data)
    return render_template("your_projects.html",owned_projects=owned_projects,participated_projects=participated_projects,invited_projects=invited_projects)

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
    participants = User.read_all_participants_of_project(participant_data)
    versions = Version.read_all_in_project(participant_data)
    invites = User.read_all_invited_to_project(participant_data)
    return render_template("project_view.html",project=project,participants=participants,invites=invites,versions=versions)

@app.route("/projects/<int:id>/invite", methods=['POST'])
def _invite_to_project(id):
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
        return redirect(f"/projects/{id}")
    #else
    user_data = {'email':request.form['email']}
    user = User.read_one_by_email(user_data)
    if not user:
        flash("could not find user","invite")
        return redirect(f"/projects/{id}")
    invite_data = {'project_id':id,'user_id':user.id}
    if not Project.validate_invite(invite_data):
        return redirect(f"/projects/{id}")
    #else
    Project.add_invite(invite_data)
    return redirect(f"/projects/{id}")

@app.route("/projects/<int:id>/edit", methods=['POST'])
def _project_edit_submit(id):
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
        return redirect(f"/projects/{id}")
    #else
    data = {'id':id,'name':request.form['name']}
    if not Project.validate(data):
        return redirect(f"/projects/{id}")
    #else
    Project.update(data)
    return redirect(f"/projects/{id}")

@app.route("/projects/<int:id>/accept_invite")
def _project_accept_invite(id):
    if 'user_id' not in session:
        return redirect("/")
    #else
    #try to accept the invite
    data = {'user_id':session['user_id'],'project_id':id}
    Project.accept_invite(data)
    return redirect(f"/projects")

@app.route("/projects/<int:id>/decline_invite")
def _project_decline_invite(id):
    if 'user_id' not in session:
        return redirect("/")
    #else
    #try to accept the invite
    data = {'user_id':session['user_id'],'project_id':id}
    Project.delete_invite(data)
    return redirect(f"/projects")