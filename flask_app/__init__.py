from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "99a8u9efua24624dgfh0U8F09UGF29JFSI278h2yfij"

bcrypt = Bcrypt(app)