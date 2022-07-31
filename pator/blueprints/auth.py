import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from jinja2 import TemplateNotFound

from werkzeug.security import check_password_hash, generate_password_hash

from pator.db import get_db

from mysql.connector import IntegrityError

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    # print(dir(request))
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        nim = request.form.get('nim', None)
        name = request.form.get('name', None)
        email = request.form.get('email', None)
        prodi = request.form.get('prodi', None)
        angkatan = request.form.get('angkatan', None)

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        if None in (nim, username, password, name, email, prodi, angkatan):
            error = "Please check you request data."

        print(error)

        if error is None:
            try:
                data = (nim, username, generate_password_hash(password), name, email, prodi, angkatan)
                cursor.execute(
                    '''INSERT INTO user
                    (NIM, username, password, name, email, prodi, angkatan)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                    data,
                )
            except IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.register"))

        flash(error)

    try:
        return render_template('auth/register.html')
    except TemplateNotFound:
        abort(404)

# work in progress
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        if '@' in username:
            cursor.execute(
                "SELECT * FROM user WHERE email = %s", (username,)
            )
        else:
            cursor.execute(
                "SELECT * FROM user WHERE username = %s", (username,)
            )

        user = cursor.fetchone()

        print(user)

        if user is None:
            error = "Incorrect username or email."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('hello'))

        flash(error)

    try:
        return render_template('auth/login.html')
    except TemplateNotFound:
        abort(404)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user WHERE id = %s", (user_id,)
        )
        g.user = cursor.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))

def get_user():
    return g.user

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view