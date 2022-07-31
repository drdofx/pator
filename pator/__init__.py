from flask import Flask

from pator.blueprints.auth import get_user, login_required

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    from . import db
    db.init_app(app)

    from .blueprints import auth 
    app.register_blueprint(auth.bp)

    # a simple page that says hello
    @app.route('/test')
    # @login_required
    def hello():
        print(get_user())
        return 'Hello, World!'
        cursor = db.get_db().cursor(dictionary=True)
        cursor.execute('SELECT * FROM test')
        res = cursor.fetchall()
        for data in res:
            print(data)



    return app