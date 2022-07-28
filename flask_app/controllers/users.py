from flask_app import app, bcrypt

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User


@app.route("/")
def _login_registration():
    if 'user_id' in session:
        return redirect("/projects")
    #else
    return render_template("login_registration.html")

@app.route("/logout")
def _logout():
    if 'user_id' in session:
        del session['user_id']
    return redirect("/")

@app.route("/register", methods=['POST'])
def _register():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
        'confirm_password': request.form['confirm_password']
    }
    if not User.validate(data):
        return redirect("/")
    #else
    data['password'] = bcrypt.generate_password_hash(data['password'])
    id = User.create(data)
    session['user_id'] = id
    return redirect("/projects")

login_fail_message = "email and/or password incorrect"

@app.route("/login", methods=['POST'])
def _login():
    data = {
        'email': request.form['email']
    }

    user = User.read_one_by_email(data)
    if not user:
        flash(login_fail_message,'login')
        return redirect("/")
    #else
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(login_fail_message,'login')
        return redirect("/")
    #else

    session['user_id'] = user.id
    return redirect("/projects")