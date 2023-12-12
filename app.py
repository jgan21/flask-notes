import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql:///hashing_login")
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)

@app.get('/')
def redirect_to_register():
    """Redirect root url to '/resiter'"""

    return redirect('/register')

@app.route('/register', methods = ["GET", "POST"])
def show_register_user():
    """Renders the create user form"""

    return render_template('register-user-form.html')