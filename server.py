from flask_app import app

from flask_app.controllers import users
from flask_app.controllers import projects
from flask_app.controllers import versions
from flask_app.controllers import task_groups
# from flask_app.controllers import tasks



if __name__ == "__main__":
    app.run(debug=True)
