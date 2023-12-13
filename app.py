import os

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import connect_db, db, User
from forms import RegisterUserForm, LoginUserForm, CSRFProtectForm

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
def register_user():
    """Register user: produce form and handle form submission"""

    form = RegisterUserForm()
    errs = []

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # TODO: maybe we should split this into a different function?
        # Could also hide this logic in the register method of the User class
        # Keep the flash in the route
        if User.query.get(username):
            errs.append("This username exists, please enter a new username.")

        if User.query.get(email):
            errs.append("This email exists, please enter a different email.")

        if errs:
            for err in errs:
                flash(err)
            return render_template('register-user-form.html',
                               first_name=first_name,
                               last_name=last_name)

        user = User.register(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        return redirect(f"/users/{user.username}")

    return render_template('register-user-form.html', form=form)


@app.route('/login', methods = ["GET", "POST"])
def login_user():
    """Login user: produce form and handle form submission"""

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        # TODO: Make this more specific to false?
        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login-form.html', form=form)


@app.get("/users/<username>")
def show_user_page(username):
    """Authenticate user and display user page with information about user,
    if invalid user, return redirect to homepage.
    """

    if username != session.get("username"):
        return redirect("/")

    form = CSRFProtectForm()

    user = User.query.get_or_404(username)
    return render_template("user-page.html", form=form, user=user)


@app.post("/logout")
def logout_user():
    """Logs user our and redirects to homepage."""

    form = CSRFProtectForm()
    # breakpoint()

    if form.validate_on_submit():
        session.pop("username", None)
        # print("session=", session["username"])

    return redirect("/")


