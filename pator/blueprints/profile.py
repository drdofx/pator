from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from jinja2 import TemplateNotFound
from werkzeug.exceptions import abort

from pator.blueprints.auth import login_required
from pator.db import get_db

bp = Blueprint('profile', __name__, url_prefix='/profile')

@bp.route('/', methods=['GET'])
def index():
    try:
        user_id = g.user['id']

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute('SELECT id, self_description FROM tutor WHERE user_id = %s', (user_id,)) 

        tutor = cursor.fetchone()

        return render_template('profile/index.html', tutor=tutor)
    except TemplateNotFound:
        abort(404)

@bp.route('/edit', methods=['POST'])
def edit():
    self_description = request.form.get('self_description', None)
    tutor_id = request.form.get('tutor_id', None)

    db = get_db()
    cursor = db.cursor(dictionary=True)
    error = None

    if None in (self_description, tutor_id):
        error = "Please check you request data."

    if error is None:
        cursor.execute(
            '''
            UPDATE tutor
            SET self_description = %s
            WHERE id = %s
            ''',
            (self_description, tutor_id,)
        )

        flash("Profile has been updated!", "success")
        return redirect(url_for("profile.index"))

    abort(400)