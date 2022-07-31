# from flaskext.mysql import MySQL
# from pymysql import cursors
from dotenv import load_dotenv
import mysql.connector
import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        load_dotenv()
        g.db = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_DATABASE'),
            autocommit=True
        )

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        

def init_db():
    db = get_db()
    
    cursor = db.cursor()
    with open('pator/database/schema.sql', encoding="utf-8") as f:
        query = f.read().split(';')

    for q in query:
        cursor.execute(q)
        print(q)

def seed_db():
    db = get_db()
    
    cursor = db.cursor()
    with open('pator/database/seeder.sql', encoding="utf-8") as f:
        query = f.read().split(';')

    for q in query:
        cursor.execute(q)
        print(q)

@click.command('init-db')
@with_appcontext
def init_db_command():
    """ Clear the existing data and create new tables. """
    init_db()
    click.echo('Initialized the database.')

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """ Adding some data to database. """
    seed_db()
    click.echo('Seeded the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)