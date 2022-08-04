from flask import Flask, render_template, request

from pator.blueprints.auth import get_user, login_required

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    # index page
    @app.route('/')
    def index():
        print(request.url_rule.endpoint)
        return render_template('index.html')

    # a simple page that says hello
    @app.route('/test')
    # @login_required
    def hello():
        print(get_user())
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from .blueprints import auth, tutor, tutee
    app.register_blueprint(auth.bp)
    app.register_blueprint(tutor.bp)
    app.register_blueprint(tutee.bp)

    


    return app