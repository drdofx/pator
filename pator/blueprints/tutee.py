from ast import Not
from unicodedata import category
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from pator.blueprints.auth import login_required
from pator.db import get_db

bp = Blueprint('course', __name__, url_prefix='/course')
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
        SELECT c.course_name, c.course_prodi, cp.course_rating, cp.hourly_fee, cp.id AS course_tutor_id, u.name
        FROM course c
        INNER JOIN course_tutor cp ON (c.id = cp.course_id)
        INNER JOIN tutor t ON (cp.tutor_id = t.id)
        INNER JOIN user u ON (t.user_id = u.id)
        WHERE c.course_prodi LIKE %s
        ''',
        (category_name,)
    )

    datas = cursor.fetchall()

    if datas is not None:
        return render_template('tutee/list.html', datas=datas)
    else:
        return render_template('tutee/list.html')


@bp.route('/detail', defaults={'id': None})
@bp.route('/detail/<int:id>', methods=(['GET']))
def detail(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)


    # TODO: Add more inner join to tables course_tutor_keyword and tutor_session_review
    cursor.execute(
        '''
        SELECT c.course_name, c.course_prodi, cp.course_rating, cp.hourly_fee, cp.id AS course_tutor_id, u.name,
        cp.course_description, t.self_description
        FROM course_tutor cp
        INNER JOIN course c ON (cp.course_id = c.id)
        INNER JOIN tutor t ON (cp.tutor_id = t.id)
        INNER JOIN user u ON (t.user_id = u.id)
        WHERE cp.id = %s
        ''',
        (id,)
    )

    data = cursor.fetchone()

    if data is not None:
        return render_template('tutee/detail.html', data=data)
    
    abort(404)