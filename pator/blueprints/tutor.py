from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from jinja2 import TemplateNotFound
from werkzeug.exceptions import abort

from pator.blueprints.auth import login_required
from pator.db import get_db

bp = Blueprint('tutor', __name__, url_prefix='/tutor')
bp_create = Blueprint('create', __name__, url_prefix='/create')

bp.register_blueprint(bp_create)

# Work in progress
@bp_create.route('/course', methods=(['POST']))
@login_required
def course():
    if request.method == 'POST':
        course_name = request.form.get('course_name', None)
        course_prodi = request.form.get('course_prodi', None)

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        if None in (course_name, course_prodi):
            error = "Please check you request data."

        print(error)

        if error is None:
            cursor.execute(
                ''' 
                INSERT INTO course (course_name, course_prodi)
                VALUES (%s, %s)
                ''', (course_name, course_prodi,)
            )
            return "ok"
        
        abort(400, error)

@bp_create.route('/detail', methods=('GET', 'POST'))
@login_required
def course_detail():
    if request.method == 'POST':
        hourly_fee = request.form.get('hourly_fee', None)
        course_description = request.form.get('course_description', None)
        course_id = request.form.get('course_id', None)

        db = get_db()
        cursor = db.cursor(dictionary=True)
        error = None

        if None in (hourly_fee, course_id):
            error = "Please check you request data."

        print(error)

        if error is None:
            cursor.execute('SELECT * FROM tutor WHERE user_id = %s', (g.user['id'],)) 

            tutor = cursor.fetchone()

            if tutor is None:
                cursor.execute('INSERT INTO tutor (user_id) VALUES (%s)', (g.user['id'],))
                tutor_id = cursor.lastrowid
            else:
                tutor_id = tutor['id']

            cursor.execute(
                ''' 
                INSERT INTO course_tutor (hourly_fee, course_description, course_id, tutor_id)
                VALUES (%s, %s, %s, %s)
                ''', 
                (hourly_fee, course_description, course_id, tutor_id,)
            )

            return redirect(url_for('tutor.create.success'))
            
        abort(400)


@bp_create.route('/iklan', methods=(['GET']))
@login_required
def iklan():
    try:
        return render_template('tutor/iklan.html')
    except TemplateNotFound:
        abort(404)

@bp_create.route('/iklan-success', methods=(['GET']))
def success():
    try:
        return render_template('tutor/success.html')
    except TemplateNotFound:
        abort(404)