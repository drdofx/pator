from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from jinja2 import TemplateNotFound
from werkzeug.exceptions import abort

from pator.blueprints.auth import login_required
from pator.db import get_db

bp = Blueprint('course', __name__, url_prefix='/course')
# bp_create = Blueprint('create', __name__, url_prefix='/create')

# bp.register_blueprint(bp_create)

def get_courses(query=None, type='category'):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    #  if query is None, return every course
    if query is None:
        cursor.execute(
            '''
            SELECT c.course_name, c.course_prodi, cp.course_rating, cp.hourly_fee, cp.id AS course_tutor_id, u.name
            FROM course c
            INNER JOIN course_tutor cp ON (c.id = cp.course_id)
            INNER JOIN tutor t ON (cp.tutor_id = t.id)
            INNER JOIN user u ON (t.user_id = u.id)
            '''
        )
        
        datas = cursor.fetchall()

        return datas

    # if query is not none, execute query statement based on type
    if type == "category":
        category_name = f"%{query}%"

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
    elif type == "search":
        search_query = f"%{query}%"

        cursor.execute(
            '''
            SELECT c.course_name, c.course_prodi, cp.course_rating, cp.hourly_fee, cp.id AS course_tutor_id, u.name
            FROM course c
            INNER JOIN course_tutor cp ON (c.id = cp.course_id)
            INNER JOIN tutor t ON (cp.tutor_id = t.id)
            INNER JOIN user u ON (t.user_id = u.id)
            WHERE c.course_name LIKE %s 
            OR u.name LIKE %s
            ''',
            (search_query, search_query,)
        )

    datas = cursor.fetchall()

    return datas


@bp.route('/category', defaults={'name': None})
@bp.route('/category/<name>', methods=(['GET']))
def category(name):
    datas = get_courses(name, "category")

    if name is not None:
        return render_template('tutee/list.html', datas=datas, category=name.title())
    else:
        return render_template('tutee/list.html', datas=datas)

@bp.route('/search', methods=(['GET']))
def search():
    query = request.args.get('query')
    
    datas = get_courses(query, "search")

    if query is not None:
        return render_template('tutee/list.html', datas=datas, category=query.title())
    else:
        return render_template('tutee/list.html', datas=datas)


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

@bp.route('/payment', defaults={'id': None})
@bp.route('/payment/<int:id>', methods=('GET', 'POST'))
@login_required
def payment(id):
    if id is None:
        return redirect(request.referrer)

    if request.method == 'GET':
        hours = request.args.get('hours')

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute(
            '''
            SELECT c.course_name, c.course_prodi, cp.course_rating, cp.hourly_fee, cp.id AS course_tutor_id, u.name, u.id
            FROM course_tutor cp
            INNER JOIN course c ON (cp.course_id = c.id)
            INNER JOIN tutor t ON (cp.tutor_id = t.id)
            INNER JOIN user u ON (t.user_id = u.id)
            WHERE cp.id = %s
            ''',
            (id,)
        )

        data = cursor.fetchone()

        data['total_fee'] = data['hourly_fee'] * int(hours)

        if data is not None:
            return render_template('tutee/payment.html', data=data)
    
        abort(400)

    elif request.method == 'POST':
        course_tutor_id = request.form.get('course_tutor_id', None)
        tutor_id = request.form.get('tutor_id', None)
        user_id = g.user['id']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        if None in (course_tutor_id, tutor_id):
            error = "Please check you request data."

        if error is None:
            course_tutor_id = int(course_tutor_id)
            tutor_id = int(tutor_id)

            cursor.execute('SELECT * FROM tutee WHERE user_id = %s', (user_id,)) 

            tutee = cursor.fetchone()

            if tutee is None:
                cursor.execute('INSERT INTO tutee (user_id) VALUES (%s)', (user_id,))
                tutee_id = cursor.lastrowid
            else:
                tutee_id = tutee['id']

            cursor.execute(
                '''
                INSERT INTO tutor_session (course_tutor_id, tutor_id, tutee_id)
                VALUES (%s, %s, %s)
                ''',
                (course_tutor_id, tutor_id, tutee_id,)
            )

            return redirect(url_for('course.success'))

        abort(400)

@bp.route('/payment-success', methods=(['GET']))
def success():
    try:
        return render_template('tutee/success.html')
    except TemplateNotFound:
        abort(404)