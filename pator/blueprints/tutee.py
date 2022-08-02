from ast import Not
from unicodedata import category
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from pator.blueprints.auth import login_required
from pator.db import get_db

bp = Blueprint('tutee', __name__, url_prefix='/tutee')
# bp_create = Blueprint('create', __name__, url_prefix='/create')

# bp.register_blueprint(bp_create)

# Work in progress
@bp.route('/category', defaults={'name': None})
@bp.route('/category/<name>', methods=(['GET']))
def category(name):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    category_name = f"%{name}%"

    cursor.execute(
        '''
        SELECT * FROM course c
        INNER JOIN course_tutor cp ON (c.id = cp.course_id)
        INNER JOIN tutor t ON (cp.tutor_id = t.id)
        INNER JOIN user u ON (t.user_id = u.id)
        WHERE c.course_prodi LIKE %s
        ''',
        (category_name,)
    )

    datas = cursor.fetchall()

    if datas is not None:
        return render_template('tutee/menu.html', datas=datas)
    else:
        return render_template('tutee/menu.html')
